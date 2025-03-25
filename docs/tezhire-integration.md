# Tezhire-Ultravox Integration API Documentation

This documentation provides a comprehensive guide to the Tezhire-Ultravox integration API, which enables automated voice interviews using Ultravox's WebRTC capabilities.

## Overview

The Tezhire-Ultravox integration allows you to:

1. Create interview sessions with detailed candidate and job information
2. Monitor the status of ongoing interviews
3. End interview sessions when needed
4. Retrieve detailed interview results and analysis
5. Configure webhooks for real-time updates

## Authentication

All API endpoints require an Ultravox API key for authentication. The API key can be provided in two ways:

1. As an environment variable: `ULTRAVOX_API_KEY`
2. In the request header: `X-API-Key`

Example:
```http
POST /api/tezhire/interview-sessions
Content-Type: application/json
X-API-Key: your_ultravox_api_key
```

## API Endpoints

### 1. Create Interview Session

Creates a new WebRTC interview session with Ultravox using candidate and job details.

**Endpoint:** `POST /api/tezhire/interview-sessions`

**Request Body:**
```json
{
  "session": {
    "sessionId": "string",
    "callbackUrl": "string"
  },
  "candidate": {
    "candidateId": "string",
    "name": "string",
    "email": "string",
    "phone": "string",
    "resumeData": {
      "skills": ["string"],
      "experience": [{
        "company": "string",
        "role": "string",
        "duration": "string",
        "description": "string"
      }],
      "education": [{
        "institution": "string",
        "degree": "string",
        "fieldOfStudy": "string",
        "year": "number"
      }],
      "projects": [{
        "name": "string",
        "description": "string",
        "technologies": ["string"]
      }],
      "rawText": "string"
    }
  },
  "job": {
    "jobId": "string",
    "companyId": "string",
    "recruiterUserId": "string",
    "title": "string",
    "department": "string",
    "description": "string",
    "requirements": ["string"],
    "responsibilities": ["string"],
    "location": "string",
    "employmentType": "string",
    "experienceLevel": "string",
    "salaryRange": {
      "min": "number",
      "max": "number",
      "currency": "string"
    }
  },
  "interview": {
    "duration": "number",
    "difficultyLevel": "string",
    "topicsToFocus": ["string"],
    "topicsToAvoid": ["string"],
    "customQuestions": ["string"],
    "interviewStyle": "string",
    "feedbackDetail": "string"
  },
  "configuration": {
    "language": "string",
    "voiceId": "string",
    "enableTranscription": "boolean",
    "audioQuality": "string",
    "timeZone": "string"
  }
}
```

**Response:**
```json
{
  "success": true,
  "sessionId": "string",
  "joinUrl": "string",
  "expiry": "string",
  "status": "created"
}
```

### 2. Check Session Status

Retrieves the current status of an interview session.

**Endpoint:** `GET /api/tezhire/interview-sessions/{sessionId}`

**Response:**
```json
{
  "sessionId": "string",
  "status": "string",
  "candidateId": "string",
  "jobId": "string",
  "startTime": "string",
  "endTime": "string",
  "duration": "number",
  "progress": "number",
  "questionsAsked": "number"
}
```

### 3. End Interview Session

Forcefully terminates an ongoing interview session.

**Endpoint:** `POST /api/tezhire/interview-sessions/{sessionId}/end`

**Request Body:**
```json
{
  "reason": "string"
}
```

**Response:**
```json
{
  "success": true,
  "sessionId": "string",
  "status": "ended",
  "duration": "number"
}
```

### 4. Retrieve Interview Results

Retrieves the detailed results of a completed interview.

**Endpoint:** `GET /api/tezhire/interview-sessions/{sessionId}/results`

**Response:**
```json
{
  "sessionId": "string",
  "candidateId": "string",
  "jobId": "string",
  "companyId": "string",
  "overallScore": "number",
  "feedback": {
    "summary": "string",
    "strengths": ["string"],
    "areasForImprovement": ["string"],
    "technicalAssessment": "string",
    "communicationAssessment": "string",
    "fitScore": "number",
    "recommendation": "string"
  },
  "questions": [{
    "questionId": "string",
    "question": "string",
    "timestamp": "string",
    "answerTranscript": "string",
    "answerDuration": "number",
    "evaluation": {
      "score": "number",
      "feedback": "string",
      "keyInsights": ["string"]
    }
  }],
  "transcript": {
    "full": "string",
    "url": "string"
  },
  "audio": {
    "url": "string",
    "duration": "number"
  }
}
```

### 5. Configure Webhooks

Configure webhooks to receive real-time updates about interview sessions.

**Endpoint:** `POST /api/tezhire/webhooks`

**Request Body:**
```json
{
  "url": "string",
  "secret": "string",
  "events": ["string"]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Webhook configured successfully",
  "webhookId": "string",
  "url": "string",
  "events": ["string"]
}
```

## Webhook Events

The following events can be subscribed to:

1. `interview.created` - Interview session created
2. `interview.started` - Candidate joined the interview
3. `interview.completed` - Interview concluded normally
4. `interview.cancelled` - Interview was cancelled
5. `interview.error` - Error occurred during interview
6. `results.available` - Interview results are ready

## WebRTC Integration

The Tezhire-Ultravox integration provides a WebRTC client for connecting to the voice interview session. The client can be used to:

1. Join the interview session
2. Toggle microphone mute/unmute
3. Toggle speaker mute/unmute
4. End the interview session
5. Receive real-time transcript updates

## Error Handling

All API endpoints return appropriate HTTP status codes:

- 200: Success
- 400: Bad Request (invalid parameters)
- 401: Unauthorized (invalid or missing API key)
- 404: Not Found (resource doesn't exist)
- 500: Internal Server Error

Error responses have the following format:

```json
{
  "error": "string",
  "details": "string"
}
```

## Demo Page

A demo page is available at `/tezhire` to test the Tezhire-Ultravox integration. The demo page allows you to:

1. Create an interview session with custom parameters
2. Join the interview session using WebRTC
3. Test microphone and speaker controls
4. End the interview session

## Implementation Checklist

- [x] Create interview session API endpoint
- [x] Check session status API endpoint
- [x] End interview session API endpoint
- [x] Retrieve interview results API endpoint
- [x] Configure webhooks API endpoint
- [x] WebRTC client integration
- [x] Demo page for testing
- [x] Documentation

## Security Considerations

1. Store API keys securely
2. Use HTTPS for all API requests
3. Validate webhook payloads using the secret
4. Implement rate limiting to prevent abuse
5. Store sensitive candidate data in compliance with relevant data protection regulations