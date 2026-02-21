from flask_login import UserMixin


class User(UserMixin):
    """Utilisateur Flask-Login base sur Firebase Auth."""

    def __init__(self, uid, email, username, display_name="", id_token="", refresh_token="", token_expiry=0):
        self.id = uid
        self.uid = uid
        self.email = email
        self.username = username
        self.display_name = display_name or username
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.token_expiry = token_expiry

    def get_id(self):
        return self.uid

    def to_dict(self):
        return {
            "uid": self.uid,
            "email": self.email,
            "username": self.username,
            "display_name": self.display_name,
            "id_token": self.id_token,
            "refresh_token": self.refresh_token,
            "token_expiry": self.token_expiry,
        }

    @staticmethod
    def from_dict(data):
        if not data:
            return None
        return User(
            uid=data.get("uid", ""),
            email=data.get("email", ""),
            username=data.get("username", ""),
            display_name=data.get("display_name", ""),
            id_token=data.get("id_token", ""),
            refresh_token=data.get("refresh_token", ""),
            token_expiry=data.get("token_expiry", 0),
        )
