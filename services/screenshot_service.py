import pyautogui
from datetime import datetime
import os

class ScreenshotService:
    @staticmethod
    def take_screenshot(region=None):
        """Take a screenshot of the entire screen or specified region"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        
        if not os.path.exists('static/screenshots'):
            os.makedirs('static/screenshots')
            
        filepath = os.path.join('static/screenshots', filename)
        
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()
            
        screenshot.save(filepath)
        return filepath
