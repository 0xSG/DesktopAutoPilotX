# System Architecture

## Overview

The AI Computer Automation System is built with a modular architecture that combines AI services, web interfaces, and automation capabilities. This document outlines the system's components and their interactions.

## High-Level Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌────────────────┐
│   Web Interface │     │  Flask API   │     │ Ollama Service │
│  (Browser/HTML) │────▶│   Server     │────▶│ (Vision/Logic) │
└─────────────────┘     └──────────────┘     └────────────────┘
                              │                       │
                              ▼                       ▼
                     ┌──────────────┐     ┌────────────────┐
                     │  PostgreSQL  │     │  Screenshot    │
                     │   Database   │     │   Service      │
                     └──────────────┘     └────────────────┘
                                                  │
                                                  ▼
                                         ┌────────────────┐
                                         │  Automation    │
                                         │   Service      │
                                         └────────────────┘
```

## Components

### 1. Web Interface

- **Technology**: HTML5, Bootstrap, JavaScript
- **Purpose**: User interaction and task monitoring
- **Key Features**:
  - Task submission form
  - Real-time status updates
  - Task history viewing
  - Screenshot display

### 2. Flask API Server

- **Technology**: Python Flask
- **Purpose**: Request handling and service coordination
- **Key Components**:
  - Route handlers
  - Request validation
  - Response formatting
  - Service orchestration

### 3. Ollama Service

- **Technology**: Ollama AI models
- **Purpose**: AI-powered decision making
- **Models**:
  - LLaVA: UI element detection
  - Llama 2: Task reasoning
  - Future: Additional specialized models

### 4. Database

- **Technology**: PostgreSQL
- **Purpose**: Data persistence
- **Schema**:
  ```sql
  -- Tasks table
  CREATE TABLE tasks (
      id SERIAL PRIMARY KEY,
      description TEXT NOT NULL,
      status VARCHAR(20) NOT NULL,
      created_at TIMESTAMP DEFAULT NOW(),
      completed_at TIMESTAMP,
      ai_reasoning TEXT,
      screenshot_path VARCHAR(255),
      result TEXT
  );

  -- Automation logs table
  CREATE TABLE automation_logs (
      id SERIAL PRIMARY KEY,
      task_id INTEGER REFERENCES tasks(id),
      action VARCHAR(100) NOT NULL,
      timestamp TIMESTAMP DEFAULT NOW(),
      success BOOLEAN DEFAULT TRUE,
      error_message TEXT
  );
  ```

### 5. Screenshot Service

- **Technology**: Python PIL
- **Purpose**: Screen capture and image processing
- **Features**:
  - Screen capture
  - Image optimization
  - Storage management

### 6. Automation Service

- **Technology**: Custom Python automation
- **Purpose**: Execute UI interactions
- **Capabilities**:
  - Mouse control
  - Keyboard input
  - Window management

## Data Flow

1. **Task Creation**:
   ```
   User → Web Interface → Flask API → Database
                                  → Ollama Service
                                  → Screenshot Service
   ```

2. **Task Execution**:
   ```
   Ollama Service → Screenshot Service → Automation Service
                                     → Database (logs)
   ```

3. **Status Updates**:
   ```
   Database → Flask API → Web Interface → User
   ```

## Security Considerations

1. **Input Validation**:
   - All user inputs sanitized
   - Request size limits
   - File type restrictions

2. **Error Handling**:
   - Graceful error recovery
   - Detailed logging
   - User-friendly messages

3. **Future Enhancements**:
   - Authentication
   - Rate limiting
   - API keys

## Scalability

The system is designed for horizontal scaling:

1. **Database**: PostgreSQL with connection pooling
2. **Services**: Stateless design for easy replication
3. **File Storage**: Prepared for cloud storage integration

## Monitoring

Current monitoring points:

1. Application logs
2. Database metrics
3. Service health checks
4. Task execution status

Future monitoring additions:

1. Prometheus metrics
2. Grafana dashboards
3. Alert system
4. Performance tracking
