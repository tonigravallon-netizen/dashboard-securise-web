"""WSGI entry point for Render/Gunicorn deployment."""
from web import create_app

app = create_app()
