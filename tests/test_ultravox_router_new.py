"""
Tests for the updated Ultravox router.
"""
import json
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient

from app.main import app
from app.controllers.ultravox_controller import (
    join_ultravox_call,
    get_call_details,
    create_ultravox_call,
    list_ultravox_calls,
    list_call_messages,
    list_call_stages,
    get_call_stage_details
)


class TestUltravoxRouter(unittest.TestCase):
    """Test cases for the updated Ultravox router."""
    
    def setUp(self):
        """Set up the test client."""
        self.client = TestClient(app)
    
    @patch('app.controllers.ultravox_controller.join_ultravox_call')
    async def test_join_ultravox_call(self, mock_join_call):
        """Test joining a call."""
        # Mock the controller function
        mock_join_call.return_value = {
            "joinUrl": "https://example.com/join/test-call-id",
            "callId": "test-call-id",
            "created": "2023-01-01T00:00:00Z"
        }
        
        # Test data
        test_data = {
            "apiKey": "test-api-key",
            "systemPrompt": "Test prompt",
            "model": "test-model",
            "voice": "test-voice",
            "languageHint": "en",
            "temperature": 0.4
        }
        
        # Make the request
        response = await self.client.post(
            "/api/ultravox/join",
            json=test_data
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["joinUrl"], "https://example.com/join/test-call-id")
        self.assertEqual(data["callId"], "test-call-id")
        
        # Check that the controller was called correctly
        mock_join_call.assert_called_once()
        args, kwargs = mock_join_call.call_args
        self.assertEqual(args[0], "test-api-key")
        self.assertNotIn("apiKey", args[1])  # API key should be removed from config
    
    @patch('app.controllers.ultravox_controller.get_call_details')
    async def test_get_call_details(self, mock_get_details):
        """Test getting call details."""
        # Mock the controller function
        mock_get_details.return_value = {
            "callId": "test-call-id",
            "clientVersion": "1.0.0",
            "created": "2023-01-01T00:00:00Z",
            "joined": "2023-01-01T00:01:00Z",
            "systemPrompt": "Test prompt",
            "model": "test-model"
        }
        
        # Test data
        test_data = {
            "apiKey": "test-api-key",
            "callId": "test-call-id"
        }
        
        # Make the request
        response = await self.client.post(
            "/api/ultravox/call-details",
            json=test_data
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["callId"], "test-call-id")
        self.assertEqual(data["systemPrompt"], "Test prompt")
        
        # Check that the controller was called correctly
        mock_get_details.assert_called_once_with("test-api-key", "test-call-id")
    
    @patch('app.controllers.ultravox_controller.create_ultravox_call')
    async def test_create_ultravox_call(self, mock_create_call):
        """Test creating a call with advanced options."""
        # Mock the controller function
        mock_create_call.return_value = {
            "callId": "test-call-id",
            "joinUrl": "https://example.com/join/test-call-id",
            "created": "2023-01-01T00:00:00Z",
            "systemPrompt": "Test prompt",
            "model": "test-model"
        }
        
        # Test data
        test_data = {
            "apiKey": "test-api-key",
            "systemPrompt": "Test prompt",
            "model": "test-model",
            "voice": "test-voice",
            "externalVoice": {
                "elevenLabs": {
                    "voiceId": "voice-id",
                    "model": "eleven-model"
                }
            },
            "maxDuration": "1800s"
        }
        
        # Make the request
        response = await self.client.post(
            "/api/ultravox/create-call",
            json=test_data
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["callId"], "test-call-id")
        self.assertEqual(data["systemPrompt"], "Test prompt")
        
        # Check that the controller was called correctly
        mock_create_call.assert_called_once()
        args, kwargs = mock_create_call.call_args
        self.assertEqual(args[0], "test-api-key")
        self.assertNotIn("apiKey", args[1])  # API key should be removed from config
    
    @patch('app.controllers.ultravox_controller.list_ultravox_calls')
    async def test_list_ultravox_calls(self, mock_list_calls):
        """Test listing calls."""
        # Mock the controller function
        mock_list_calls.return_value = {
            "next": "next-cursor",
            "previous": None,
            "results": [
                {
                    "callId": "call-1",
                    "created": "2023-01-01T00:00:00Z",
                    "systemPrompt": "Test prompt 1"
                },
                {
                    "callId": "call-2",
                    "created": "2023-01-02T00:00:00Z",
                    "systemPrompt": "Test prompt 2"
                }
            ],
            "total": 2
        }
        
        # Test data
        test_data = {
            "apiKey": "test-api-key",
            "cursor": "test-cursor"
        }
        
        # Make the request
        response = await self.client.post(
            "/api/ultravox/list-calls",
            json=test_data
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["next"], "next-cursor")
        self.assertEqual(len(data["results"]), 2)
        self.assertEqual(data["results"][0]["callId"], "call-1")
        
        # Check that the controller was called correctly
        mock_list_calls.assert_called_once_with("test-api-key", "test-cursor")
    
    @patch('app.controllers.ultravox_controller.list_call_messages')
    async def test_list_call_messages(self, mock_list_messages):
        """Test listing call messages."""
        # Mock the controller function
        mock_list_messages.return_value = {
            "next": "next-cursor",
            "previous": None,
            "results": [
                {
                    "role": "ASSISTANT",
                    "text": "Hello, how can I help you?"
                },
                {
                    "role": "USER",
                    "text": "Tell me about yourself"
                }
            ],
            "total": 2
        }
        
        # Test data
        test_data = {
            "apiKey": "test-api-key",
            "callId": "test-call-id",
            "cursor": "test-cursor"
        }
        
        # Make the request
        response = await self.client.post(
            "/api/ultravox/call-messages",
            json=test_data
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["next"], "next-cursor")
        self.assertEqual(len(data["results"]), 2)
        self.assertEqual(data["results"][0]["text"], "Hello, how can I help you?")
        
        # Check that the controller was called correctly
        mock_list_messages.assert_called_once_with("test-api-key", "test-call-id", "test-cursor")
    
    @patch('app.controllers.ultravox_controller.list_call_stages')
    async def test_list_call_stages(self, mock_list_stages):
        """Test listing call stages."""
        # Mock the controller function
        mock_list_stages.return_value = {
            "next": "next-cursor",
            "previous": None,
            "results": [
                {
                    "callId": "test-call-id",
                    "callStageId": "stage-1",
                    "created": "2023-01-01T00:00:00Z"
                },
                {
                    "callId": "test-call-id",
                    "callStageId": "stage-2",
                    "created": "2023-01-01T00:15:00Z"
                }
            ],
            "total": 2
        }
        
        # Test data
        test_data = {
            "apiKey": "test-api-key",
            "callId": "test-call-id",
            "cursor": "test-cursor"
        }
        
        # Make the request
        response = await self.client.post(
            "/api/ultravox/call-stages",
            json=test_data
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["next"], "next-cursor")
        self.assertEqual(len(data["results"]), 2)
        self.assertEqual(data["results"][0]["callStageId"], "stage-1")
        
        # Check that the controller was called correctly
        mock_list_stages.assert_called_once_with("test-api-key", "test-call-id", "test-cursor")
    
    @patch('app.controllers.ultravox_controller.get_call_stage_details')
    async def test_get_call_stage_details(self, mock_get_stage_details):
        """Test getting call stage details."""
        # Mock the controller function
        mock_get_stage_details.return_value = {
            "callId": "test-call-id",
            "callStageId": "test-stage-id",
            "created": "2023-01-01T00:00:00Z",
            "systemPrompt": "Test prompt",
            "model": "test-model"
        }
        
        # Test data
        test_data = {
            "apiKey": "test-api-key",
            "callId": "test-call-id",
            "callStageId": "test-stage-id"
        }
        
        # Make the request
        response = await self.client.post(
            "/api/ultravox/call-stage-details",
            json=test_data
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["callId"], "test-call-id")
        self.assertEqual(data["callStageId"], "test-stage-id")
        self.assertEqual(data["systemPrompt"], "Test prompt")
        
        # Check that the controller was called correctly
        mock_get_stage_details.assert_called_once_with("test-api-key", "test-call-id", "test-stage-id")


if __name__ == "__main__":
    unittest.main()