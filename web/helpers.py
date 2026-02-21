import time
from functools import wraps

from flask import session, redirect, url_for, flash, g
from flask_login import current_user

from .firebase_service import FirebaseService


def get_firebase():
    """Retourne une instance FirebaseService configuree avec les tokens de l'utilisateur courant."""
    if "firebase" not in g:
        fb = FirebaseService()
        if current_user.is_authenticated:
            fb.id_token = current_user.id_token
            fb.refresh_token = current_user.refresh_token
            fb.firebase_uid = current_user.uid
            fb.token_expiry = current_user.token_expiry

            # Auto-refresh si le token expire dans moins de 60 secondes
            if fb.token_expiry and time.time() > fb.token_expiry - 60:
                if fb._refresh_id_token():
                    current_user.id_token = fb.id_token
                    current_user.refresh_token = fb.refresh_token
                    current_user.token_expiry = fb.token_expiry
                    session["user_data"] = current_user.to_dict()

        g.firebase = fb
    return g.firebase


def firebase_required(f):
    """Decorateur : verifie que l'utilisateur est connecte et que Firebase est pret."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Veuillez vous connecter.", "warning")
            return redirect(url_for("auth.login"))
        fb = get_firebase()
        if not fb.is_authenticated():
            flash("Session expiree, reconnectez-vous.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function
