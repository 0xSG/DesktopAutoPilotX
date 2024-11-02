import pyautogui
import time

class AutomationService:
    @staticmethod
    def move_mouse(x, y):
        """Move mouse to specified coordinates"""
        pyautogui.moveTo(x, y)
    
    @staticmethod
    def click(x=None, y=None):
        """Click at current position or specified coordinates"""
        if x is not None and y is not None:
            pyautogui.click(x, y)
        else:
            pyautogui.click()
    
    @staticmethod
    def type_text(text):
        """Type the specified text"""
        pyautogui.write(text)
    
    @staticmethod
    def press_key(key):
        """Press a specific key"""
        pyautogui.press(key)

    @staticmethod
    def wait(seconds):
        """Wait for specified number of seconds"""
        time.sleep(seconds)
