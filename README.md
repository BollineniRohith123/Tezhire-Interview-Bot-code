# Interview Bot with Tezhire-Ultravox Integration

This project implements an interview bot application that integrates with Ultravox's WebRTC capabilities to conduct voice interviews. The application includes a complete API for creating and managing interview sessions, as well as a user interface for conducting interviews.

## Features

- **Voice Interviews**: Conduct real-time voice interviews using Ultravox's WebRTC technology
- **Comprehensive API**: Create, manage, and analyze interview sessions
- **Candidate Assessment**: Evaluate candidates based on their responses and generate detailed reports
- **Customizable Interviews**: Configure interview parameters such as duration, difficulty, and topics
- **Real-time Transcription**: Get real-time transcripts of the interview
- **Webhook Integration**: Receive real-time updates about interview sessions

## Getting Started

### Prerequisites

- Node.js 18.x or higher
- An Ultravox API key

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a `.env.local` file with your Ultravox API key:
   ```
   ULTRAVOX_API_KEY=your_api_key_here
   ```

### Running the Application

```bash
npm run dev
```

The application will be available at http://localhost:3000.

## API Documentation

The API documentation is available in the [docs/tezhire-integration.md](docs/tezhire-integration.md) file. It includes detailed information about the API endpoints, request/response formats, and examples.

### API Endpoints

- `POST /api/tezhire/interview-sessions` - Create a new interview session
- `GET /api/tezhire/interview-sessions/{sessionId}` - Check the status of an interview session
- `POST /api/tezhire/interview-sessions/{sessionId}/end` - End an interview session
- `GET /api/tezhire/interview-sessions/{sessionId}/results` - Get the results of an interview
- `POST /api/tezhire/webhooks` - Configure webhooks for real-time updates

## Demo Page

A demo page is available at `/tezhire` to test the Tezhire-Ultravox integration. The demo page allows you to:

1. Create an interview session with custom parameters
2. Join the interview session using WebRTC
3. Test microphone and speaker controls
4. End the interview session

## Implementation Details

The application is built using:

- Next.js for the frontend and API routes
- TypeScript for type safety
- Tailwind CSS for styling
- Ultravox Client SDK for WebRTC integration

## Security Considerations

- API keys are stored securely and never exposed to the client
- All API endpoints require authentication
- Sensitive candidate data is handled in compliance with data protection regulations
- Webhook payloads are validated using a secret

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.