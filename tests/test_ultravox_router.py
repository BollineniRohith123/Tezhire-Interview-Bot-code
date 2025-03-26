"""
Tests for the Ultravox router.
"""
import json
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from fastapi import HTTPException

from app.main import app
from app.routers.ultravox import make_ultravox_request, router


class TestUltravoxRouter(unittest.TestCase):
    """Test cases for the Ultravox router."""
    
    def setUp(self):
        """Set up the test client."""
        self.client = TestClient(app)
    
    @patch('app.routers.ultravox.make_ultravox_request')
    @patch('app.routers.ultravox.get_api_key')
    async def test_create_call(self, mock_get_api_key, mock_make_request):
        """Test creating a call."""
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
            "systemPrompt": "Test prompt",
            "model": "test-model",
            "voice": "test-voice",
            "maxDuration": "1800s"
        }
        
        # Make the request
        response = await self.client.post(
            "/api/ultravox",
            json=test_data,
            headers={"X-API-Key": "test-api-key"}
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["callId"], "test-call-id")
        self.assertEqual(data["joinUrl"], "https://example.com/join/test-call-id")
        
        # Check that the API was called correctly
        mock_make_request.assert_called_once()
        args, kwargs = mock_make_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(kwargs["json_data"], test_data)
    
    @patch('app.routers.ultravox.make_ultravox_request')
    @patch('app.routers.ultravox.get_api_key')
    async def test_create_call_invalid_request(self, mock_get_api_key, mock_make_request):
        """Test creating a call with invalid request data."""
        # Mock the API key
        mock_get_api_key.return_value = "test-api-key"
        
        # Test data (missing required systemPrompt)
        test_data = {
            "model": "test-model",
            "voice": "test-voice"
        }
        
        # Make the request
        response = await self.client.post(
            "/api/ultravox",
            json=test_data,
            headers={"X-API-Key": "test-api-key"}
        )
        
        # Check the response
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("error", data)
        self.assertIn("systemPrompt", data.get("details", ""))
        
        # Check that the API was not called
        mock_make_request.assert_not_called()
    
    @patch('app.routers.ultravox.make_ultravox_request')
    @patch('app.routers.ultravox.get_api_key')
    async def test_validate_key(self, mock_get_api_key, mock_make_request):
        """Test validating an API key."""
        # Mock the Ultravox API response
        mock_make_request.return_value = {
            "name": "Test Account",
            "billingUrl": "https://example.com/billing",
            "freeTimeUsed": "1h",
            "freeTimeRemaining": "2h",
            "hasActiveSubscription": True,
            "activeCalls": 0,
            "allowedConcurrentCalls": 5,
            "allowedVoices": 10
        }
        
        # Test data
        test_data = {
            "apiKey": "test-api-key"
        }
        
        # Make the request
        response = await self.client.post(
            "/api/ultravox/validate-key",
            json=test_data
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["valid"])
        self.assertEqual(data["accountInfo"]["name"], "Test Account")
        
        # Check that the API was called correctly
        mock_make_request.assert_called_once()
        args, kwargs = mock_make_request.call_args
        self.assertEqual(args[0], "GET")
        self.assertEqual(args[1], "https://api.ultravox.ai/api/accounts/me")
        self.assertEqual(args[2], "test-api-key")
    
    @patch('app.routers.ultravox.make_ultravox_request')
    @patch('app.routers.ultravox.get_api_key')
    async def test_get_messages(self, mock_get_api_key, mock_make_request):
        """Test getting messages for a call."""
        # Mock the API key
        mock_get_api_key.return_value = "test-api-key"
        
        # Mock the Ultravox API response
        mock_make_request.return_value = {
            "messages": [
                {
                    "role": "ASSISTANT",
                    "text": "Hello, how can I help you?",
                    "ordinal": 1
                },
                {
                    "role": "USER",
                    "text": "Tell me about yourself",
                    "ordinal": 2
                }
            ]
        }
        
        # Make the request
        response = await self.client.get(
            "/api/ultravox/messages?call_id=test-call-id",
            headers={"X-API-Key": "test-api-key"}
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["messages"]), 2)
        self.assertEqual(data["messages"][0]["text"], "Hello, how can I help you?")
        
        # Check that the API was called correctly
        mock_make_request.assert_called_once()
        args, kwargs = mock_make_request.call_args
        self.assertEqual(args[0], "GET")
        self.assertEqual(args[1], "https://api.ultravox.ai/api/calls/test-call-id/messages")
    
    @patch('app.routers.ultravox.make_ultravox_request')
    @patch('app.routers.ultravox.get_api_key')
    async def test_create_call_with_defaults(self, mock_get_api_key, mock_make_request):
        """Test creating a call with default settings."""
        # Mock the API key
        mock_get_api_key.return_value = "test-api-key"
        
        # Mock the Ultravox API response
        mock_make_request.return_value = {
            "callId": "test-call-id",
            "joinUrl": "https://example.com/join/test-call-id",
            "created": "2023-01-01T00:00:00Z"
        }
        
        # Make the request
        response = await self.client.post(
            "/api/ultravox/create-with-defaults?system_prompt=Test%20prompt&model=test-model",
            headers={"X-API-Key": "test-api-key"}
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["callId"], "test-call-id")
        self.assertEqual(data["joinUrl"], "https://example.com/join/test-call-id")
        
        # Check that the API was called correctly
        mock_make_request.assert_called_once()
        args, kwargs = mock_make_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(kwargs["json_data"]["systemPrompt"], "Test prompt")
        self.assertEqual(kwargs["json_data"]["model"], "test-model")
    
    @patch('app.routers.ultravox.make_ultravox_request')
    @patch('app.routers.ultravox.get_api_key')
    async def test_health_check_healthy(self, mock_get_api_key, mock_make_request):
        """Test health check when API is healthy."""
        # Mock the API key
        mock_get_api_key.return_value = "test-api-key"
        
        # Mock the Ultravox API response
        mock_make_request.return_value = {
            "name": "Test Account"
        }
        
        # Make the request
        response = await self.client.get(
            "/api/ultravox/health",
            headers={"X-API-Key": "test-api-key"}
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
    
    @patch('app.routers.ultravox.make_ultravox_request')
    @patch('app.routers.ultravox.get_api_key')
    async def test_health_check_unhealthy(self, mock_get_api_key, mock_make_request):
        """Test health check when API is unhealthy."""
        # Mock the API key
        mock_get_api_key.return_value = "test-api-key"
        
        # Mock the Ultravox API error
        mock_make_request.side_effect = HTTPException(
            status_code=401,
            detail={"error": "Unauthorized", "details": "Invalid API key"}
        )
        
        # Make the request
        response = await self.client.get(
            "/api/ultravox/health",
            headers={"X-API-Key": "test-api-key"}
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)  # Always 200 for health checks
        data = response.json()
        self.assertEqual(data["status"], "unhealthy")
        self.assertEqual(data["error"], "Unauthorized")


class TestMakeUltravoxRequest(unittest.TestCase):
    """Test cases for the make_ultravox_request function."""
    
    @patch('httpx.AsyncClient.request')
    async def test_successful_request(self, mock_request):
        """Test a successful API request."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.status_code = 200
        mock_response.reason_phrase = "OK"
        mock_response.json.return_value = {"result": "success"}
        
        # Set up the mock
        mock_request.return_value = mock_response
        
        # Make the request
        result = await make_ultravox_request(
            "GET",
            "https://api.example.com/test",
            "test-api-key"
        )
        
        # Check the result
        self.assertEqual(result, {"result": "success"})
        
        # Check that the request was made correctly
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], "GET")
        self.assertEqual(args[1], "https://api.example.com/test")
        self.assertEqual(kwargs["headers"]["X-API-Key"], "test-api-key")
    
    @patch('httpx.AsyncClient.request')
    async def test_error_response(self, mock_request):
        """Test handling an error response."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.is_success = False
        mock_response.status_code = 400
        mock_response.reason_phrase = "Bad Request"
        mock_response.text = "Error text"
        mock_response.json.return_value = {"error": "Bad request", "message": "Invalid parameter"}
        
        # Set up the mock
        mock_request.return_value = mock_response
        
        # Make the request and check for exception
        with self.assertRaises(HTTPException) as context:
            await make_ultravox_request(
                "POST",
                "https://api.example.com/test",
                "test-api-key",
                json_data={"param": "value"}
            )
        
        # Check the exception details
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail["error"], "Ultravox API error")
        self.assertEqual(context.exception.detail["details"], "Bad request")
    
    @patch('httpx.AsyncClient.request')
    async def test_timeout_exception(self, mock_request):
        """Test handling a timeout exception."""
        # Set up the mock to raise a timeout exception
        from httpx import TimeoutException
        mock_request.side_effect = TimeoutException("Request timed out")
        
        # Make the request and check for exception
        with self.assertRaises(HTTPException) as context:
            await make_ultravox_request(
                "GET",
                "https://api.example.com/test",
                "test-api-key"
            )
        
        # Check the exception details
        self.assertEqual(context.exception.status_code, 504)
        self.assertEqual(context.exception.detail["error"], "API request timed out")


if __name__ == "__main__":
    unittest.main()