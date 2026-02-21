from flask import Flask, session
from flask_login import LoginManager

from .config import Config
from .models import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # --- Flask-Login ---
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Veuillez vous connecter."
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(uid):
        user_data = session.get("user_data")
        if user_data and user_data.get("uid") == uid:
            return User.from_dict(user_data)
        return None

    # --- Blueprints ---
    from .auth_routes import auth_bp
    from .social_routes import social_bp
    from .api_routes import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(social_bp, url_prefix="/social")
    app.register_blueprint(api_bp, url_prefix="/api")

    # --- Route racine ---
    @app.route("/")
    def index():
        from flask_login import current_user
        from flask import redirect, url_for

        if current_user.is_authenticated:
            return redirect(url_for("social.friends"))
        return redirect(url_for("auth.login"))

    return app
