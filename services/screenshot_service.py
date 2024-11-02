import os
from datetime import datetime
from PIL import Image

class ScreenshotService:
    def __init__(self, screenshot_dir="static/screenshots"):
        self.screenshot_dir = screenshot_dir
        os.makedirs(screenshot_dir, exist_ok=True)
        
    def take_screenshot(self):
        """
        Mock screenshot functionality that creates a blank image with timestamp
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            
            # Create a small blank image
            image = Image.new('RGB', (800, 600), color='black')
            # Add timestamp text
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(image)
            draw.text((10, 10), f"Mock Screenshot: {timestamp}", fill='white')
            
            # Save the image
            image.save(filepath, optimize=True, quality=85)
            
            return filepath
        except Exception as e:
            raise Exception(f"Screenshot failed: {str(e)}")
