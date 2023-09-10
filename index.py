from App import app
from waitress import serve

# Running application
mode = "dev"

if __name__ == "__main__":
    match mode:
        case "dev":
            app.run(debug=True, port=3112)
        case "prod":
            serve(app, host="0.0.0.0", port=4020, threads=10)