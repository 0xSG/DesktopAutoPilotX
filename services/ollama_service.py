import requests
from PIL import Image
import io
import base64
import logging
from typing import Optional, Dict, Any

class OllamaService:
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.logger = logging.getLogger(__name__)
        
    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """
        Use LLaVA to analyze UI elements in screenshots with precise detection
        """
        try:
            # Convert image to base64
            with Image.open(image_path) as img:
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # Craft a detailed prompt for UI element detection
            prompt = """
            Analyze this screenshot and identify UI elements with their exact locations. For each element:
            1. Describe its type (button, input field, dropdown, etc.)
            2. Specify its position (coordinates or relative position)
            3. Note any text content or labels
            4. Describe its visual state (enabled/disabled, selected, etc.)
            5. Identify any interactive elements nearby
            
            Format the response as a structured analysis.
            """
            
            payload = {
                "model": "llava",
                "prompt": prompt,
                "images": [img_str],
                "stream": False,
                "options": {
                    "temperature": 0.1,  # Lower temperature for more precise outputs
                    "num_predict": 1000  # Allow for detailed response
                }
            }
            
            response = requests.post(f"{self.base_url}/api/generate", json=payload)
            response.raise_for_status()
            
            analysis = response.json().get("response", "")
            self.logger.info("Successfully analyzed image with LLaVA")
            
            return {
                "success": True,
                "analysis": analysis,
                "elements": self._parse_ui_elements(analysis)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing image: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "elements": []
            }

    def get_reasoning(self, prompt: str, context: str = "") -> Dict[str, Any]:
        """
        Use Llama 3.2 for advanced task reasoning and planning
        """
        try:
            # Craft a detailed system prompt for better reasoning
            system_prompt = """
            You are an AI automation assistant specialized in UI interaction planning.
            Analyze tasks and break them down into specific, actionable steps.
            For each step:
            1. Identify the UI element to interact with
            2. Specify the type of interaction needed
            3. Determine any preconditions
            4. Predict expected outcomes
            5. Plan for potential error cases
            """
            
            # Combine prompts with context
            full_prompt = f"""
            {system_prompt}
            
            Context: {context}
            
            Task to analyze: {prompt}
            
            Provide detailed reasoning and steps:
            """
            
            payload = {
                "model": "llama2",
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,  # Balance between creativity and precision
                    "num_predict": 2000,  # Allow for detailed planning
                    "top_p": 0.9
                }
            }
            
            response = requests.post(f"{self.base_url}/api/generate", json=payload)
            response.raise_for_status()
            
            reasoning = response.json().get("response", "")
            self.logger.info("Successfully generated task reasoning")
            
            return {
                "success": True,
                "reasoning": reasoning,
                "steps": self._parse_reasoning_steps(reasoning)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting reasoning: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "steps": []
            }
    
    def _parse_ui_elements(self, analysis: str) -> list:
        """
        Parse the LLaVA analysis into structured UI element data
        """
        # TODO: Implement more sophisticated parsing
        # For now, return raw analysis as a single element
        return [{
            "type": "raw_analysis",
            "content": analysis
        }]
    
    def _parse_reasoning_steps(self, reasoning: str) -> list:
        """
        Parse the reasoning output into structured steps
        """
        # TODO: Implement more sophisticated parsing
        # For now, return raw reasoning as a single step
        return [{
            "type": "reasoning",
            "content": reasoning
        }]
