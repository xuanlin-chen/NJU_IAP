# Database models and interaction
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy without binding to app yet
db = SQLAlchemy()

def init_app(app):
    """Initialize the database with the app"""
    db.init_app(app)