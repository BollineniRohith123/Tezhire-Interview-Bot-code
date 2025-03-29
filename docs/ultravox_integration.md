# Ultravox Integration Guide

This document provides comprehensive documentation for the Ultravox integration in the Tezhire Interview Bot application.

## Overview

Ultravox is a WebRTC-based voice AI platform that enables real-time voice conversations. The Tezhire Interview Bot uses Ultravox to conduct automated technical interviews with candidates.

## Configuration

### Environment Variables

The following environment variables are used to configure the Ultravox integration:

- `ULTRAVOX_API_KEY`: Your Ultravox API key (required)
- `ULTRAVOX_MODEL`: The model to use (default: "fixie-ai/ultravox-70B")
- `ULTRAVOX_VOICE`: The voice to use (default: "echo")
- `ULTRAVOX_LANGUAGE`: The language hint (default: "en-US")
- `ULTRAVOX_MAX_DURATION`: Maximum call duration (default: "1800s")
- `ULTRAVOX_TEMPERATURE`: Temperature for model generation (default: 0.7)
- `ULTRAVOX_RECORDING_ENABLED`: Whether to enable recording (default: true)

You can set these variables in a `.env` file or directly in your environment.

## API Endpoints

### Create a Call

```
POST /api/ultravox
```

Creates a new Ultravox call.

**Request Body:**

```json
{
  "systemPrompt": "You are an interviewer for a software engineering position...",
  "model": "fixie-ai/ultravox-70B",
  "voice": "echo",
  "languageHint": "en-US",
  "maxDuration": "1800s",
  "temperature": 0.7,
  "recordingEnabled": true
}
```

**Response:**

```json
{
  "callId": "call_123456789",
  "joinUrl": "https://ultravox.ai/join/call_123456789",
  "created": "2023-01-01T00:00:00Z",
  "model": "fixie-ai/ultravox-70B",
  "systemPrompt": "You are an interviewer...",
  "temperature": 0.7
}
```

### Create a Call with Default Settings

```
POST /api/ultravox/create-with-defaults?system_prompt=Your%20prompt&model=model-name&voice=voice-name
```

Creates a new Ultravox call with default settings, allowing you to override specific parameters via query parameters.

**Query Parameters:**

- `system_prompt` (required): The system prompt for the call
- `model` (optional): The model to use
- `voice` (optional): The voice to use
- `max_duration` (optional): Maximum duration in seconds
- `temperature` (optional): Temperature for model generation

**Response:**

Same as the Create a Call endpoint.

### Get Call Messages

```
GET /api/ultravox/messages?call_id=call_123456789
```

Gets the messages for a specific call.

**Query Parameters:**

- `call_id` (required): The ID of the call to fetch messages for

**Response:**

```json
{
  "messages": [
    {
      "role": "ASSISTANT",
      "text": "Hello, I'm your interviewer today. How are you doing?",
      "ordinal": 1
    },
    {
      "role": "USER",
      "text": "I'm doing well, thank you.",
      "ordinal": 2
    }
  ]
}
```

### Validate API Key

```
POST /api/ultravox/validate-key
```

Validates an Ultravox API key.

**Request Body:**

```json
{
  "apiKey": "your-api-key"
}
```

**Response:**

```json
{
  "valid": true,
  "accountInfo": {
    "name": "Your Account",
    "billingUrl": "https://ultravox.ai/billing",
    "freeTimeUsed": "1h",
    "freeTimeRemaining": "2h",
    "hasActiveSubscription": true,
    "activeCalls": 0,
    "allowedConcurrentCalls": 5,
    "allowedVoices": 10
  }
}
```

### Health Check

```
GET /api/ultravox/health
```

Checks the health of the Ultravox API.

**Response (Healthy):**

```json
{
  "status": "healthy",
  "message": "Ultravox API is operational"
}
```

**Response (Unhealthy):**

```json
{
  "status": "unhealthy",
  "message": "Ultravox API is not operational",
  "error": "Unauthorized",
  "status_code": 401
}
```

## Error Handling

All API endpoints return standardized error responses:

```json
{
  "error": "Error message",
  "details": "Additional error details"
}
```

Common error scenarios:

- **401 Unauthorized**: Invalid or missing API key
- **400 Bad Request**: Invalid request parameters
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server-side error
- **502 Bad Gateway**: Error communicating with Ultravox API
- **504 Gateway Timeout**: Ultravox API request timed out

## Usage Examples

### Joining a Call

```python
import httpx

async def join_call():
    url = "http://localhost:8000/api/ultravox/join"
    payload = {
        "apiKey": "your-ultravox-api-key",
        "systemPrompt": "You are an interviewer for a software engineering position...",
        "model": "fixie-ai/ultravox-70B",
        "voice": "terrence",
        "temperature": 0.4
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()
```

### Creating a Call with Advanced Options

```python
import httpx

async def create_call():
    url = "http://localhost:8000/api/ultravox/create-call"
    payload = {
        "apiKey": "your-ultravox-api-key",
        "systemPrompt": "You are an interviewer for a software engineering position...",
        "model": "fixie-ai/ultravox-70B",
        "voice": "terrence",
        "externalVoice": {
            "elevenLabs": {
                "voiceId": "voice-id",
                "model": "eleven-model"
            }
        },
        "maxDuration": "1800s"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()
```

### Listing Calls with Pagination

```python
import httpx

async def list_calls(cursor=None):
    url = "http://localhost:8000/api/ultravox/list-calls"
    payload = {
        "apiKey": "your-ultravox-api-key"
    }
    
    if cursor:
        payload["cursor"] = cursor
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()
```

### Getting Call Messages

```python
import httpx

async def get_call_messages(call_id, cursor=None):
    url = "http://localhost:8000/api/ultravox/call-messages"
    payload = {
        "apiKey": "your-ultravox-api-key",
        "callId": call_id
    }
    
    if cursor:
        payload["cursor"] = cursor
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()
```

## Testing

The Ultravox integration includes comprehensive tests:

- `test_ultravox_config.py`: Tests for the configuration module
- `test_ultravox_router.py`: Tests for the API endpoints

Run the tests using:

```bash
python run_tests.py
```

## Troubleshooting

### API Key Issues

- Ensure your API key is correctly set in the environment variables or passed in the request body
- Validate your API key using the `/api/ultravox/validate-key` endpoint

### Connection Issues

- Check the health of the Ultravox API using the `/api/ultravox/health` endpoint
- Ensure your network allows connections to the Ultravox API (https://api.ultravox.ai)

### Call Creation Issues

- Ensure your system prompt is not empty
- Check that the model and voice specified are available in your Ultravox account
- Verify that your account has sufficient credits or an active subscription

## Best Practices

1. **System Prompts**: Create clear, detailed system prompts to guide the interview
2. **Error Handling**: Always handle API errors gracefully in your application
3. **Testing**: Test your integration thoroughly before deploying to production
4. **Monitoring**: Monitor API usage and errors to identify issues early
5. **Security**: Keep your API key secure and never expose it in client-side code
6. **Pagination**: When listing calls or messages, implement proper pagination handling
7. **External Voices**: When using external voice providers, test thoroughly to ensure compatibility
8. **Temperature Setting**: Use appropriate temperature values (0.0-1.0) based on your needs:
   - Lower values (0.0-0.3): More deterministic, consistent responses
   - Medium values (0.4-0.6): Balanced creativity and consistency
   - Higher values (0.7-1.0): More creative, varied responses