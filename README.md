# DesktopAutoPilotX: 

Looking for a free, open-source alternative to Claude's "Computer Use"? DesktopAutoPilotX brings the power of local AI automation to your computer, without the need for API keys or cloud services.

## Why This Matters

Today's businesses are looking for ways to automate repetitive tasks, but most solutions either require expensive subscriptions or lack true AI capabilities. DesktopAutoPilotX bridges this gap by providing a local, intelligent automation system that's both powerful and accessible. Think of it as your personal automation assistant that can see, understand, and interact with your computer just like a human would.

## What Makes It Special?

- 🤖 **AI That Understands Your Screen**: Using LLaVA for vision and Llama 2 for reasoning, it's like having a smart assistant who can actually see your screen
- 🎯 **Precise & Intelligent**: No more pixel-perfect coordinates - it finds and interacts with UI elements just like you would
- 📊 **Never Misses a Beat**: Keeps detailed logs of what it did and why, so you're always in the loop
- 🔍 **Watch It Work**: See exactly what it's doing in real-time, perfect for building trust in automation
- 🧠 **Thinks Before It Acts**: Breaks down complex tasks into simple steps, just like a human would

## Getting Started Is Easy

First, make sure you have these basics covered:
- Python 3.11+
- PostgreSQL
- Ollama with LLaVA and Llama 2 models
- Git (for joining our community)

### Quick Setup

1. Grab the code:
```bash
git clone https://github.com/yourusername/ai-automation-system.git
cd ai-automation-system
```

2. Install what you need:
```bash
pip install -r requirements.txt
```

3. Set up your environment (check .env.example for all options):
```bash
FLASK_SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://username:password@host:port/dbname
```

4. Prepare the database:
```bash
flask db upgrade
```

5. Launch it:
```bash
python main.py
```

Visit `http://localhost:5000` and you're ready to go!

## Making It Your Own

### Working with Models

We support three ways to bring AI into your automation:

1. **Ollama Provider**: Perfect for running everything locally
2. **Local Model Provider**: Want to use your own models? No problem!
3. **API Provider**: Need to connect to external AI services? We've got you covered

### Adding Your Own Models

Creating a new model configuration is straightforward. Just add a JSON file in `config/models/`:

```json
{
    "provider": "ollama|local|api",
    "model": "model_name",
    "temperature": 0.7,
    "description": "What makes your model special",
    "capabilities": ["text", "vision"]
    // Provider-specific settings here
}
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

## Join Our Community

DesktopAutoPilotX is more than just code - it's a community of people who believe in making computers work better for humans. Whether you're a seasoned developer or just getting started with automation, we'd love to have you aboard.

### How You Can Contribute

1. **Try it out**: Use it, break it, tell us what you think
2. **Share your ideas**: Open issues for features you'd love to see
3. **Show us your code**: Pull requests are always welcome
4. **Spread the word**: If you like what we're building, let others know!

Remember, every great tool started with a community of passionate people. Your contribution, no matter how small, helps make DesktopAutoPilotX better for everyone.

### Key Areas We're Looking For Help

- 🎨 UI/UX improvements
- 🧪 Testing and bug reporting
- 📚 Documentation
- 🔧 New feature development
- 🌍 Internationalization

Ready to dive in? Check out our [Contribution Guidelines](CONTRIBUTING.md) to get started!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
