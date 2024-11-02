# Configuration Guide

## Environment Variables

### Required Variables

```bash
# Flask Configuration
FLASK_SECRET_KEY=your_secret_key        # Required for session management
FLASK_ENV=production                    # production/development

# Database Configuration
DATABASE_URL=postgresql://user:pass@host:port/dbname
PGUSER=your_db_user
PGPASSWORD=your_db_password
PGDATABASE=your_db_name
PGHOST=your_db_host
PGPORT=5432

# Server Configuration
PORT=5000                              # Web server port
HOST=0.0.0.0                           # Listen on all interfaces
```

### Optional Variables

```bash
# Logging Configuration
LOG_LEVEL=INFO                         # DEBUG/INFO/WARNING/ERROR
LOG_FILE=/path/to/log/file            # Default: stdout

# Service Configuration
SCREENSHOT_DIR=static/screenshots      # Screenshot storage location
MAX_TASK_RUNTIME=3600                 # Maximum task runtime in seconds
```

## Database Setup

1. Create PostgreSQL database:
```sql
CREATE DATABASE automation_system;
```

2. Initialize schema:
```bash
flask db upgrade
```

3. Optional: Create read-only user:
```sql
CREATE USER readonly WITH PASSWORD 'password';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
```

## Ollama Configuration

1. Install Ollama:
```bash
curl https://ollama.ai/install.sh | sh
```

2. Pull required models:
```bash
ollama pull llava
ollama pull llama2
```

3. Model configuration files:

`llava.json`:
```json
{
    "model": "llava",
    "temperature": 0.1,
    "num_predict": 1000
}
```

`llama2.json`:
```json
{
    "model": "llama2",
    "temperature": 0.7,
    "num_predict": 2000,
    "top_p": 0.9
}
```

## Logging Configuration

Default logging configuration in `logging.conf`:

```ini
[loggers]
keys=root,automation

[handlers]
keys=console,file

[formatters]
keys=standard

[logger_root]
level=INFO
handlers=console

[logger_automation]
level=INFO
handlers=console,file
qualname=automation
propagate=0

[handler_console]
class=StreamHandler
level=INFO
formatter=standard
args=(sys.stdout,)

[handler_file]
class=FileHandler
level=INFO
formatter=standard
args=('automation.log', 'a')

[formatter_standard]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S
```

## Development Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up pre-commit hooks:
```bash
pre-commit install
```

3. Configure development environment:
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
```

## Production Deployment

1. Use production WSGI server:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

2. Configure nginx (optional):
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. Enable SSL (recommended):
```bash
certbot --nginx -d your_domain.com
```

## Maintenance

1. Database backup:
```bash
pg_dump -U your_user automation_system > backup.sql
```

2. Log rotation:
```bash
# /etc/logrotate.d/automation
/path/to/automation.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 640 www-data www-data
}
```

3. Screenshot cleanup:
```bash
find static/screenshots -type f -mtime +30 -delete
```

## Troubleshooting

1. Check service health:
```bash
curl http://localhost:5000/health
```

2. View logs:
```bash
tail -f automation.log
```

3. Common issues:
   - Database connection: Check credentials and network
   - Ollama service: Ensure models are downloaded
   - Permission issues: Check file/directory permissions
