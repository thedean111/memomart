from unittest import result

import cv2
import numpy as np
import os
from networkManager import NetworkManager
from io import BytesIO
from flask import Flask, jsonify, request, Response, send_file, session
from PIL import Image
from werkzeug.security import check_password_hash

class FM_Server:
    # -------------------------------------------------------------------
    # __init__: Setup server states
    # -------------------------------------------------------------------
    def __init__(self, application):
        self.app = Flask(
            __name__,
            static_folder="../web",
            static_url_path=""
        )
        self.application = application
        self.app.config["SECRET_KEY"] = os.environ["FM_SECRET_KEY"]
        self.nm = NetworkManager()
        self.SetupRoutes()

    # -------------------------------------------------------------------
    # SetupRoutes: Configure the routes in the server
    # -------------------------------------------------------------------
    def SetupRoutes(self):
        # ---------------- PAGES --------------------------
        @self.app.route("/")
        def index():
            return self.app.send_static_file("index.html")

        # ---------------- REQUESTS --------------------------
        # ------ Get authentication status ------ #
        @self.app.get("/api/auth")
        def get_auth_status():
            authenticated = session.get("authenticated", False)
            return jsonify({"authenticated": authenticated})

        # ------ Retrieve the current configuration ------ #
        @self.app.get("/api/config")
        def get_config():
            return jsonify(self.application.GetSettings())

        # ------ Update configuration parameters ------ #
        @self.app.put("/api/config")
        def update_config():
            data = request.get_json()

            self.application.UpdateSettings(data)

            return jsonify({
                "success": True
            })

        # ------ Stream from the camera ------ #
        @self.app.get("/api/camera")
        def camera():
            return Response(
                self._generate_camera_frames(),
                mimetype="multipart/x-mixed-replace; boundary=frame"
            )

        # ------ Get a preview of the frame ------ #
        @self.app.get("/api/preview")
        def get_preview():
            print("PREVIEW REQUEST", request.args)
            buffer = BytesIO()
            img = self.application.UpdateFrame()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            return send_file(buffer, mimetype="image/png")

        # ------ Login to services ------ #
        @self.app.post("/api/login")
        def login():
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            password_hash = os.environ.get("FM_PASSWORD_HASH")

            if username != "admin":
                return jsonify({"error": "Invalid username or password"}), 401
            
            password_hash = os.environ.get("FM_PASSWORD_HASH")
            if not password_hash or not check_password_hash(password_hash, password):
                return jsonify({"error": "Invalid username or password"}), 401

            session["authenticated"] = True
            return jsonify({"success": True})

        # ------ Get Wifi status ------ #
        @self.app.get("/api/wifi")
        def wifiStatus():
            return jsonify(self.nm.status())

        # ------ Connect to wifi ------ #
        @self.app.post("/api/wifi/connect")
        def connectWifi():
            data = request.get_json(silent=True) or {}

            result = self.nm.connect(
                data.get("ssid"),
                data.get("password")
            )
            return jsonify(result), 200 if result["success"] else 400
        
        # ------ Disconnect from wifi ------ #
        @self.app.post("/api/wifi/disconnect")
        def disconnectWifi():
            result = self.nm.disconnect()
            print(result)
            return jsonify(result), 200 if result["success"] else 400

            
    # -------------------------------------------------------------------
    # ApplyCameraEffects: Apply custom filter to the frame
    # -------------------------------------------------------------------
    def ApplyCameraEffects(self, frame):

        # Rotate
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        target_width = 576
        # 1. Resize down to thermal printer native width (fast)
        h, w = frame.shape[:2]
        target_height = int(target_width * (h / w))
        resized = cv2.resize(frame, (target_width, target_height), interpolation=cv2.INTER_AREA)
        
        # 2. Grayscale conversion
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        
        # 3. Softer contrast adjustment (prevents the background from totally blowing out)
        alpha = 2.
        beta = -10     # Reduced brightness shift
        adjusted = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
        
        # Lighter CLAHE clip limit to preserve midtones
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(adjusted)
        
        # 4. Fast Pillow Floyd-Steinberg Dithering at native low resolution
        pil_img = Image.fromarray(enhanced)
        dithered_img = pil_img.convert('1', dither=Image.FLOYDSTEINBERG)
        
        # 5. Convert directly back to 8-bit numpy array WITHOUT python upscaling
        output_frame = np.array(dithered_img, dtype=np.uint8) * 255

        return output_frame

    # -------------------------------------------------------------------
    # _generate_camera_frames: Compile frames from the camera
    # -------------------------------------------------------------------
    def _generate_camera_frames(self):

        while True:
            frame = self.application.GetCameraFrame()

            if frame is None:
                continue

            frame = self.ApplyCameraEffects(frame)
            success, jpeg = cv2.imencode(".jpg", frame)

            if not success:
                continue

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" +
                jpeg.tobytes() +
                b"\r\n"
            )

    # -------------------------------------------------------------------
    # Run: Start the server
    # -------------------------------------------------------------------
    def Run(self):
        res = self.nm.start()
        print(res)
        
        self.app.run(
            host="0.0.0.0",
            port=8000
        )
        print("Server running!")
