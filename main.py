from api import app
import os

if __name__ == "__main__":
    os.environ
    os.environ['TEST']="esta es un aprueba"
    app.run(debug=True, port=5000, host="0.0.0.0")
