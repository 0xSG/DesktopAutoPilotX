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

3. Set up environment variables:
```bash
FLASK_SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://username:password@host:port/dbname
```

4. Initialize the database:
```bash
flask db upgrade
```

5. Start Ollama service with required models:
```bash
ollama run llava  # In one terminal
ollama run llama2 # In another terminal
```

6. Start the application:
```bash
python main.py
```

The application will be available at `http://localhost:5000`

## Usage

### 1. Creating an Automation Task

1. Navigate to the home page
2. Enter your task description in natural language
3. Click "Start Task" to begin automation
4. Monitor progress in real-time

Example task descriptions:
- "Open the settings menu and enable dark mode"
- "Find and click the submit button on the form"
- "Type 'Hello World' into the active text field"

### 2. Viewing Task History

1. Click on "Task History" in the navigation
2. View all past automation tasks
3. Check screenshots, AI reasoning, and execution logs

## API Documentation

### Endpoints

#### `POST /task/create`
Create a new automation task.

Request body:
```json
{
    "description": "string"
}
```

Response:
```json
{
    "task_id": "integer"
}
```

#### `GET /task/{task_id}/status`
Get task execution status.

Response:
```json
{
    "status": "string",
    "message": "string",
    "screenshot": "string",
    "ai_analysis": "object"
}
```

#### `GET /history`
Get list of all tasks.

Response: HTML page with task history.

## Architecture

The system consists of several key components:

1. **Flask Web Server**: Handles HTTP requests and serves the web interface
2. **Ollama Integration**: 
   - LLaVA for vision tasks
   - Llama 2 for reasoning
3. **Services**:
   - Screenshot Service
   - Automation Service
   - Ollama Service
4. **PostgreSQL Database**: Stores task data and execution logs

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on contributing to this project.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
