# Interview Bot Python Backend

This is the Python backend for the Interview Bot application with Ultravox integration for WebRTC functionality. This backend is a migration from the original Next.js backend.

## Features

- **Voice Interviews**: Conduct real-time voice interviews using Ultravox's WebRTC technology
- **Comprehensive API**: Create, manage, and analyze interview sessions
- **Candidate Assessment**: Evaluate candidates based on their responses and generate detailed reports
- **Customizable Interviews**: Configure interview parameters such as duration, difficulty, and topics
- **Real-time Transcription**: Get real-time transcripts of the interview
- **Webhook Integration**: Receive real-time updates about interview sessions

## Prerequisites

- Python 3.8 or higher
- An Ultravox API key

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Ultravox API key:
   ```
   ULTRAVOX_API_KEY=your_api_key_here
   ```

## Running the Application

```bash
python main.py
```

The application will be available at http://localhost:8000.

## API Documentation

### API Endpoints

- `POST /api/tezhire/interview-sessions` - Create a new interview session
- `GET /api/tezhire/interview-sessions/{sessionId}` - Check the status of an interview session
- `POST /api/tezhire/interview-sessions/{sessionId}/end` - End an interview session
- `GET /api/tezhire/interview-sessions/{sessionId}/results` - Get the results of an interview
- `POST /api/tezhire/webhooks` - Configure webhooks for real-time updates
- `POST /api/ultravox` - Create a new Ultravox call
- `GET /api/ultravox/messages` - Get messages for a specific call
- `POST /api/ultravox/validate-key` - Validate an Ultravox API key

## Implementation Details

The application is built using:

- FastAPI for the API framework
- Pydantic for data validation and serialization
- HTTPX for making HTTP requests
- Python-dotenv for environment variable management
- Uvicorn for the ASGI server

## Security Considerations

- API keys are stored securely and never exposed to the client
- All API endpoints require authentication
- Sensitive candidate data is handled in compliance with data protection regulations
- Webhook payloads are validated using a secret

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.