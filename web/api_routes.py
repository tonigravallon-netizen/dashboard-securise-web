"""Routes API (AJAX/JSON) pour les actions asynchrones."""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from .helpers import get_firebase

api_bp = Blueprint("api", __name__)


# ── Polling ───────────────────────────────────────────────

@api_bp.route("/poll")
@login_required
def poll():
    fb = get_firebase()
    if not fb:
        return jsonify({"error": "Non connecte"}), 401
    data = fb.poll_updates(current_user.uid)
    return jsonify(data)


# ── Friends ───────────────────────────────────────────────

@api_bp.route("/search-users")
@login_required
def search_users():
    query = request.args.get("q", "").strip()
    if len(query) < 2:
        return jsonify([])

    fb = get_firebase()
    if not fb:
        return jsonify([])

    results = fb.search_users(query, limit=10)
    # Filtrer l'utilisateur courant
    filtered = []
    for u in results:
        if u.get("__id") != current_user.uid:
            filtered.append({
                "uid": u.get("__id", ""),
                "username": u.get("username", ""),
                "display_name": u.get("display_name", u.get("username", "")),
                "online": u.get("online", False),
            })
    return jsonify(filtered)


@api_bp.route("/send-friend-request", methods=["POST"])
@login_required
def send_friend_request():
    data = request.get_json()
    to_uid = data.get("to_uid", "")
    to_username = data.get("to_username", "")

    if not to_uid or not to_username:
        return jsonify({"success": False, "message": "Donnees manquantes."}), 400

    fb = get_firebase()
    if not fb:
        return jsonify({"success": False, "message": "Non connecte."}), 401

    success, message = fb.send_friend_request(
        current_user.uid, current_user.username,
        to_uid, to_username
    )
    return jsonify({"success": success, "message": message})


@api_bp.route("/accept-friend-request", methods=["POST"])
@login_required
def accept_friend_request():
    data = request.get_json()
    request_id = data.get("request_id", "")
    from_uid = data.get("from_uid", "")
    from_username = data.get("from_username", "")

    if not request_id or not from_uid:
        return jsonify({"success": False, "message": "Donnees manquantes."}), 400

    fb = get_firebase()
    if not fb:
        return jsonify({"success": False, "message": "Non connecte."}), 401

    ok = fb.accept_friend_request(
        request_id,
        from_uid, from_username,
        current_user.uid, current_user.username
    )
    return jsonify({"success": ok, "message": "Ami accepte !" if ok else "Erreur."})


@api_bp.route("/decline-friend-request", methods=["POST"])
@login_required
def decline_friend_request():
    data = request.get_json()
    request_id = data.get("request_id", "")

    if not request_id:
        return jsonify({"success": False, "message": "Donnees manquantes."}), 400

    fb = get_firebase()
    if not fb:
        return jsonify({"success": False, "message": "Non connecte."}), 401

    ok = fb.decline_friend_request(request_id)
    return jsonify({"success": ok, "message": "Demande refusee." if ok else "Erreur."})


@api_bp.route("/remove-friend", methods=["POST"])
@login_required
def remove_friend():
    data = request.get_json()
    friend_doc_id = data.get("friend_doc_id", "")

    if not friend_doc_id:
        return jsonify({"success": False, "message": "Donnees manquantes."}), 400

    fb = get_firebase()
    if not fb:
        return jsonify({"success": False, "message": "Non connecte."}), 401

    ok = fb.remove_friend(friend_doc_id)
    return jsonify({"success": ok, "message": "Ami supprime." if ok else "Erreur."})


# ── Messages ──────────────────────────────────────────────

@api_bp.route("/start-conversation", methods=["POST"])
@login_required
def start_conversation():
    data = request.get_json()
    friend_uid = data.get("friend_uid", "")
    friend_username = data.get("friend_username", "")

    if not friend_uid:
        return jsonify({"success": False, "message": "Donnees manquantes."}), 400

    fb = get_firebase()
    if not fb:
        return jsonify({"success": False, "message": "Non connecte."}), 401

    conv_id = fb.get_or_create_conversation(
        current_user.uid, friend_uid,
        current_user.username, friend_username
    )
    return jsonify({"success": True, "conv_id": conv_id})


@api_bp.route("/send-message", methods=["POST"])
@login_required
def send_message():
    data = request.get_json()
    conv_id = data.get("conv_id", "")
    text = data.get("text", "").strip()
    receiver_uid = data.get("receiver_uid", "")

    if not conv_id or not text or not receiver_uid:
        return jsonify({"success": False, "message": "Donnees manquantes."}), 400

    fb = get_firebase()
    if not fb:
        return jsonify({"success": False, "message": "Non connecte."}), 401

    ok = fb.send_message(conv_id, current_user.uid, current_user.username, text, receiver_uid)
    return jsonify({"success": ok})


@api_bp.route("/get-messages/<conv_id>")
@login_required
def get_messages(conv_id):
    fb = get_firebase()
    if not fb:
        return jsonify([])

    msgs = fb.get_messages(conv_id, limit=100)
    # Marquer comme lu
    fb.mark_messages_read(conv_id, current_user.uid)
    return jsonify(msgs)


# ── RDV ───────────────────────────────────────────────────

@api_bp.route("/create-rdv", methods=["POST"])
@login_required
def create_rdv():
    data = request.get_json()
    invitee_uid = data.get("invitee_uid", "")
    invitee_username = data.get("invitee_username", "")
    title = data.get("title", "").strip()
    dt_str = data.get("datetime", "").strip()
    location = data.get("location", "").strip()

    if not invitee_uid or not title or not dt_str:
        return jsonify({"success": False, "message": "Donnees manquantes."}), 400

    fb = get_firebase()
    if not fb:
        return jsonify({"success": False, "message": "Non connecte."}), 401

    success, message = fb.create_appointment(
        current_user.uid, current_user.username,
        invitee_uid, invitee_username,
        title, dt_str, location
    )
    return jsonify({"success": success, "message": message})


@api_bp.route("/respond-rdv", methods=["POST"])
@login_required
def respond_rdv():
    data = request.get_json()
    rdv_id = data.get("rdv_id", "")
    response = data.get("response", "")

    if not rdv_id or response not in ("accepted", "declined"):
        return jsonify({"success": False, "message": "Donnees invalides."}), 400

    fb = get_firebase()
    if not fb:
        return jsonify({"success": False, "message": "Non connecte."}), 401

    ok = fb.respond_to_appointment(rdv_id, response)
    msg = "RDV accepte !" if response == "accepted" else "RDV refuse."
    return jsonify({"success": ok, "message": msg if ok else "Erreur."})
