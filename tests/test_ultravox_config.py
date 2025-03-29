"""
Tests for the Ultravox configuration module.
"""
import os
import unittest
from unittest.mock import patch
from typing import Dict, Any

from app.utils.ultravox_config import (
    UltravoxConfig, validate_call_config, create_default_call_config,
    get_default_headers, create_api_payload, VALID_FIELDS, REQUIRED_FIELDS
)


class TestUltravoxConfig(unittest.TestCase):
    """Test cases for the UltravoxConfig class."""
    
    def test_default_values(self):
        """Test that default values are set correctly."""
        config = UltravoxConfig()
        self.assertIsNone(config.api_key)
        self.assertEqual(config.model, "fixie-ai/ultravox-70B")
        self.assertEqual(config.voice, "echo")
        self.assertEqual(config.language_hint, "en-US")
        self.assertEqual(config.max_duration, "1800s")
        self.assertEqual(config.temperature, 0.7)
        self.assertTrue(config.recording_enabled)
    
    @patch.dict(os.environ, {
        "ULTRAVOX_API_KEY": "test-api-key",
        "ULTRAVOX_MODEL": "test-model",
        "ULTRAVOX_VOICE": "test-voice",
        "ULTRAVOX_LANGUAGE": "fr-FR",
        "ULTRAVOX_MAX_DURATION": "900s",
        "ULTRAVOX_TEMPERATURE": "0.5",
        "ULTRAVOX_RECORDING_ENABLED": "false"
    })
    def test_from_env(self):
        """Test that environment variables are loaded correctly."""
        config = UltravoxConfig.from_env()
        self.assertEqual(config.api_key, "test-api-key")
        self.assertEqual(config.model, "test-model")
        self.assertEqual(config.voice, "test-voice")
        self.assertEqual(config.language_hint, "fr-FR")
        self.assertEqual(config.max_duration, "900s")
        self.assertEqual(config.temperature, 0.5)
        self.assertFalse(config.recording_enabled)


class TestValidateCallConfig(unittest.TestCase):
    """Test cases for the validate_call_config function."""
    
    def test_valid_config(self):
        """Test that a valid configuration passes validation."""
        config = {
            "systemPrompt": "Test prompt",
            "model": "test-model",
            "voice": "test-voice",
            "temperature": 0.7,
            "maxDuration": "1800s"
        }
        
        result = validate_call_config(config)
        self.assertEqual(result["systemPrompt"], "Test prompt")
        self.assertEqual(result["model"], "test-model")
        self.assertEqual(result["voice"], "test-voice")
        self.assertEqual(result["temperature"], 0.7)
        self.assertEqual(result["maxDuration"], "1800s")
    
    def test_missing_required_field(self):
        """Test that missing required fields raise an error."""
        config = {
            "model": "test-model",
            "voice": "test-voice"
        }
        
        with self.assertRaises(ValueError) as context:
            validate_call_config(config)
        
        self.assertIn("systemPrompt", str(context.exception))
    
    def test_invalid_field_type(self):
        """Test that invalid field types raise an error."""
        config = {
            "systemPrompt": "Test prompt",
            "temperature": "not a number"
        }
        
        with self.assertRaises(ValueError) as context:
            validate_call_config(config)
        
        self.assertIn("temperature", str(context.exception))
    
    def test_max_duration_suffix(self):
        """Test that maxDuration gets 's' suffix if missing."""
        config = {
            "systemPrompt": "Test prompt",
            "maxDuration": "1800"
        }
        
        result = validate_call_config(config)
        self.assertEqual(result["maxDuration"], "1800s")


class TestCreateDefaultCallConfig(unittest.TestCase):
    """Test cases for the create_default_call_config function."""
    
    def test_create_with_defaults(self):
        """Test creating a configuration with defaults."""
        result = create_default_call_config("Test prompt")
        
        self.assertEqual(result["systemPrompt"], "Test prompt")
        self.assertEqual(result["model"], "fixie-ai/ultravox-70B")
        self.assertEqual(result["voice"], "echo")
        self.assertEqual(result["languageHint"], "en-US")
        self.assertEqual(result["maxDuration"], "1800s")
        self.assertEqual(result["temperature"], 0.7)
        self.assertTrue(result["recordingEnabled"])
    
    def test_create_with_overrides(self):
        """Test creating a configuration with overrides."""
        result = create_default_call_config(
            "Test prompt",
            model="custom-model",
            voice="custom-voice",
            temperature=0.5
        )
        
        self.assertEqual(result["systemPrompt"], "Test prompt")
        self.assertEqual(result["model"], "custom-model")
        self.assertEqual(result["voice"], "custom-voice")
        self.assertEqual(result["temperature"], 0.5)


class TestGetDefaultHeaders(unittest.TestCase):
    """Test cases for the get_default_headers function."""
    
    def test_headers(self):
        """Test that headers are generated correctly."""
        headers = get_default_headers()
        
        self.assertEqual(headers["Content-Type"], "application/json")
        self.assertEqual(headers["Accept"], "application/json")
        self.assertEqual(headers["User-Agent"], "Ultravox-Client/1.0")


class TestCreateApiPayload(unittest.TestCase):
    """Test cases for the create_api_payload function."""
    
    def test_create_payload_with_api_key_only(self):
        """Test creating a payload with only the API key."""
        payload = create_api_payload("test-api-key")
        
        self.assertEqual(payload["apiKey"], "test-api-key")
        self.assertEqual(len(payload), 1)
    
    def test_create_payload_with_additional_params(self):
        """Test creating a payload with additional parameters."""
        payload = create_api_payload(
            "test-api-key",
            callId="test-call-id",
            cursor="test-cursor"
        )
        
        self.assertEqual(payload["apiKey"], "test-api-key")
        self.assertEqual(payload["callId"], "test-call-id")
        self.assertEqual(payload["cursor"], "test-cursor")
        self.assertEqual(len(payload), 3)


if __name__ == "__main__":
    unittest.main()