"""Firebase REST API service - version autonome pour le deploiement web.

Utilise les variables d'environnement FIREBASE_API_KEY et FIREBASE_PROJECT_ID
ou bien le fichier firebase_config.json en local.
"""
import json
import os
import time
import threading
from datetime import datetime, timezone

import requests

FIREBASE_AUTH_URL = "https://identitytoolkit.googleapis.com/v1"
FIREBASE_TOKEN_URL = "https://securetoken.googleapis.com/v1/token"
FIRESTORE_BASE = "https://firestore.googleapis.com/v1"


def _load_config():
    """Charge la config Firebase depuis les variables d'env ou le fichier JSON."""
    api_key = os.environ.get("FIREBASE_API_KEY", "")
    project_id = os.environ.get("FIREBASE_PROJECT_ID", "")
    if api_key and project_id:
        return {"api_key": api_key, "project_id": project_id}

    # Fallback : lire firebase_config.json dans le dossier parent (dev local)
    for path in [
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "firebase_config.json"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "firebase_config.json"),
    ]:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return {"api_key": data.get("api_key", ""), "project_id": data.get("project_id", "")}
            except (json.JSONDecodeError, OSError):
                pass
    return {"api_key": "", "project_id": ""}


class FirebaseService:
    """Handles all Firebase operations via REST API."""

    def __init__(self):
        self.config = _load_config()
        self.id_token = None
        self.refresh_token = None
        self.firebase_uid = None
        self.token_expiry = 0
        self._lock = threading.Lock()

    def is_ready(self):
        return bool(self.config.get("api_key")) and bool(self.config.get("project_id"))

    def _api_key(self):
        return self.config.get("api_key", "")

    def _project_id(self):
        return self.config.get("project_id", "")

    # ── Firebase Auth ────────────────────────────────────────

    def sign_up(self, email, password):
        if not self.is_ready():
            return False, "Firebase non configure.", {}
        url = f"{FIREBASE_AUTH_URL}/accounts:signUp?key={self._api_key()}"
        payload = {"email": email, "password": password, "returnSecureToken": True}
        try:
            resp = requests.post(url, json=payload, timeout=10)
            data = resp.json()
            if resp.status_code == 200:
                self.id_token = data.get("idToken")
                self.refresh_token = data.get("refreshToken")
                self.firebase_uid = data.get("localId")
                self.token_expiry = time.time() + int(data.get("expiresIn", 3600))
                return True, "Compte Firebase cree.", data
            else:
                error_msg = data.get("error", {}).get("message", "Erreur inconnue")
                return False, f"Erreur Firebase: {error_msg}", data
        except requests.RequestException as e:
            return False, f"Erreur reseau: {e}", {}

    def sign_in(self, email, password):
        if not self.is_ready():
            return False, "Firebase non configure.", {}
        url = f"{FIREBASE_AUTH_URL}/accounts:signInWithPassword?key={self._api_key()}"
        payload = {"email": email, "password": password, "returnSecureToken": True}
        try:
            resp = requests.post(url, json=payload, timeout=10)
            data = resp.json()
            if resp.status_code == 200:
                self.id_token = data.get("idToken")
                self.refresh_token = data.get("refreshToken")
                self.firebase_uid = data.get("localId")
                self.token_expiry = time.time() + int(data.get("expiresIn", 3600))
                return True, "Connecte a Firebase.", data
            else:
                error_msg = data.get("error", {}).get("message", "Erreur inconnue")
                return False, f"Erreur Firebase: {error_msg}", data
        except requests.RequestException as e:
            return False, f"Erreur reseau: {e}", {}

    def _refresh_id_token(self):
        if not self.refresh_token:
            return False
        url = f"{FIREBASE_TOKEN_URL}?key={self._api_key()}"
        payload = {"grant_type": "refresh_token", "refresh_token": self.refresh_token}
        try:
            resp = requests.post(url, data=payload, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                self.id_token = data.get("id_token")
                self.refresh_token = data.get("refresh_token")
                self.token_expiry = time.time() + int(data.get("expires_in", 3600))
                return True
        except requests.RequestException:
            pass
        return False

    def _get_headers(self):
        with self._lock:
            if time.time() >= self.token_expiry - 60:
                self._refresh_id_token()
        return {"Authorization": f"Bearer {self.id_token}", "Content-Type": "application/json"}

    def is_authenticated(self):
        return self.id_token is not None and self.firebase_uid is not None

    # ── Firestore Helpers ────────────────────────────────────

    def _fs_url(self, path=""):
        base = f"{FIRESTORE_BASE}/projects/{self._project_id()}/databases/(default)/documents"
        return f"{base}/{path}" if path else base

    @staticmethod
    def _to_fs_value(val):
        if val is None:
            return {"nullValue": None}
        elif isinstance(val, bool):
            return {"booleanValue": val}
        elif isinstance(val, int):
            return {"integerValue": str(val)}
        elif isinstance(val, float):
            return {"doubleValue": val}
        elif isinstance(val, str):
            return {"stringValue": val}
        elif isinstance(val, datetime):
            return {"timestampValue": val.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}
        elif isinstance(val, list):
            return {"arrayValue": {"values": [FirebaseService._to_fs_value(v) for v in val]}}
        elif isinstance(val, dict):
            return {"mapValue": {"fields": {k: FirebaseService._to_fs_value(v) for k, v in val.items()}}}
        return {"stringValue": str(val)}

    @staticmethod
    def _from_fs_value(val):
        if "stringValue" in val:
            return val["stringValue"]
        elif "integerValue" in val:
            return int(val["integerValue"])
        elif "doubleValue" in val:
            return val["doubleValue"]
        elif "booleanValue" in val:
            return val["booleanValue"]
        elif "nullValue" in val:
            return None
        elif "timestampValue" in val:
            return val["timestampValue"]
        elif "arrayValue" in val:
            return [FirebaseService._from_fs_value(v) for v in val["arrayValue"].get("values", [])]
        elif "mapValue" in val:
            return {k: FirebaseService._from_fs_value(v) for k, v in val["mapValue"].get("fields", {}).items()}
        return None

    def _parse_doc(self, doc):
        fields = doc.get("fields", {})
        result = {k: self._from_fs_value(v) for k, v in fields.items()}
        name = doc.get("name", "")
        if name:
            result["__id"] = name.split("/")[-1]
        return result

    # ── Firestore CRUD ───────────────────────────────────────

    def set_document(self, collection, doc_id, data):
        url = f"{self._fs_url(collection)}/{doc_id}"
        body = {"fields": {k: self._to_fs_value(v) for k, v in data.items()}}
        try:
            resp = requests.patch(url, json=body, headers=self._get_headers(), timeout=10)
            return resp.status_code == 200
        except requests.RequestException:
            return False

    def get_document(self, collection, doc_id):
        url = f"{self._fs_url(collection)}/{doc_id}"
        try:
            resp = requests.get(url, headers=self._get_headers(), timeout=10)
            if resp.status_code == 200:
                return self._parse_doc(resp.json())
        except requests.RequestException:
            pass
        return None

    def add_document(self, collection, data):
        url = self._fs_url(collection)
        body = {"fields": {k: self._to_fs_value(v) for k, v in data.items()}}
        try:
            resp = requests.post(url, json=body, headers=self._get_headers(), timeout=10)
            if resp.status_code == 200:
                name = resp.json().get("name", "")
                return name.split("/")[-1] if name else ""
        except requests.RequestException:
            pass
        return ""

    def update_fields(self, collection, doc_id, fields):
        url = f"{self._fs_url(collection)}/{doc_id}"
        mask = "&".join(f"updateMask.fieldPaths={k}" for k in fields.keys())
        body = {"fields": {k: self._to_fs_value(v) for k, v in fields.items()}}
        try:
            resp = requests.patch(f"{url}?{mask}", json=body, headers=self._get_headers(), timeout=10)
            return resp.status_code == 200
        except requests.RequestException:
            return False

    def delete_document(self, collection, doc_id):
        url = f"{self._fs_url(collection)}/{doc_id}"
        try:
            resp = requests.delete(url, headers=self._get_headers(), timeout=10)
            return resp.status_code == 200
        except requests.RequestException:
            return False

    def query_collection(self, collection, field, op, value, order_by="", limit=50):
        url = f"{self._fs_url()}:runQuery"
        sq = {
            "from": [{"collectionId": collection}],
            "where": {"fieldFilter": {"field": {"fieldPath": field}, "op": op, "value": self._to_fs_value(value)}},
            "limit": limit,
        }
        if order_by:
            sq["orderBy"] = [{"field": {"fieldPath": order_by}, "direction": "DESCENDING"}]
        try:
            resp = requests.post(url, json={"structuredQuery": sq}, headers=self._get_headers(), timeout=10)
            if resp.status_code == 200:
                return [self._parse_doc(item["document"]) for item in resp.json() if "document" in item]
        except requests.RequestException:
            pass
        return []

    def query_two_conditions(self, collection, field1, op1, value1, field2, op2, value2, order_by="", limit=50):
        url = f"{self._fs_url()}:runQuery"
        sq = {
            "from": [{"collectionId": collection}],
            "where": {"compositeFilter": {"op": "AND", "filters": [
                {"fieldFilter": {"field": {"fieldPath": field1}, "op": op1, "value": self._to_fs_value(value1)}},
                {"fieldFilter": {"field": {"fieldPath": field2}, "op": op2, "value": self._to_fs_value(value2)}},
            ]}},
            "limit": limit,
        }
        if order_by:
            sq["orderBy"] = [{"field": {"fieldPath": order_by}, "direction": "DESCENDING"}]
        try:
            resp = requests.post(url, json={"structuredQuery": sq}, headers=self._get_headers(), timeout=10)
            if resp.status_code == 200:
                return [self._parse_doc(item["document"]) for item in resp.json() if "document" in item]
        except requests.RequestException:
            pass
        return []

    def query_subcollection(self, parent_collection, parent_id, subcollection, order_by="", order_dir="ASCENDING", limit=50):
        url = f"{self._fs_url(f'{parent_collection}/{parent_id}')}:runQuery"
        sq = {"from": [{"collectionId": subcollection}], "limit": limit}
        if order_by:
            sq["orderBy"] = [{"field": {"fieldPath": order_by}, "direction": order_dir}]
        try:
            resp = requests.post(url, json={"structuredQuery": sq}, headers=self._get_headers(), timeout=10)
            if resp.status_code == 200:
                return [self._parse_doc(item["document"]) for item in resp.json() if "document" in item]
        except requests.RequestException:
            pass
        return []

    def add_to_subcollection(self, parent_collection, parent_id, subcollection, data):
        path = f"{parent_collection}/{parent_id}/{subcollection}"
        url = self._fs_url(path)
        body = {"fields": {k: self._to_fs_value(v) for k, v in data.items()}}
        try:
            resp = requests.post(url, json=body, headers=self._get_headers(), timeout=10)
            if resp.status_code == 200:
                name = resp.json().get("name", "")
                return name.split("/")[-1] if name else ""
        except requests.RequestException:
            pass
        return ""

    # ── User Profiles ────────────────────────────────────────

    def create_user_profile(self, uid, username, display_name, email):
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return self.set_document("users", uid, {
            "username": username.lower(), "display_name": display_name or username,
            "email": email, "online": True, "last_seen": now, "created_at": now,
        })

    def update_online_status(self, uid, online):
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return self.update_fields("users", uid, {"online": online, "last_seen": now})

    def search_users(self, query_text, limit=10):
        query_text = query_text.lower().strip()
        if not query_text:
            return []
        return self.query_two_conditions("users",
            "username", "GREATER_THAN_OR_EQUAL", query_text,
            "username", "LESS_THAN", query_text + "\uf8ff", limit=limit)

    def get_user_by_username(self, username):
        results = self.query_collection("users", "username", "EQUAL", username.lower(), limit=1)
        return results[0] if results else None

    # ── Friends System ───────────────────────────────────────

    def send_friend_request(self, from_uid, from_username, to_uid, to_username):
        friends = self.get_friends(from_uid)
        for f in friends:
            if f.get("user1_uid") == to_uid or f.get("user2_uid") == to_uid:
                return False, "Vous etes deja amis."
        existing = self.query_two_conditions("friend_requests", "from_uid", "EQUAL", from_uid, "to_uid", "EQUAL", to_uid, limit=1)
        if existing and existing[0].get("status") == "pending":
            return False, "Demande deja envoyee."
        reverse = self.query_two_conditions("friend_requests", "from_uid", "EQUAL", to_uid, "to_uid", "EQUAL", from_uid, limit=1)
        if reverse and reverse[0].get("status") == "pending":
            req_id = reverse[0].get("__id")
            if req_id:
                self.accept_friend_request(req_id, to_uid, to_username, from_uid, from_username)
                return True, "Demande acceptee automatiquement (demande reciproque)."
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        doc_id = self.add_document("friend_requests", {
            "from_uid": from_uid, "to_uid": to_uid,
            "from_username": from_username.lower(), "to_username": to_username.lower(),
            "status": "pending", "created_at": now,
        })
        return (True, "Demande d'ami envoyee !") if doc_id else (False, "Erreur lors de l'envoi.")

    def get_pending_requests(self, uid):
        return self.query_two_conditions("friend_requests", "to_uid", "EQUAL", uid, "status", "EQUAL", "pending")

    def get_sent_requests(self, uid):
        return self.query_two_conditions("friend_requests", "from_uid", "EQUAL", uid, "status", "EQUAL", "pending")

    def accept_friend_request(self, request_id, user1_uid, user1_username, user2_uid, user2_username):
        ok = self.update_fields("friend_requests", request_id, {"status": "accepted"})
        if not ok:
            return False
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        self.add_document("friends", {
            "users": [user1_uid, user2_uid],
            "user1_uid": user1_uid, "user2_uid": user2_uid,
            "user1_username": user1_username.lower(), "user2_username": user2_username.lower(),
            "since": now,
        })
        return True

    def decline_friend_request(self, request_id):
        return self.update_fields("friend_requests", request_id, {"status": "declined"})

    def get_friends(self, uid):
        return self.query_collection("friends", "users", "ARRAY_CONTAINS", uid, limit=100)

    def remove_friend(self, friend_doc_id):
        return self.delete_document("friends", friend_doc_id)

    def get_friend_info(self, friend_doc, my_uid):
        if friend_doc.get("user1_uid") == my_uid:
            return {"uid": friend_doc.get("user2_uid", ""), "username": friend_doc.get("user2_username", ""), "friend_doc_id": friend_doc.get("__id", "")}
        return {"uid": friend_doc.get("user1_uid", ""), "username": friend_doc.get("user1_username", ""), "friend_doc_id": friend_doc.get("__id", "")}

    # ── Messaging ────────────────────────────────────────────

    def _conversation_id(self, uid1, uid2):
        uids = sorted([uid1, uid2])
        return f"{uids[0]}_{uids[1]}"

    def get_or_create_conversation(self, uid1, uid2, username1, username2):
        conv_id = self._conversation_id(uid1, uid2)
        doc = self.get_document("conversations", conv_id)
        if doc:
            return conv_id
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        self.set_document("conversations", conv_id, {
            "participants": [uid1, uid2],
            "participant_usernames": {uid1: username1, uid2: username2},
            "last_message": "", "last_message_time": now,
            f"unread_{uid1}": 0, f"unread_{uid2}": 0,
        })
        return conv_id

    def send_message(self, conversation_id, sender_uid, sender_username, text, receiver_uid):
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        msg_id = self.add_to_subcollection("conversations", conversation_id, "messages", {
            "sender_uid": sender_uid, "sender_username": sender_username,
            "text": text, "timestamp": now, "read": False,
        })
        if msg_id:
            conv = self.get_document("conversations", conversation_id)
            unread_key = f"unread_{receiver_uid}"
            current_unread = 0
            if conv:
                current_unread = conv.get(unread_key, 0)
                if isinstance(current_unread, str):
                    current_unread = int(current_unread) if current_unread.isdigit() else 0
            self.update_fields("conversations", conversation_id, {
                "last_message": text[:100], "last_message_time": now, unread_key: current_unread + 1,
            })
            return True
        return False

    def get_messages(self, conversation_id, limit=50):
        return self.query_subcollection("conversations", conversation_id, "messages", order_by="timestamp", order_dir="ASCENDING", limit=limit)

    def mark_messages_read(self, conversation_id, reader_uid):
        return self.update_fields("conversations", conversation_id, {f"unread_{reader_uid}": 0})

    def get_conversations(self, uid):
        return self.query_collection("conversations", "participants", "ARRAY_CONTAINS", uid, limit=50)

    def get_unread_total(self, uid):
        convs = self.get_conversations(uid)
        total = 0
        for conv in convs:
            count = conv.get(f"unread_{uid}", 0)
            if isinstance(count, str):
                count = int(count) if count.isdigit() else 0
            total += count
        return total

    # ── Shared Appointments ──────────────────────────────────

    def create_appointment(self, creator_uid, creator_username, invitee_uid, invitee_username, title, dt_str, location):
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        doc_id = self.add_document("shared_appointments", {
            "creator_uid": creator_uid, "creator_username": creator_username.lower(),
            "invitee_uid": invitee_uid, "invitee_username": invitee_username.lower(),
            "title": title, "datetime": dt_str, "location": location,
            "status": "pending", "created_at": now,
        })
        return (True, "Invitation envoyee !") if doc_id else (False, "Erreur lors de l'envoi.")

    def get_pending_appointments(self, uid):
        return self.query_two_conditions("shared_appointments", "invitee_uid", "EQUAL", uid, "status", "EQUAL", "pending")

    def get_sent_appointments(self, uid):
        return self.query_collection("shared_appointments", "creator_uid", "EQUAL", uid)

    def get_accepted_appointments(self, uid):
        as_creator = self.query_two_conditions("shared_appointments", "creator_uid", "EQUAL", uid, "status", "EQUAL", "accepted")
        as_invitee = self.query_two_conditions("shared_appointments", "invitee_uid", "EQUAL", uid, "status", "EQUAL", "accepted")
        return as_creator + as_invitee

    def respond_to_appointment(self, appointment_id, response):
        return self.update_fields("shared_appointments", appointment_id, {"status": response})

    # ── Polling ──────────────────────────────────────────────

    def poll_updates(self, uid):
        result = {"unread_messages": 0, "pending_requests": 0, "pending_appointments": 0}
        try:
            result["unread_messages"] = self.get_unread_total(uid)
            result["pending_requests"] = len(self.get_pending_requests(uid))
            result["pending_appointments"] = len(self.get_pending_appointments(uid))
        except Exception:
            pass
        return result

    # ── Wiki Articles ─────────────────────────────────────────

    def create_article(self, data):
        """Cree un nouvel article. Retourne le doc_id ou ''."""
        return self.add_document("articles", data)

    def get_article_by_slug(self, slug):
        """Recupere un article par son slug."""
        results = self.query_collection("articles", "slug", "EQUAL", slug, limit=1)
        return results[0] if results else None

    def get_article_by_id(self, article_id):
        """Recupere un article par son ID Firestore."""
        return self.get_document("articles", article_id)

    def update_article(self, article_id, data):
        """Met a jour les champs d'un article."""
        return self.update_fields("articles", article_id, data)

    def list_articles(self, status="published", limit=20):
        """Liste les articles publies, tries par date de creation descendante."""
        return self.query_collection("articles", "status", "EQUAL", status,
                                     order_by="created_at", limit=limit)

    def get_featured_articles(self, limit=6):
        """Recupere les articles en vedette."""
        return self.query_two_conditions("articles",
            "featured", "EQUAL", True,
            "status", "EQUAL", "published",
            limit=limit)

    def get_articles_by_category(self, category, limit=20):
        """Recupere les articles d'une categorie donnee."""
        return self.query_two_conditions("articles",
            "category", "EQUAL", category,
            "status", "EQUAL", "published",
            order_by="created_at", limit=limit)

    def get_articles_by_tag(self, tag, limit=20):
        """Recupere les articles contenant un tag specifique."""
        return self.query_two_conditions("articles",
            "tags", "ARRAY_CONTAINS", tag,
            "status", "EQUAL", "published",
            limit=limit)

    def get_articles_by_author(self, author_uid, limit=20):
        """Recupere les articles d'un auteur."""
        return self.query_collection("articles", "author_uid", "EQUAL", author_uid,
                                     order_by="created_at", limit=limit)

    def search_articles(self, query_text, limit=20):
        """Recherche d'articles par prefixe de titre (Firestore limitation)."""
        query_text = query_text.lower().strip()
        if not query_text:
            return []
        return self.query_two_conditions("articles",
            "title_lower", "GREATER_THAN_OR_EQUAL", query_text,
            "title_lower", "LESS_THAN", query_text + "\uf8ff",
            limit=limit)

    def increment_views(self, article_id, current_views):
        """Incremente le compteur de vues d'un article."""
        return self.update_fields("articles", article_id, {"views": current_views + 1})

    # ── Article Votes ─────────────────────────────────────────

    def vote_article(self, article_id, user_uid, vote_type):
        """Vote pour un article (up/down). Retourne (success, new_upvotes, new_downvotes)."""
        vote_doc_id = f"{article_id}_{user_uid}"
        existing = self.get_document("article_votes", vote_doc_id)

        article = self.get_article_by_id(article_id)
        if not article:
            return False, 0, 0

        upvotes = article.get("upvotes", 0)
        downvotes = article.get("downvotes", 0)
        if isinstance(upvotes, str):
            upvotes = int(upvotes)
        if isinstance(downvotes, str):
            downvotes = int(downvotes)

        if existing:
            old_vote = existing.get("vote_type", "")
            if old_vote == vote_type:
                # Retirer le vote
                self.delete_document("article_votes", vote_doc_id)
                if vote_type == "up":
                    upvotes = max(0, upvotes - 1)
                else:
                    downvotes = max(0, downvotes - 1)
            else:
                # Changer le vote
                now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                self.set_document("article_votes", vote_doc_id, {
                    "article_id": article_id, "user_uid": user_uid,
                    "vote_type": vote_type, "created_at": now,
                })
                if vote_type == "up":
                    upvotes += 1
                    downvotes = max(0, downvotes - 1)
                else:
                    downvotes += 1
                    upvotes = max(0, upvotes - 1)
        else:
            # Nouveau vote
            now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            self.set_document("article_votes", vote_doc_id, {
                "article_id": article_id, "user_uid": user_uid,
                "vote_type": vote_type, "created_at": now,
            })
            if vote_type == "up":
                upvotes += 1
            else:
                downvotes += 1

        self.update_fields("articles", article_id, {"upvotes": upvotes, "downvotes": downvotes})
        return True, upvotes, downvotes

    def get_user_vote(self, article_id, user_uid):
        """Retourne le vote de l'utilisateur sur un article ('up', 'down', ou None)."""
        vote_doc_id = f"{article_id}_{user_uid}"
        doc = self.get_document("article_votes", vote_doc_id)
        if doc:
            return doc.get("vote_type")
        return None

    # ── Article Comments ──────────────────────────────────────

    def add_comment(self, article_id, data):
        """Ajoute un commentaire a un article. Retourne le comment_id."""
        comment_id = self.add_to_subcollection("articles", article_id, "comments", data)
        if comment_id:
            # Incrementer le compteur de commentaires
            article = self.get_article_by_id(article_id)
            if article:
                count = article.get("comment_count", 0)
                if isinstance(count, str):
                    count = int(count)
                self.update_fields("articles", article_id, {"comment_count": count + 1})
        return comment_id

    def get_comments(self, article_id, limit=50):
        """Recupere les commentaires d'un article."""
        return self.query_subcollection("articles", article_id, "comments",
                                        order_by="created_at", order_dir="DESCENDING", limit=limit)

    # ── Chat History (IA) ─────────────────────────────────────

    def get_chat_history(self, user_uid):
        """Recupere l'historique de chat IA de l'utilisateur."""
        results = self.query_collection("chat_history", "user_uid", "EQUAL", user_uid, limit=1)
        return results[0] if results else None

    def save_chat_history(self, user_uid, messages):
        """Sauvegarde l'historique de chat IA (max 20 messages)."""
        messages = messages[-20:]  # garder les 20 derniers
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        existing = self.get_chat_history(user_uid)
        if existing and existing.get("__id"):
            return self.update_fields("chat_history", existing["__id"], {
                "messages": messages, "updated_at": now,
            })
        else:
            return self.add_document("chat_history", {
                "user_uid": user_uid, "messages": messages,
                "created_at": now, "updated_at": now,
            })

    def clear_chat_history(self, user_uid):
        """Supprime l'historique de chat IA."""
        existing = self.get_chat_history(user_uid)
        if existing and existing.get("__id"):
            return self.delete_document("chat_history", existing["__id"])
        return True

    # ── Categories ────────────────────────────────────────────

    def get_categories(self):
        """Recupere toutes les categories."""
        url = f"{self._fs_url('categories')}"
        try:
            resp = requests.get(url, headers=self._get_headers(), timeout=10)
            if resp.status_code == 200:
                docs = resp.json().get("documents", [])
                return [self._parse_doc(doc) for doc in docs]
        except requests.RequestException:
            pass
        return []

    def init_categories(self):
        """Initialise les categories par defaut si elles n'existent pas."""
        categories = [
            {"slug": "technologie", "name": "Technologie & Surveillance", "icon": "eye", "description": "IA, 5G, puces, surveillance de masse...", "color": "#00ff41", "article_count": 0, "order": 1},
            {"slug": "histoire", "name": "Histoire Secrete", "icon": "scroll", "description": "Evenements historiques revisites, documents declassifies...", "color": "#d4af37", "article_count": 0, "order": 2},
            {"slug": "politique", "name": "Politique & Pouvoir", "icon": "landmark", "description": "Gouvernements de l'ombre, lobbying, manipulations...", "color": "#dc2626", "article_count": 0, "order": 3},
            {"slug": "espace", "name": "Espace & Extraterrestres", "icon": "rocket", "description": "OVNI, Zone 51, programmes spatiaux secrets...", "color": "#22d3ee", "article_count": 0, "order": 4},
            {"slug": "sante", "name": "Sante & Big Pharma", "icon": "flask", "description": "Industrie pharmaceutique, essais cliniques, medecine alternative...", "color": "#a855f7", "article_count": 0, "order": 5},
            {"slug": "finance", "name": "Finance & Economie", "icon": "banknote", "description": "Banques centrales, cryptomonnaies, systeme monetaire...", "color": "#f59e0b", "article_count": 0, "order": 6},
            {"slug": "occultisme", "name": "Occultisme & Societes Secretes", "icon": "triangle", "description": "Illuminati, Franc-maconnerie, rituels, symbolisme...", "color": "#ec4899", "article_count": 0, "order": 7},
            {"slug": "science", "name": "Science Cachee", "icon": "atom", "description": "Technologies supprimees, energie libre, physique alternative...", "color": "#3b82f6", "article_count": 0, "order": 8},
        ]
        for cat in categories:
            existing = self.get_document("categories", cat["slug"])
            if not existing:
                self.set_document("categories", cat["slug"], cat)
