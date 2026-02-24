import time

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user

from .models import User
from .helpers import get_firebase
from .firebase_service import FirebaseService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("wiki.home"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Veuillez remplir tous les champs.", "error")
            return render_template("auth/login.html")

        fb = FirebaseService()
        success, message, data = fb.sign_in(email, password)

        if success:
            uid = data.get("localId", "")
            # Recuperer le profil utilisateur depuis Firestore
            profile = fb.get_document("users", uid)
            username = profile.get("username", email.split("@")[0]) if profile else email.split("@")[0]
            display_name = profile.get("display_name", username) if profile else username

            user = User(
                uid=uid,
                email=email,
                username=username,
                display_name=display_name,
                id_token=fb.id_token,
                refresh_token=fb.refresh_token,
                token_expiry=time.time() + 3500,
            )

            session["user_data"] = user.to_dict()
            login_user(user, remember=True)

            # Mettre a jour le statut en ligne
            fb.update_online_status(uid, True)

            flash(f"Bienvenue, {display_name} !", "success")
            return redirect(url_for("wiki.home"))
        else:
            # Traduire les erreurs Firebase
            error_msg = _translate_error(message)
            flash(error_msg, "error")

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("wiki.home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        password2 = request.form.get("password2", "")

        # Validation
        if not all([username, email, password, password2]):
            flash("Veuillez remplir tous les champs.", "error")
            return render_template("auth/register.html")

        if len(username) < 3:
            flash("Le nom d'utilisateur doit faire au moins 3 caracteres.", "error")
            return render_template("auth/register.html")

        if password != password2:
            flash("Les mots de passe ne correspondent pas.", "error")
            return render_template("auth/register.html")

        if len(password) < 6:
            flash("Le mot de passe doit faire au moins 6 caracteres.", "error")
            return render_template("auth/register.html")

        fb = FirebaseService()

        # Verifier si le username est deja pris
        existing = fb.get_user_by_username(username)
        if existing:
            flash("Ce nom d'utilisateur est deja pris.", "error")
            return render_template("auth/register.html")

        # Creer le compte Firebase Auth
        success, message, data = fb.sign_up(email, password)

        if success:
            uid = data.get("localId", "")

            # Creer le profil Firestore
            fb.create_user_profile(uid, username, username, email)

            user = User(
                uid=uid,
                email=email,
                username=username,
                display_name=username,
                id_token=fb.id_token,
                refresh_token=fb.refresh_token,
                token_expiry=time.time() + 3500,
            )

            session["user_data"] = user.to_dict()
            login_user(user, remember=True)

            flash("Compte cree avec succes !", "success")
            return redirect(url_for("wiki.home"))
        else:
            error_msg = _translate_error(message)
            flash(error_msg, "error")

    return render_template("auth/register.html")


@auth_bp.route("/logout")
def logout():
    if current_user.is_authenticated:
        try:
            fb = get_firebase()
            fb.update_online_status(current_user.uid, False)
        except Exception:
            pass

    session.clear()
    logout_user()
    flash("Deconnexion reussie.", "info")
    return redirect(url_for("auth.login"))


def _translate_error(msg):
    """Traduit les erreurs Firebase Auth en francais."""
    msg_lower = msg.lower()
    if "email_not_found" in msg_lower or "user_not_found" in msg_lower:
        return "Aucun compte avec cet email."
    if "invalid_password" in msg_lower or "wrong_password" in msg_lower:
        return "Mot de passe incorrect."
    if "email_exists" in msg_lower:
        return "Un compte avec cet email existe deja."
    if "weak_password" in msg_lower:
        return "Mot de passe trop faible (min. 6 caracteres)."
    if "invalid_email" in msg_lower:
        return "Adresse email invalide."
    if "too_many_attempts" in msg_lower:
        return "Trop de tentatives. Reessayez plus tard."
    if "invalid_login_credentials" in msg_lower:
        return "Email ou mot de passe incorrect."
    return f"Erreur : {msg}"
