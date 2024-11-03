from typing import Dict, Any, Optional
import json
import os
import logging
from litellm import completion

logger = logging.getLogger(__name__)

class ModelRegistry:
    def __init__(self):
        self.models: Dict[str, Dict[str, Any]] = {}
        self._selected_models = {
            'vision': None,
            'reasoning': None
        }
        self.load_models()

    def load_models(self) -> None:
        """Load model configurations from the config directory"""
        config_dir = "config/models"
        os.makedirs(config_dir, exist_ok=True)
        
        try:
            # Load local environment variables if .env.local exists
            env_local = os.path.join(os.getcwd(), '.env.local')
            if os.path.exists(env_local):
                with open(env_local) as f:
                    for line in f:
                        if line.strip() and not line.startswith('#'):
                            key, value = line.strip().split('=', 1)
                            os.environ[key] = value

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
        logger.info(f"Registered model: {name} with config: {config}")

    def get_model(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a model configuration by name"""
        return self.models.get(name)

    def list_models(self) -> Dict[str, Dict[str, Any]]:
        """List all registered models and their configurations"""
        return self.models

    @property
    def selected_models(self) -> Dict[str, str]:
        """Get currently selected models"""
        return self._selected_models

    @selected_models.setter
    def selected_models(self, models: Dict[str, str]) -> None:
        """Set selected models for vision and reasoning tasks"""
        if 'vision' in models:
            self._selected_models['vision'] = models['vision']
        if 'reasoning' in models:
            self._selected_models['reasoning'] = models['reasoning']
        logger.info(f"Updated selected models: {self._selected_models}")

    def generate(self, model_name: str, prompt: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate completion using litellm"""
        try:
            model_config = self.get_model(model_name)
            if not model_config:
                raise ValueError(f"Model {model_name} not found")

            # Merge model config with additional options
            model_options = {
                "model": model_config["model"],
                "temperature": model_config.get("temperature", 0.7),
                **model_config.get("additional_params", {}),
                **(options or {})
            }

            # Add API key if present in environment
            api_key = os.getenv(f"{model_name.upper()}_API_KEY")
            if api_key:
                model_options["api_key"] = api_key

            response = completion(
                messages=[{"role": "user", "content": prompt}],
                **model_options
            )

            return {
                "success": True,
                "response": response.choices[0].message.content if response.choices else "",
                "model": model_name,
            }
        except Exception as e:
            logger.error(f"Generation error for model {model_name}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "model": model_name,
            }
