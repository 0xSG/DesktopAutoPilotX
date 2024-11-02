from typing import Dict, Any, Optional
import json
import os
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class ModelProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        pass

class OllamaProvider(ModelProvider):
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        import requests
        self._session = requests.Session()

    def generate(self, prompt: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        try:
            payload = {
                "prompt": prompt,
                "stream": False,
                **(options or {})
            }
            response = self._session.post(f"{self.base_url}/api/generate", json=payload)
            response.raise_for_status()
            return {"success": True, "response": response.json().get("response", "")}
        except Exception as e:
            logger.error(f"Ollama generation error: {str(e)}")
            return {"success": False, "error": str(e)}

class LocalModelProvider(ModelProvider):
    def __init__(self, model_path: str):
        self.model_path = model_path
        # Initialize local model (placeholder for future implementation)

    def generate(self, prompt: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        # Placeholder for local model implementation
        return {"success": False, "error": "Local model generation not implemented"}

class APIModelProvider(ModelProvider):
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        import requests
        self._session = requests.Session()
        self._session.headers.update({"Authorization": f"Bearer {api_key}"})

    def generate(self, prompt: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        try:
            payload = {
                "prompt": prompt,
                **(options or {})
            }
            response = self._session.post(self.api_url, json=payload)
            response.raise_for_status()
            return {"success": True, "response": response.json()}
        except Exception as e:
            logger.error(f"API generation error: {str(e)}")
            return {"success": False, "error": str(e)}

class ModelRegistry:
    def __init__(self):
        self.models: Dict[str, Dict[str, Any]] = {}
        self.providers: Dict[str, ModelProvider] = {}
        self.load_models()

    def load_models(self) -> None:
        """Load model configurations from the config directory"""
        config_dir = "config/models"
        os.makedirs(config_dir, exist_ok=True)
        
        try:
            for filename in os.listdir(config_dir):
                if filename.endswith('.json'):
                    model_name = filename[:-5]
                    with open(os.path.join(config_dir, filename)) as f:
                        config = json.load(f)
                        self.register_model(model_name, config)
        except Exception as e:
            logger.error(f"Error loading model configurations: {str(e)}")

    def register_model(self, name: str, config: Dict[str, Any]) -> None:
        """Register a model with its configuration"""
        self.models[name] = config
        provider_type = config.get('provider', 'ollama')
        
        try:
            if provider_type == 'ollama':
                self.providers[name] = OllamaProvider(config.get('base_url'))
            elif provider_type == 'local':
                self.providers[name] = LocalModelProvider(config.get('model_path'))
            elif provider_type == 'api':
                self.providers[name] = APIModelProvider(
                    config.get('api_url'),
                    config.get('api_key')
                )
            else:
                logger.error(f"Unknown provider type: {provider_type}")
        except Exception as e:
            logger.error(f"Error registering model {name}: {str(e)}")

    def get_model(self, name: str) -> Optional[ModelProvider]:
        """Get a model provider by name"""
        return self.providers.get(name)

    def list_models(self) -> Dict[str, Dict[str, Any]]:
        """List all registered models and their configurations"""
        return self.models
