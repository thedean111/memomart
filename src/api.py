from flask import Flask, jsonify, request

class FM_Server:
    # -------------------------------------------------------------------
    # __init__: Setup server states
    # -------------------------------------------------------------------
    def __init__(self, application)
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

    # -------------------------------------------------------------------
    # Run: Start the server
    # -------------------------------------------------------------------
    def Run(self):
        self.app.run(
            host="0.0.0.0",
            port=8000
        )