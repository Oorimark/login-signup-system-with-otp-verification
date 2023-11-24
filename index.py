import logging
from app import app
from waitress import serve

# Application Run Mode
mode = "prod"

if __name__ == "__main__":
    if mode == "dev":
        app.run(debug=True, port=3112)
        logging.info('Starting application in dev mode')
    else:
        serve(app, host="0.0.0.0", port=4020, threads=10)
        logging.info('Starting application in production mode')
