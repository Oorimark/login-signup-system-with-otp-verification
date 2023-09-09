from flask import Flask
from config.logger.app_logger import app_logger
from waitress import serve
from api.v1.v1 import api_v1

app = Flask(__name__)

# Registering blueprints
app.register_blueprint(api_v1)

# Running application
mode = "dev"
if __name__ == "__main__":
    match mode:
        case "dev":
            app.run(debug=True, port=3112)
            app_logger.info("Starting in development mode")
        case "prod":
            serve(app, host="0.0.0.0", port=4020, threads=10)
            app_logger.info("Starting app in production mode")