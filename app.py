from flask import Flask
from routes.hand_route import hand_bp



app = Flask(__name__)


# Register Blueprint
app.register_blueprint(hand_bp)


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )