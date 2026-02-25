import re
import time
from datetime import datetime, timezone
from functools import wraps

import bleach
import markdown
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


# ── Markdown & HTML ───────────────────────────────────────

ALLOWED_TAGS = [
    "p", "br", "h1", "h2", "h3", "h4", "h5", "h6",
    "strong", "em", "b", "i", "u", "s", "del",
    "ul", "ol", "li", "blockquote", "pre", "code",
    "a", "img", "hr", "table", "thead", "tbody", "tr", "th", "td",
    "span", "div", "sup", "sub",
]

ALLOWED_ATTRS = {
    "a": ["href", "title", "target", "rel"],
    "img": ["src", "alt", "title", "width", "height", "class"],
    "td": ["align"],
    "th": ["align"],
    "span": ["class", "data-tooltip"],
    "div": ["class", "data-warning"],
    "code": ["class"],
    "pre": ["class"],
}


def render_markdown(text):
    """Convertit du Markdown en HTML securise."""
    if not text:
        return ""
    html = markdown.markdown(text, extensions=["tables", "fenced_code", "nl2br"])
    clean = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)
    return clean


def sanitize_text(text, max_length=10000):
    """Nettoie le texte utilisateur (supprime HTML, limite la longueur)."""
    if not text:
        return ""
    clean = bleach.clean(text, tags=[], strip=True)
    return clean[:max_length]


def truncate_text(text, length=200):
    """Tronque un texte a la longueur donnee."""
    if not text or len(text) <= length:
        return text or ""
    return text[:length].rsplit(" ", 1)[0] + "..."


def slugify(text):
    """Convertit un texte en slug URL-friendly."""
    text = text.lower().strip()
    # Remplacer les caracteres accentues
    replacements = {
        "a": "àâäã", "e": "éèêë", "i": "ïî", "o": "ôö", "u": "ùûü",
        "c": "ç", "n": "ñ",
    }
    for replacement, chars in replacements.items():
        for c in chars:
            text = text.replace(c, replacement)
    # Garder uniquement les caracteres alphanumeriques et les tirets
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text)
    return text.strip("-")[:100]


# ── Formatage de dates ────────────────────────────────────

MOIS_FR = [
    "", "janvier", "fevrier", "mars", "avril", "mai", "juin",
    "juillet", "aout", "septembre", "octobre", "novembre", "decembre",
]


def format_date_fr(iso_date):
    """Formate une date ISO en francais relatif ('il y a 2h', '23 fevrier 2026')."""
    if not iso_date:
        return ""
    try:
        if isinstance(iso_date, str):
            # Gerer differents formats
            iso_date = iso_date.replace("Z", "+00:00")
            if "." in iso_date:
                dt = datetime.fromisoformat(iso_date)
            else:
                dt = datetime.fromisoformat(iso_date)
        else:
            return str(iso_date)

        now = datetime.now(timezone.utc)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        diff = now - dt
        seconds = int(diff.total_seconds())

        if seconds < 60:
            return "a l'instant"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"il y a {minutes} min"
        elif seconds < 86400:
            hours = seconds // 3600
            return f"il y a {hours}h"
        elif seconds < 604800:
            days = seconds // 86400
            return f"il y a {days}j"
        else:
            return f"{dt.day} {MOIS_FR[dt.month]} {dt.year}"
    except (ValueError, TypeError):
        return str(iso_date)[:10] if iso_date else ""


def format_number(n):
    """Formate un nombre (1200 -> '1.2k')."""
    if not n:
        return "0"
    n = int(n) if isinstance(n, str) else n
    if n >= 1000000:
        return f"{n / 1000000:.1f}M"
    elif n >= 1000:
        return f"{n / 1000:.1f}k"
    return str(n)
