import requests
from PIL import Image
import io
import base64

class OllamaService:
    def __init__(self):
        self.base_url = "http://localhost:11434"
        
    def analyze_image(self, image_path):
        try:
            with Image.open(image_path) as img:
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
            
            payload = {
                "model": "llava",
                "prompt": "What do you see in this image? Describe any UI elements and their locations.",
                "images": [img_str]
            }
            
            response = requests.post(f"{self.base_url}/api/generate", json=payload)
            return response.json()["response"]
        except Exception as e:
            return f"Error analyzing image: {str(e)}"

    def get_reasoning(self, prompt, context=""):
        try:
            payload = {
                "model": "llama2",
                "prompt": f"Context: {context}\n\nTask: {prompt}\n\nProvide reasoning and next steps:",
            }
            
            response = requests.post(f"{self.base_url}/api/generate", json=payload)
            return response.json()["response"]
        except Exception as e:
            return f"Error getting reasoning: {str(e)}"
