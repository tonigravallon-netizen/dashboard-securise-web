"""Routes pour les pages sociales : Amis, Messages, RDV."""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from .helpers import get_firebase

social_bp = Blueprint("social", __name__)


@social_bp.route("/friends")
@login_required
def friends():
    fb = get_firebase()
    if not fb:
        return redirect(url_for("auth.login"))

    # Recuperer les amis
    friends_docs = fb.get_friends(current_user.uid)
    friends_list = []
    for fdoc in friends_docs:
        info = fb.get_friend_info(fdoc, current_user.uid)
        # Recuperer le profil pour le statut en ligne
        profile = fb.get_document("users", info["uid"])
        info["online"] = profile.get("online", False) if profile else False
        info["display_name"] = profile.get("display_name", info["username"]) if profile else info["username"]
        friends_list.append(info)

    # Recuperer les demandes recues
    pending = fb.get_pending_requests(current_user.uid)

    # Recuperer les demandes envoyees
    sent = fb.get_sent_requests(current_user.uid)

    return render_template(
        "social/friends.html",
        friends=friends_list,
        pending_requests=pending,
        sent_requests=sent,
    )


@social_bp.route("/messages")
@login_required
def messages():
    fb = get_firebase()
    if not fb:
        return redirect(url_for("auth.login"))

    # Liste des conversations
    conversations = fb.get_conversations(current_user.uid)
    conv_list = []
    for conv in conversations:
        conv_id = conv.get("__id", "")
        usernames = conv.get("participant_usernames", {})
        participants = conv.get("participants", [])

        # Trouver l'autre utilisateur
        other_uid = ""
        for p in participants:
            if p != current_user.uid:
                other_uid = p
                break

        other_username = usernames.get(other_uid, "Inconnu") if isinstance(usernames, dict) else "Inconnu"

        unread_key = f"unread_{current_user.uid}"
        unread = conv.get(unread_key, 0)
        if isinstance(unread, str):
            unread = int(unread) if unread.isdigit() else 0

        conv_list.append({
            "id": conv_id,
            "other_uid": other_uid,
            "other_username": other_username,
            "last_message": conv.get("last_message", ""),
            "last_message_time": conv.get("last_message_time", ""),
            "unread": unread,
        })

    # Trier par dernier message
    conv_list.sort(key=lambda x: x["last_message_time"], reverse=True)

    return render_template("social/messages.html", conversations=conv_list)


@social_bp.route("/messages/<conv_id>")
@login_required
def chat(conv_id):
    fb = get_firebase()
    if not fb:
        return redirect(url_for("auth.login"))

    # Recuperer la conversation
    conv = fb.get_document("conversations", conv_id)
    if not conv:
        flash("Conversation introuvable.", "error")
        return redirect(url_for("social.messages"))

    # Verifier que l'utilisateur participe
    participants = conv.get("participants", [])
    if current_user.uid not in participants:
        flash("Acces refuse.", "error")
        return redirect(url_for("social.messages"))

    # Trouver l'autre utilisateur
    other_uid = ""
    for p in participants:
        if p != current_user.uid:
            other_uid = p
            break

    usernames = conv.get("participant_usernames", {})
    other_username = usernames.get(other_uid, "Inconnu") if isinstance(usernames, dict) else "Inconnu"

    # Recuperer les messages
    msgs = fb.get_messages(conv_id, limit=100)

    # Marquer comme lu
    fb.mark_messages_read(conv_id, current_user.uid)

    return render_template(
        "social/chat.html",
        conv_id=conv_id,
        other_uid=other_uid,
        other_username=other_username,
        messages=msgs,
    )


@social_bp.route("/rdv")
@login_required
def rdv():
    fb = get_firebase()
    if not fb:
        return redirect(url_for("auth.login"))

    # RDV en attente (recus)
    pending = fb.get_pending_appointments(current_user.uid)

    # RDV envoyes
    sent = fb.get_sent_appointments(current_user.uid)
    sent_pending = [a for a in sent if a.get("status") == "pending"]

    # RDV acceptes
    accepted = fb.get_accepted_appointments(current_user.uid)

    # Recuperer la liste d'amis pour le formulaire
    friends_docs = fb.get_friends(current_user.uid)
    friends_list = []
    for fdoc in friends_docs:
        info = fb.get_friend_info(fdoc, current_user.uid)
        friends_list.append(info)

    return render_template(
        "social/rdv.html",
        pending_rdv=pending,
        sent_rdv=sent_pending,
        accepted_rdv=accepted,
        friends=friends_list,
    )
