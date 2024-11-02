# Contributing to AI Computer Automation System

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Code Style Guidelines

### Python

1. Follow PEP 8 style guide
2. Use type hints for function arguments and return values
3. Write docstrings for all functions and classes
4. Keep functions focused and single-purpose
5. Use meaningful variable names
6. Comment complex logic

Example:
```python
from typing import Dict, Any

def process_task(task_description: str) -> Dict[str, Any]:
    """
    Process an automation task with AI reasoning.
    
    Args:
        task_description: Natural language description of the task
        
    Returns:
        Dictionary containing task results and analysis
    """
    # Implementation here
```

### JavaScript

1. Use ES6+ features
2. Follow Airbnb JavaScript Style Guide
3. Use async/await for asynchronous operations
4. Keep event handlers clean and focused
5. Use meaningful variable and function names

Example:
```javascript
async function submitTask(description) {
    try {
        const response = await fetch('/task/create', {
            method: 'POST',
            body: new FormData({ description })
        });
        return await response.json();
    } catch (error) {
        console.error('Task submission failed:', error);
        throw error;
    }
}
```

### HTML/CSS

1. Use semantic HTML5 elements
2. Follow Bootstrap conventions
3. Keep CSS classes meaningful and reusable
4. Use proper indentation
5. Maintain responsive design principles

Example:
```html
<section class="task-container">
    <div class="card">
        <div class="card-header">
            <h5 class="card-title">New Task</h5>
        </div>
        <div class="card-body">
            <!-- Form content -->
        </div>
    </div>
</section>
```

## Development Setup

1. Install Python 3.11:
```bash
pyenv install 3.11
pyenv global 3.11
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Ollama:
```bash
curl https://ollama.ai/install.sh | sh
```

4. Pull required models:
```bash
ollama pull llava
ollama pull llama2
```

5. Set up PostgreSQL database:
```bash
createdb automation_system
```

6. Set environment variables:
```bash
export FLASK_SECRET_KEY=development_key
export DATABASE_URL=postgresql://localhost/automation_system
```

7. Initialize database:
```bash
flask db upgrade
```

## Pull Request Process

1. Update the README.md with details of changes to the interface
2. Update the documentation with any new dependencies or features
3. Increase the version numbers in any examples files and the README.md
4. The PR will be merged once you have the sign-off of at least one maintainer

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issue tracker]

We use GitHub issues to track public bugs. Report a bug by [opening a new issue]().

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## License

By contributing, you agree that your contributions will be licensed under its MIT License.

## References

This document was adapted from the open-source contribution guidelines for [Facebook's Draft](https://github.com/facebook/draft-js/blob/a9316a723f9e918afde44dea68b5f9f39b7d9b00/CONTRIBUTING.md).
