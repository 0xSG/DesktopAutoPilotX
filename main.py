import os
import logging
from app import app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        logger.info("Starting Flask server...")
        
        # Get port from Replit environment variables
        port = int(os.environ.get('PORT', 5000))
        host = '0.0.0.0'  # Bind to all network interfaces
        
        logger.info(f"Starting server on {host}:{port}")
        
        # Start Flask with production configuration
        app.run(
            host=host,
            port=port,
            debug=False,  # Disable debug mode for production
            use_reloader=False,  # Disable reloader to prevent duplicate processes
            threaded=True,  # Enable threading for better request handling
            load_dotenv=False  # Disable dotenv loading as Replit handles env vars
        )
    except Exception as e:
        logger.error(f"Server failed to start: {str(e)}")
        raise
