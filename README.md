<div align="center">

# DesktopAutoPilotX

🤖 Open-source AI automation for everyone, powered by local LLMs
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/0xSG/DesktopAutoPilotX)
[![GitHub stars](https://img.shields.io/github/stars/0xSG/DesktopAutoPilotX?style=social)](https://github.com/0xSG/DesktopAutoPilotX/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Discord](https://img.shields.io/discord/1302574295435841567)](https://discord.gg/kvnShnxt)
[![Twitter Follow](https://img.shields.io/twitter/follow/sooryagangaraj?style=social)](https://x.com/sooryagangaraj)

[Installation](#installation) • [Documentation](docs/) • [Examples](examples/) • [Contributing](CONTRIBUTING.md) • [Community](#community)

## 📸 Screenshots

<p align="center">
  <img src="assets/settings-screen.png" alt="Settings Screen" width="800"/>
  <em>AI Model Configuration and Theme Settings</em>
</p>

<p align="center">
  <img src="assets/task-history.png" alt="Task History" width="800"/>
  <em>Task History Overview</em>
</p>

<p align="center">
  <img src="assets/new-task.png" alt="New Automation Task" width="800"/>
  <em>New Automation Task Creation Interface</em>
</p>

</div>

## 🌟 What is DesktopAutoPilotX?

DesktopAutoPilotX is your computer's new co-pilot – a free, open-source AI automation system that sees, understands, and interacts with your desktop just like you do. No cloud services, no API keys, just pure local AI power.

### ✨ Key Features

- 🧠 **True AI Vision**: Powered by LLaVA and Llama 2 for intelligent screen understanding
- 🎯 **Context-Aware**: Finds and interacts with UI elements naturally, no pixel coordinates needed
- 📊 **Transparent**: Real-time visualization and detailed logging of all actions
- 🛡️ **Secure**: Runs 100% locally - your data never leaves your machine
- 🔄 **Self-Learning**: Gets smarter with each task it handles

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL
- Ollama with LLaVA and Llama 2 models
- Git
- Poetry (Python package manager)

### Installation

```bash
# Clone the repo
git clone https://github.com/0xSG/DesktopAutoPilotX.git
cd DesktopAutoPilotX

# Install dependencies using Poetry
poetry install

# Activate the virtual environment
poetry shell

# Set up environment variables
cp .env.example .env
# Edit .env with your settings

# Initialize database
flask db upgrade

# Launch
python main.py
```

### Development Setup

```bash
# Install development dependencies
poetry install --with dev,test,docs

# Install pre-commit hooks
poetry run pre-commit install

# Run tests
poetry run pytest

# Run type checking
poetry run mypy .

# Format code
poetry run black .
poetry run ruff .
```

### Using Docker

```bash
# Build and run using Docker Compose
docker compose up -d
```

## 📦 Project Structure

```
DesktopAutoPilotX/
├── src/
│   └── desktop_autopilot/
│       ├── core/           # Core automation engine
│       ├── models/         # AI model integrations
│       ├── vision/         # Screen analysis components
│       └── utils/          # Utility functions
├── tests/                  # Test suite
├── docs/                   # Documentation
├── examples/               # Example scripts
├── docker/                 # Docker configurations
├── pyproject.toml         # Project dependencies and config
└── README.md              # You are here
```

## 🎮 Usage Examples

```python
from desktop_autopilot import AutoPilot

pilot = AutoPilot()

# Example 1: Web Automation
@pilot.task
async def search_github():
    """Search for a repository on GitHub."""
    await pilot.browser.open("https://github.com")
    await pilot.keyboard.type("DesktopAutoPilotX")
    await pilot.keyboard.press("Enter")
    
# Example 2: Desktop App Automation
@pilot.task
async def process_images():
    """Batch process images in a folder."""
    await pilot.app.launch("PhotoEditor")
    await pilot.folder.select("~/Pictures/batch")
    await pilot.vision.wait_for("Process All")
    await pilot.mouse.click()
```

More examples in our [cookbook](docs/cookbook.md) 📚

## 🛠️ Configuration

### AI Provider Setup

Configure your AI providers in `config/providers.toml`:

```toml
[ollama]
base_url = "http://localhost:11434"
models = ["llava", "llama2"]
timeout = 30

[local]
model_path = "/path/to/models"
device = "cuda"

[api]
base_url = "https://api.example.com/v1"
timeout = 10
```

### Environment Variables

```bash
# Required
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
FLASK_SECRET_KEY=your-secret-key

# Optional
LOG_LEVEL=INFO
OLLAMA_BASE_URL=http://localhost:11434
```

## 👥 Community & Support

[![Discord](https://img.shields.io/discord/YOUR_DISCORD_ID)](https://discord.gg/kvnShnxt)
[![Twitter Follow](https://img.shields.io/twitter/follow/sooryagangaraj?style=social)](https://x.com/sooryagangaraj)

- 💬 [Join our Discord](https://discord.gg/kvnShnxt)
- 🐦 [Follow on X (Twitter)](https://x.com/sooryagangaraj)
- 📝 [Read our blog](https://thedevstories.com)

## 🤝 Contributing

We believe great software is built together! Check out our [Contributing Guidelines](CONTRIBUTING.md) to get started.

### Development Workflow

1. Fork the repository
2. Create a new branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `poetry run pytest`
5. Format code: `poetry run black . && poetry run ruff .`
6. Commit: `git commit -m "feat: add new feature"`
7. Push: `git push origin feature-name`
8. Open a Pull Request

## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=0xSG/DesktopAutoPilotX&type=Date)](https://star-history.com/#0xSG/DesktopAutoPilotX)

## 📜 License

DesktopAutoPilotX is MIT licensed, as found in the [LICENSE](LICENSE) file.

---

<div align="center">
Made with ❤️ by the DesktopAutoPilotX Community

[⬆ back to top](#desktopautopilotx)
</div>
