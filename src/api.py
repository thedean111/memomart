from flask import Flask, jsonify, request, Response
import cv2
import numpy as np
from PIL import Image

class FM_Server:
    preview_contrast = 1.0
    preview_noise = 1.0

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
        self.SetupRoutes()

    # -------------------------------------------------------------------
    # SetupRoutes: Configure the routes in the server
    # -------------------------------------------------------------------
    def SetupRoutes(self):
        @self.app.route("/")
        def index():
            return self.app.send_static_file("index.html")

        @self.app.put("/api/preview-settings")
        def update_preview_settings():

            data = request.get_json()

            if "contrast" in data:
                self.preview_contrast = float(data["contrast"])
            if "noise" in data:
                self.preview_contrast = float(data["noise"])

            return jsonify({
                "contrast": self.preview_contrast,
                "noise": self.preview_noise
            })

        @self.app.get("/api/config")
        def get_config():
            return jsonify(self.application.GetSettings())

        @self.app.put("/api/config")
        def update_config():
            data = request.get_json()

            self.application.UpdateSettings(data)

            return jsonify({
                "success": True
            })

        @self.app.get("/api/camera")
        def camera():
            return Response(
                self._generate_camera_frames(),
                mimetype="multipart/x-mixed-replace; boundary=frame"
            )

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
        self.app.run(
            host="0.0.0.0",
            port=8000
        )
        print("Server running!")
