"""Blueprint wiki - Routes principales du wiki."""
from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from .helpers import get_firebase, firebase_required, render_markdown, sanitize_text, truncate_text, slugify, format_date_fr
from .gemini_service import get_gemini

wiki_bp = Blueprint("wiki", __name__)


@wiki_bp.route("/")
@wiki_bp.route("/wiki")
def home():
    fb = get_firebase()
    # Init categories si premiere visite
    if fb.is_authenticated():
        fb.init_categories()
    
    featured = fb.get_featured_articles(limit=6) if fb.is_authenticated() else []
    recent = fb.list_articles(status="published", limit=10) if fb.is_authenticated() else []
    
    return render_template("wiki/home.html", featured=featured, recent=recent)


@wiki_bp.route("/wiki/article/<slug>")
def article(slug):
    fb = get_firebase()
    art = fb.get_article_by_slug(slug)
    if not art:
        flash("Article introuvable.", "error")
        return redirect(url_for("wiki.home"))
    
    # Increment views
    article_id = art.get("__id", "")
    views = art.get("views", 0)
    if isinstance(views, str):
        views = int(views)
    fb.increment_views(article_id, views)
    art["views"] = views + 1
    
    # User vote
    user_vote = None
    if current_user.is_authenticated:
        user_vote = fb.get_user_vote(article_id, current_user.uid)
    
    # Comments
    comments = fb.get_comments(article_id, limit=50)
    
    return render_template("wiki/article.html", article=art, user_vote=user_vote, comments=comments,
                           format_date=format_date_fr)


@wiki_bp.route("/wiki/category/<slug>")
def category(slug):
    fb = get_firebase()
    articles = fb.get_articles_by_category(slug, limit=30)
    
    category_names = {
        "technologie": "Technologie & Surveillance",
        "histoire": "Histoire Secrete",
        "politique": "Politique & Pouvoir",
        "espace": "Espace & Extraterrestres",
        "sante": "Sante & Big Pharma",
        "finance": "Finance & Economie",
        "occultisme": "Occultisme & Societes Secretes",
        "science": "Science Cachee",
    }
    cat_name = category_names.get(slug, slug.capitalize())
    
    return render_template("wiki/category.html", articles=articles, category_slug=slug, category_name=cat_name)


@wiki_bp.route("/wiki/tag/<tag>")
def tag(tag):
    fb = get_firebase()
    articles = fb.get_articles_by_tag(tag, limit=30)
    return render_template("wiki/category.html", articles=articles, category_slug=tag, category_name=f"Tag: {tag}")


@wiki_bp.route("/wiki/search")
def search():
    q = request.args.get("q", "").strip()
    articles = []
    if q:
        fb = get_firebase()
        articles = fb.search_articles(q, limit=30)
    return render_template("wiki/search.html", articles=articles, query=q)


@wiki_bp.route("/wiki/editor", methods=["GET", "POST"])
@login_required
def editor():
    if request.method == "POST":
        return save_article()
    
    # Check if editing existing article
    slug = request.args.get("edit", "")
    article = None
    if slug:
        fb = get_firebase()
        article = fb.get_article_by_slug(slug)
        if article and article.get("author_uid") != current_user.uid:
            flash("Vous ne pouvez modifier que vos propres articles.", "error")
            return redirect(url_for("wiki.article", slug=slug))
    
    return render_template("wiki/editor.html", article=article)


def save_article():
    """Sauvegarde un article (nouveau ou modifie)."""
    fb = get_firebase()
    
    title = sanitize_text(request.form.get("title", ""), max_length=200)
    content = request.form.get("content", "")[:50000]  # Max 50k chars
    category = sanitize_text(request.form.get("category", ""), max_length=50)
    tags_str = sanitize_text(request.form.get("tags", ""), max_length=500)
    classification = request.form.get("classification", "confidentiel")
    credibility = request.form.get("credibility", "speculatif")
    status = request.form.get("status", "published")
    article_id = request.form.get("article_id", "")
    
    if not title or not content:
        flash("Le titre et le contenu sont obligatoires.", "error")
        return redirect(url_for("wiki.editor"))
    
    # Process tags
    tags = [t.strip().lower().replace(" ", "-") for t in tags_str.split(",") if t.strip()]
    tags = tags[:10]  # Max 10 tags
    
    # Generate slug
    slug = slugify(title)
    
    # Render HTML
    content_html = render_markdown(content)
    summary = truncate_text(content.replace("#", "").replace("*", "").strip(), 200)
    
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    if article_id:
        # Update existing
        fb.update_article(article_id, {
            "title": title,
            "title_lower": title.lower(),
            "slug": slug,
            "summary": summary,
            "content": content,
            "content_html": content_html,
            "category": category,
            "tags": tags,
            "classification": classification,
            "credibility": credibility,
            "status": status,
            "updated_at": now,
        })
        flash("Article mis a jour !", "success")
    else:
        # Create new
        data = {
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
            "generated_by_ai": False,
            "ai_model": "",
            "status": status,
            "credibility": credibility,
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
        new_id = fb.create_article(data)
        if new_id:
            flash("Article publie !", "success")
        else:
            flash("Erreur lors de la creation.", "error")
            return redirect(url_for("wiki.editor"))
    
    return redirect(url_for("wiki.article", slug=slug))


@wiki_bp.route("/wiki/generate", methods=["GET"])
@login_required
def generate():
    return render_template("wiki/generate.html")


@wiki_bp.route("/wiki/my-articles")
@login_required
def my_articles():
    fb = get_firebase()
    articles = fb.get_articles_by_author(current_user.uid, limit=50)
    return render_template("wiki/category.html", articles=articles, category_slug="mes-articles",
                           category_name="Mes articles")
