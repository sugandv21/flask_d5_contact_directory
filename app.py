from flask import Flask
from config import Config
from extensions import db
from routes import main
import os

def create_app():
    template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates")
    app = Flask(__name__, template_folder=template_dir)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()  # auto-generate .db

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
