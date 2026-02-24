"""Blueprint API wiki - Endpoints JSON pour les actions AJAX."""
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from .helpers import get_firebase, render_markdown, sanitize_text, truncate_text, slugify
from .gemini_service import get_gemini

api_wiki_bp = Blueprint("api_wiki", __name__)


@api_wiki_bp.route("/vote", methods=["POST"])
@login_required
def vote():
    data = request.get_json()
    article_id = data.get("article_id", "")
    vote_type = data.get("vote_type", "")
    
    if not article_id or vote_type not in ("up", "down"):
        return jsonify({"error": "Parametres invalides"}), 400
    
    fb = get_firebase()
    success, upvotes, downvotes = fb.vote_article(article_id, current_user.uid, vote_type)
    
    if success:
        return jsonify({"ok": True, "upvotes": upvotes, "downvotes": downvotes})
    return jsonify({"error": "Erreur lors du vote"}), 500


@api_wiki_bp.route("/comment", methods=["POST"])
@login_required
def add_comment():
    data = request.get_json()
    article_id = data.get("article_id", "")
    text = sanitize_text(data.get("text", ""), max_length=2000)
    
    if not article_id or not text:
        return jsonify({"error": "Commentaire vide"}), 400
    
    fb = get_firebase()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    comment_data = {
        "author_uid": current_user.uid,
        "author_username": current_user.username or current_user.display_name or "anonyme",
        "text": text,
        "created_at": now,
        "upvotes": 0,
    }
    
    comment_id = fb.add_comment(article_id, comment_data)
    if comment_id:
        return jsonify({"ok": True, "comment_id": comment_id, "comment": comment_data})
    return jsonify({"error": "Erreur"}), 500


@api_wiki_bp.route("/comments/<article_id>")
def get_comments(article_id):
    fb = get_firebase()
    comments = fb.get_comments(article_id, limit=50)
    return jsonify({"comments": comments})


@api_wiki_bp.route("/generate-article", methods=["POST"])
@login_required
def generate_article():
    data = request.get_json()
    subject = sanitize_text(data.get("subject", ""), max_length=500)
    category = data.get("category", "")
    tone = data.get("tone", "neutre")
    length = data.get("length", "moyen")
    
    if not subject:
        return jsonify({"error": "Sujet requis"}), 400
    
    gemini = get_gemini()
    if not gemini.is_available():
        return jsonify({"error": "Service IA non disponible. Verifiez la cle API Gemini."}), 503
    
    content, error = gemini.generate_article(subject, category, tone, length)
    if error:
        return jsonify({"error": error}), 500
    
    # Generate summary
    summary = truncate_text(content.replace("#", "").replace("*", "").strip(), 200)
    
    return jsonify({
        "ok": True,
        "content": content,
        "summary": summary,
        "content_html": render_markdown(content),
    })


@api_wiki_bp.route("/suggest-tags", methods=["POST"])
@login_required
def suggest_tags():
    data = request.get_json()
    title = data.get("title", "")
    content = data.get("content", "")[:500]
    
    gemini = get_gemini()
    tags = gemini.suggest_tags(title, content)
    return jsonify({"tags": tags})


@api_wiki_bp.route("/save-generated", methods=["POST"])
@login_required
def save_generated():
    """Sauvegarde un article genere par l'IA."""
    data = request.get_json()
    title = sanitize_text(data.get("title", ""), max_length=200)
    content = data.get("content", "")[:50000]
    category = data.get("category", "")
    tags_str = data.get("tags", "")
    classification = data.get("classification", "confidentiel")
    
    if not title or not content:
        return jsonify({"error": "Titre et contenu requis"}), 400
    
    tags = [t.strip().lower().replace(" ", "-") for t in tags_str.split(",") if t.strip()][:10]
    slug = slugify(title)
    content_html = render_markdown(content)
    summary = truncate_text(content.replace("#", "").replace("*", "").strip(), 200)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    fb = get_firebase()
    article_data = {
        "title": title,
        "title_lower": title.lower(),
        "slug": slug,
        "summary": summary,
        "content": content,
        "content_html": content_html,
        "category": category,
        "tags": tags,
        "sources": [],
        "related_articles": [],
        "author_uid": current_user.uid,
        "author_username": current_user.username or current_user.display_name or "anonyme",
        "generated_by_ai": True,
        "ai_model": "gemini-2.0-flash",
        "status": "published",
        "credibility": "speculatif",
        "classification": classification,
        "views": 0,
        "upvotes": 0,
        "downvotes": 0,
        "comment_count": 0,
        "created_at": now,
        "updated_at": now,
        "featured": False,
        "image_url": "",
    }
    
    new_id = fb.create_article(article_data)
    if new_id:
        return jsonify({"ok": True, "slug": slug})
    return jsonify({"error": "Erreur lors de la sauvegarde"}), 500


@api_wiki_bp.route("/search")
def search_json():
    q = request.args.get("q", "").strip()
    if not q or len(q) < 2:
        return jsonify({"articles": []})
    
    fb = get_firebase()
    articles = fb.search_articles(q, limit=10)
    results = [{
        "title": a.get("title"),
        "slug": a.get("slug"),
        "category": a.get("category"),
        "summary": a.get("summary", "")[:100],
    } for a in articles]
    return jsonify({"articles": results})
