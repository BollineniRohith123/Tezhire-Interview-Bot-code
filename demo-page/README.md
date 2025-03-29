# Tezhire Interview Bot Demo

This demo showcases a WebRTC-based interview system that allows customers to create interview sessions, conduct interviews, and generate comprehensive summaries of the conversations.

## Features

- **JSON Configuration**: Input a JSON object to create a customized interview session
- **WebRTC Call**: Initiate a WebRTC call session based on the provided configuration
- **Automated Interview**: Experience an AI-driven interview with predefined questions
- **Comprehensive Summary**: View a detailed summary of the interview, including:
  - Technical score
  - Communication score
  - Overall assessment
  - Strengths and areas for improvement
  - Hiring recommendation
  - Full interview transcript

## How to Use

1. Open `index.html` in a web browser
2. Click "Load Sample JSON" to populate the input field with a sample configuration, or enter your own JSON configuration
3. Click "Validate JSON" to ensure your configuration is valid
4. Click "Create Interview Session" to start the interview
5. The WebRTC call will be initiated automatically
6. Answer the interview questions as they are asked
7. The interview will end automatically after all questions are answered, or you can click "End Interview" to end it manually
8. View the comprehensive interview summary, including scores and recommendations

## JSON Configuration Format

The JSON configuration should follow this structure:

```json
{
  "session": {
    "sessionId": "unique-session-id",
    "callbackUrl": "https://example.com/webhook"
  },
  "candidate": {
    "candidateId": "candidate-id",
    "name": "Candidate Name",
    "email": "candidate@example.com",
    "phone": "+1234567890",
    "resumeData": {
      "skills": ["Skill1", "Skill2"],
      "experience": [
        {
          "company": "Company Name",
          "role": "Job Title",
          "duration": "Duration",
          "description": "Job Description"
        }
      ],
      "education": [
        {
          "institution": "Institution Name",
          "degree": "Degree",
          "fieldOfStudy": "Field of Study",
          "year": 2020
        }
      ],
      "projects": [
        {
          "name": "Project Name",
          "description": "Project Description",
          "technologies": ["Tech1", "Tech2"]
        }
      ],
      "rawText": "Full resume text"
    }
  },
  "job": {
    "jobId": "job-id",
    "companyId": "company-id",
    "recruiterUserId": "recruiter-id",
    "title": "Job Title",
    "department": "Department",
    "description": "Job Description",
    "requirements": ["Requirement1", "Requirement2"],
    "responsibilities": ["Responsibility1", "Responsibility2"],
    "location": "Location",
    "employmentType": "Employment Type",
    "experienceLevel": "Experience Level",
    "salaryRange": {
      "min": 50000,
      "max": 100000,
      "currency": "USD"
    }
  },
  "interview": {
    "duration": 30,
    "difficultyLevel": "Medium",
    "topicsToFocus": ["Topic1", "Topic2"],
    "topicsToAvoid": ["Topic3", "Topic4"],
    "customQuestions": ["Question1", "Question2"],
    "interviewStyle": "Conversational",
    "feedbackDetail": "Comprehensive"
  },
  "configuration": {
    "language": "en-US",
    "voiceId": "voice-id",
    "enableTranscription": true,
    "audioQuality": "high",
    "timeZone": "America/New_York"
  }
}
```

## Notes

- This is a demo application and does not make actual API calls to the backend
- In a production environment, the WebRTC call would be connected to a real Ultravox session
- The interview summary is generated with mock data for demonstration purposes

## Requirements

- Modern web browser with JavaScript enabled
- Internet connection (for loading external resources)