# AI Computer Automation System

A powerful automation system that integrates local Ollama AI for computer vision and reasoning capabilities. This system allows automated UI interaction with intelligent decision-making powered by LLaVA for vision tasks and Llama 2 for reasoning.

## Features

- 🤖 **AI-Powered Automation**: Uses Ollama's LLaVA for UI element detection and Llama 2 for task reasoning
- 📸 **Screenshot Analysis**: Captures and analyzes screen content for intelligent interaction
- 🎯 **Precise UI Interaction**: Automatically identifies and interacts with UI elements
- 📊 **Task History**: Maintains detailed logs of automation tasks and their outcomes
- 🔍 **Real-time Monitoring**: Track task progress and view screenshots in real-time
- 🧠 **Intelligent Planning**: Break down complex tasks into actionable steps with AI reasoning

## Prerequisites

Before installing the system, ensure you have:

1. Python 3.11 or higher
2. PostgreSQL database
3. Ollama installed with LLaVA and Llama 2 models
4. Git (for development)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-automation-system.git
cd ai-automation-system
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (see .env.example for all options):
```bash
FLASK_SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://username:password@host:port/dbname
```

4. Initialize the database:
```bash
flask db upgrade
```

5. Start the application:
```bash
python main.py
```

The application will be available at `http://localhost:5000`

## Model Configuration

### Supported Model Providers

1. **Ollama Provider**
   - Local Ollama instance
   - Supports LLaVA and Llama 2 models
   - Configurable parameters per model

2. **Local Model Provider**
   - Run models directly on the machine
   - Support for custom model formats
   - Configurable model paths and parameters

3. **API Provider**
   - Connect to external AI APIs
   - Configurable endpoints and authentication
   - Support for various API formats

### Adding Custom Models

1. Create a JSON configuration file in `config/models/`:

```json
{
    "provider": "ollama|local|api",
    "model": "model_name",
    "temperature": 0.7,
    "description": "Model description",
    "capabilities": ["text", "vision"],
    
    // Provider-specific configuration
    "base_url": "http://localhost:11434",  // For Ollama
    "model_path": "/path/to/model",        // For local models
    "api_url": "https://api.example.com",  // For API provider
    "api_key": "your_api_key"              // For API provider
}
```

2. Model will be automatically loaded on application start

3. Access the model through the registry:
```python
from services.model_registry import ModelRegistry

registry = ModelRegistry()
model = registry.get_model('your_model_name')
result = model.generate("Your prompt")
```

### Example Configurations

1. **Ollama LLaVA Configuration**
```json
{
    "provider": "ollama",
    "base_url": "http://localhost:11434",
    "model": "llava",
    "temperature": 0.1,
    "num_predict": 1000,
    "description": "Vision-language model for UI element detection",
    "capabilities": ["vision", "text"]
}
```

2. **Local Model Configuration**
```json
{
    "provider": "local",
    "model_path": "/path/to/model",
    "model": "custom_model",
    "temperature": 0.5,
    "description": "Custom local model",
    "capabilities": ["text"]
}
```

3. **API Model Configuration**
```json
{
    "provider": "api",
    "api_url": "https://api.example.com/v1/generate",
    "api_key": "your_api_key",
    "model": "gpt-4",
    "temperature": 0.7,
    "description": "External API model",
    "capabilities": ["text"]
}
```

## Usage

[Rest of the README content remains the same...]
