import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "default-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

# Replit-specific configuration
app.config["SERVER_NAME"] = None  # Allow all hostnames
app.config["PREFERRED_URL_SCHEME"] = "https"  # Force HTTPS on Replit
app.config["PROPAGATE_EXCEPTIONS"] = True  # Ensure errors are properly logged
app.config["ENV"] = "production"  # Set to production mode
app.config["TEMPLATES_AUTO_RELOAD"] = False  # Disable template auto-reload
app.config["SESSION_COOKIE_SECURE"] = True  # Force secure cookies
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # Set SameSite policy

# Initialize database
db = SQLAlchemy()
db.init_app(app)

# Ensure required directories exist
os.makedirs("static/screenshots", exist_ok=True)

# Initialize services
try:
    from services.ollama_service import OllamaService
    from services.screenshot_service import ScreenshotService
    from services.automation_service import AutomationService
    
    ollama_service = OllamaService()
    screenshot_service = ScreenshotService()
    automation_service = AutomationService()
except Exception as e:
    logger.error(f"Failed to initialize services: {str(e)}")
    ollama_service = None
    screenshot_service = None
    automation_service = None

# Import routes after db and service initialization
from models import *
from routes import *

# Create tables within app context
with app.app_context():
    try:
        # Drop all tables first to ensure clean slate
        db.drop_all()
        # Create all tables with updated schema
        db.create_all()
        logger.info("Database tables dropped and recreated successfully")
    except Exception as e:
        logger.error(f"Failed to recreate database tables: {str(e)}")
