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
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

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
with app.app_context():
    from models import *
    from routes import *
    try:
        db.create_all()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")
