"""
Tests for the Tezhire router.
"""
import json
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from fastapi import HTTPException

from app.main import app
from app.routers.tezhire import router, session_store
from app.routers.ultravox import make_ultravox_request


class TestTezhireRouter(unittest.TestCase):
    """Test cases for the Tezhire router."""
    
    def setUp(self):
        """Set up the test client."""
        self.client = TestClient(app)
        # Clear the session store before each test
        session_store.clear()
    
    @patch('app.routers.tezhire.make_ultravox_request')
    @patch('app.routers.tezhire.get_api_key')
    async def test_create_interview_session(self, mock_get_api_key, mock_make_request):
        """Test creating an interview session."""
        # Mock the API key
        mock_get_api_key.return_value = "test-api-key"
        
        # Mock the Ultravox API response
        mock_make_request.return_value = {
            "callId": "test-call-id",
            "joinUrl": "https://example.com/join/test-call-id",
            "created": "2023-01-01T00:00:00Z"
        }
        
        # Test data
        test_data = {
            "session": {
                "sessionId": "session-123",
                "callbackUrl": "https://example.com/callback"
            },
            "candidate": {
                "candidateId": "candidate-123",
                "name": "John Doe",
                "email": "john@example.com",
                "resumeData": {
                    "skills": ["Python", "JavaScript"],
                    "experience": [
                        {
                            "company": "Example Corp",
                            "role": "Developer",
                            "duration": "2 years",
                            "description": "Developed web applications"
                        }
                    ],
                    "education": [
                        {
                            "institution": "Example University",
                            "degree": "BS",
                            "fieldOfStudy": "Computer Science",
                            "year": 2020
                        }
                    ],
                    "projects": [
                        {
                            "name": "Project X",
                            "description": "A web application",
                            "technologies": ["React", "Node.js"]
                        }
                    ],
                    "rawText": "John Doe - Developer"
                }
            },
            "job": {
                "jobId": "job-456",
                "companyId": "company-789",
                "recruiterUserId": "recruiter-101",
                "title": "Software Engineer",
                "department": "Engineering",
                "description": "Software engineering position",
                "requirements": ["Python", "JavaScript"],
                "responsibilities": ["Develop applications", "Write tests"],
                "location": "Remote",
                "employmentType": "Full-time",
                "experienceLevel": "Mid-level"
            },
            "interview": {
                "duration": 30,
                "difficultyLevel": "Medium",
                "topicsToFocus": ["Python", "Web Development"],
                "topicsToAvoid": ["Salary", "Personal questions"],
                "customQuestions": ["Tell me about yourself", "What are your strengths?"],
                "interviewStyle": "Conversational",
                "feedbackDetail": "Comprehensive"
            },
            "configuration": {
                "language": "en-US",
                "voiceId": "echo",
                "enableTranscription": True,
                "audioQuality": "high",
                "timeZone": "America/New_York"
            }
        }
        
        # Make the request
        response = await self.client.post(
            "/api/tezhire/interview-sessions",
            json=test_data,
            headers={"X-API-Key": "test-api-key"}
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["sessionId"], "session-123")
        self.assertEqual(data["joinUrl"], "https://example.com/join/test-call-id")
        self.assertEqual(data["status"], "created")
        
        # Check that the API was called correctly
        mock_make_request.assert_called_once()
        args, kwargs = mock_make_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(args[1], "https://api.ultravox.ai/api/calls")
        self.assertEqual(args[2], "test-api-key")
        self.assertEqual(kwargs["json_data"]["voice"], "echo")
        self.assertEqual(kwargs["json_data"]["languageHint"], "en-US")
        self.assertTrue(kwargs["json_data"]["recordingEnabled"])
        
        # Check that the session was stored
        self.assertIn("session-123", session_store)
        self.assertEqual(session_store["session-123"]["call_id"], "test-call-id")
        self.assertEqual(session_store["session-123"]["status"], "created")
    
    @patch('app.routers.tezhire.get_api_key')
    async def test_get_session_status(self, mock_get_api_key):
        """Test getting the status of an interview session."""
        # Mock the API key
        mock_get_api_key.return_value = "test-api-key"
        
        # Create a test session
        session_id = "session-123"
        created_at = datetime.now() - timedelta(minutes=10)
        session_store[session_id] = {
            "call_id": "test-call-id",
            "join_url": "https://example.com/join/test-call-id",
            "created_at": created_at.isoformat(),
            "status": "in_progress",
            "candidate_id": "candidate-123",
            "job_id": "job-456",
            "company_id": "company-789",
            "expiry": (created_at + timedelta(days=1)).isoformat()
        }
        
        # Make the request
        response = await self.client.get(
            f"/api/tezhire/interview-sessions/{session_id}",
            headers={"X-API-Key": "test-api-key"}
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["sessionId"], session_id)
        self.assertEqual(data["status"], "in_progress")
        self.assertEqual(data["candidateId"], "candidate-123")
        self.assertEqual(data["jobId"], "job-456")
        self.assertEqual(data["startTime"], created_at.isoformat())
        self.assertIsNone(data["endTime"])
        self.assertGreater(data["duration"], 0)
        self.assertGreater(data["progress"], 0)
        self.assertGreater(data["questionsAsked"], 0)
    
    @patch('app.routers.tezhire.get_api_key')
    async def test_get_session_status_not_found(self, mock_get_api_key):
        """Test getting the status of a non-existent session."""
        # Mock the API key
        mock_get_api_key.return_value = "test-api-key"
        
        # Make the request
        response = await self.client.get(
            "/api/tezhire/interview-sessions/non-existent-session",
            headers={"X-API-Key": "test-api-key"}
        )
        
        # Check the response
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["error"], "Session not found")
    
    @patch('app.routers.tezhire.get_api_key')
    async def test_end_session(self, mock_get_api_key):
        """Test ending an interview session."""
        # Mock the API key
        mock_get_api_key.return_value = "test-api-key"
        
        # Create a test session
        session_id = "session-123"
        created_at = datetime.now() - timedelta(minutes=20)
        session_store[session_id] = {
            "call_id": "test-call-id",
            "join_url": "https://example.com/join/test-call-id",
            "created_at": created_at.isoformat(),
            "status": "in_progress",
            "candidate_id": "candidate-123",
            "job_id": "job-456",
            "company_id": "company-789",
            "expiry": (created_at + timedelta(days=1)).isoformat()
        }
        
        # Make the request
        response = await self.client.post(
            f"/api/tezhire/interview-sessions/{session_id}/end",
            json={"reason": "Interview completed"},
            headers={"X-API-Key": "test-api-key"}
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["sessionId"], session_id)
        self.assertEqual(data["status"], "ended")
        self.assertGreater(data["duration"], 0)
        
        # Check that the session was updated
        self.assertEqual(session_store[session_id]["status"], "ended")
        self.assertIn("end_time", session_store[session_id])
        self.assertIn("duration", session_store[session_id])
    
    @patch('app.routers.tezhire.get_api_key')
    async def test_get_interview_results(self, mock_get_api_key):
        """Test getting the results of an interview session."""
        # Mock the API key
        mock_get_api_key.return_value = "test-api-key"
        
        # Create a test session
        session_id = "session-123"
        created_at = datetime.now() - timedelta(minutes=30)
        end_time = datetime.now() - timedelta(minutes=5)
        session_store[session_id] = {
            "call_id": "test-call-id",
            "join_url": "https://example.com/join/test-call-id",
            "created_at": created_at.isoformat(),
            "status": "ended",
            "end_time": end_time.isoformat(),
            "duration": 1500,
            "candidate_id": "candidate-123",
            "job_id": "job-456",
            "company_id": "company-789",
            "expiry": (created_at + timedelta(days=1)).isoformat()
        }
        
        # Make the request
        response = await self.client.get(
            f"/api/tezhire/interview-sessions/{session_id}/results",
            headers={"X-API-Key": "test-api-key"}
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["sessionId"], session_id)
        self.assertEqual(data["candidateId"], "candidate-123")
        self.assertEqual(data["jobId"], "job-456")
        self.assertEqual(data["companyId"], "company-789")
        self.assertIn("overallScore", data)
        self.assertIn("feedback", data)
        self.assertIn("questions", data)
        self.assertIn("transcript", data)
        self.assertIn("audio", data)
    
    @patch('app.routers.tezhire.get_api_key')
    async def test_get_interview_results_active_session(self, mock_get_api_key):
        """Test getting the results of an active session."""
        # Mock the API key
        mock_get_api_key.return_value = "test-api-key"
        
        # Create a test session
        session_id = "session-123"
        created_at = datetime.now() - timedelta(minutes=10)
        session_store[session_id] = {
            "call_id": "test-call-id",
            "join_url": "https://example.com/join/test-call-id",
            "created_at": created_at.isoformat(),
            "status": "in_progress",
            "candidate_id": "candidate-123",
            "job_id": "job-456",
            "company_id": "company-789",
            "expiry": (created_at + timedelta(days=1)).isoformat()
        }
        
        # Make the request
        response = await self.client.get(
            f"/api/tezhire/interview-sessions/{session_id}/results",
            headers={"X-API-Key": "test-api-key"}
        )
        
        # Check the response
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["error"], "Session active")
        self.assertEqual(data["details"], "Cannot get results for an active session")
    
    @patch('app.routers.tezhire.get_api_key')
    async def test_configure_webhook(self, mock_get_api_key):
        """Test configuring a webhook."""
        # Mock the API key
        mock_get_api_key.return_value = "test-api-key"
        
        # Test data
        test_data = {
            "url": "https://example.com/webhook",
            "secret": "webhook-secret",
            "events": ["interview.created", "interview.completed", "results.available"]
        }
        
        # Make the request
        response = await self.client.post(
            "/api/tezhire/webhooks",
            json=test_data,
            headers={"X-API-Key": "test-api-key"}
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["url"], "https://example.com/webhook")
        self.assertEqual(data["events"], ["interview.created", "interview.completed", "results.available"])
        self.assertIn("webhookId", data)
    
    @patch('app.routers.tezhire.get_api_key')
    async def test_configure_webhook_invalid_events(self, mock_get_api_key):
        """Test configuring a webhook with invalid events."""
        # Mock the API key
        mock_get_api_key.return_value = "test-api-key"
        
        # Test data with invalid event
        test_data = {
            "url": "https://example.com/webhook",
            "secret": "webhook-secret",
            "events": ["interview.created", "invalid.event"]
        }
        
        # Make the request
        response = await self.client.post(
            "/api/tezhire/webhooks",
            json=test_data,
            headers={"X-API-Key": "test-api-key"}
        )
        
        # Check the response
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["error"], "Invalid event types")
        self.assertIn("invalid.event", data["details"])


if __name__ == "__main__":
    unittest.main()