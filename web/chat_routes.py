"""Blueprint Chat IA - API pour le chatbot ORACLE."""
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from .helpers import get_firebase, sanitize_text
from .gemini_service import get_gemini

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/message", methods=["POST"])
@login_required
def send_message():
    data = request.get_json()
    user_message = sanitize_text(data.get("message", ""), max_length=2000)

    if not user_message:
        return jsonify({"error": "Message vide"}), 400

    fb = get_firebase()
    gemini = get_gemini()

    if not gemini.is_available():
        return jsonify({"error": "ORACLE est hors ligne. Cle API Gemini manquante."}), 503

    # Get conversation history
    history = fb.get_chat_history(current_user.uid)

    # Generate response
    response_text, error = gemini.chat_response(user_message, history)

    if error:
        return jsonify({"error": error}), 500

    # Update history
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": response_text})
    fb.save_chat_history(current_user.uid, history)

    return jsonify({"ok": True, "response": response_text})


@chat_bp.route("/history")
@login_required
def get_history():
    fb = get_firebase()
    history = fb.get_chat_history(current_user.uid)
    return jsonify({"history": history})


@chat_bp.route("/clear", methods=["POST"])
@login_required
def clear_history():
    fb = get_firebase()
    fb.clear_chat_history(current_user.uid)
    return jsonify({"ok": True})
