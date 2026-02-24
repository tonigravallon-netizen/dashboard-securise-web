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
    from .wiki_routes import wiki_bp
    from .api_wiki_routes import api_wiki_bp
    from .chat_routes import chat_bp
    from .seed_routes import seed_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(social_bp, url_prefix="/social")
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(wiki_bp)
    app.register_blueprint(api_wiki_bp, url_prefix="/api/wiki")
    app.register_blueprint(chat_bp, url_prefix="/api/chat")
    app.register_blueprint(seed_bp)

    return app
