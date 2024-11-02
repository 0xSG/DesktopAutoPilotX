# API Documentation

## Overview

The AI Computer Automation System provides a RESTful API for creating and managing automation tasks. This document provides detailed information about available endpoints, request/response formats, and examples.

## Base URL

All API endpoints are relative to: `http://your-server:5000/`

## Authentication

Currently, the API does not require authentication. Future versions will implement OAuth2 authentication.

## Endpoints

### Create Task

Create a new automation task with AI-powered execution.

**Endpoint:** `POST /task/create`

**Request Body:**
```json
{
    "description": "string (required) - Natural language description of the task"
}
```

**Response:**
```json
{
    "task_id": "integer - Unique identifier for the created task"
}
```

**Status Codes:**
- 200: Success
- 400: Invalid request (missing description)
- 500: Server error

**Example:**
```bash
curl -X POST http://localhost:5000/task/create \
     -H "Content-Type: application/json" \
     -d '{"description": "Click the submit button"}'
```

### Get Task Status

Retrieve the current status of a task.

**Endpoint:** `GET /task/{task_id}/status`

**Parameters:**
- task_id (path): Integer ID of the task

**Response:**
```json
{
    "status": "string (pending|completed|failed)",
    "message": "string - Latest status message",
    "screenshot": "string (optional) - Path to latest screenshot",
    "ai_analysis": {
        "reasoning": "string - AI reasoning about the task",
        "steps": [
            {
                "type": "string",
                "content": "string"
            }
        ]
    }
}
```

**Status Codes:**
- 200: Success
- 404: Task not found
- 500: Server error

**Example:**
```bash
curl http://localhost:5000/task/1/status
```

### Get Task History

Retrieve a list of all tasks.

**Endpoint:** `GET /history`

**Response:** HTML page containing task history

**Status Codes:**
- 200: Success
- 500: Server error

### Health Check

Check system health and service availability.

**Endpoint:** `GET /health`

**Response:**
```json
{
    "status": "string (healthy|unhealthy)",
    "database": "boolean",
    "ollama_service": "boolean",
    "screenshot_service": "boolean",
    "automation_service": "boolean"
}
```

**Status Codes:**
- 200: Success
- 500: Server error

## Error Handling

All endpoints follow a consistent error response format:

```json
{
    "error": "string - Error message",
    "details": "string (optional) - Detailed error information"
}
```

Common error codes:
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

## Rate Limiting

Currently, no rate limiting is implemented. Future versions will include rate limiting headers:
- X-RateLimit-Limit
- X-RateLimit-Remaining
- X-RateLimit-Reset

## Versioning

API versioning will be implemented in future releases using URL prefixing (e.g., `/v1/task/create`).
