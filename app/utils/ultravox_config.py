"""
Ultravox configuration module.

This module provides centralized configuration for Ultravox API integration,
including API endpoints, default values, and utility functions.
"""
import os
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

# Ultravox API base URL
ULTRAVOX_API_BASE_URL = "https://api.ultravox.ai/api"

# Ultravox API endpoints
ULTRAVOX_ENDPOINTS = {
    "calls": f"{ULTRAVOX_API_BASE_URL}/calls",
    "messages": f"{ULTRAVOX_API_BASE_URL}/calls/{{call_id}}/messages",
    "account": f"{ULTRAVOX_API_BASE_URL}/accounts/me",
}

# Default Ultravox model
DEFAULT_ULTRAVOX_MODEL = "fixie-ai/ultravox-70B"

# Default voice
DEFAULT_VOICE = "echo"

# Default language
DEFAULT_LANGUAGE = "en-US"

# Default max duration (30 minutes)
DEFAULT_MAX_DURATION = "1800s"

# Valid fields for Ultravox API
VALID_FIELDS = [
    'systemPrompt',
    'temperature',
    'model',
    'voice',
    'languageHint',
    'initialMessages',
    'joinTimeout',
    'maxDuration',
    'timeExceededMessage',
    'inactivityMessages',
    'selectedTools',
    'medium',
    'recordingEnabled',
    'firstSpeaker',
    'transcriptOptional',
    'initialOutputMedium',
    'vadSettings',
    'firstSpeakerSettings',
    'experimentalSettings',
    'interactionConfig'
]

# Field type mapping for validation
FIELD_TYPES = {
    'systemPrompt': str,
    'model': str,
    'voice': str,
    'languageHint': str,
    'maxDuration': str,
    'timeExceededMessage': str,
    'temperature': (int, float),
    'selectedTools': list,
    'initialMessages': list,
    'inactivityMessages': list,
    'recordingEnabled': bool,
    'transcriptOptional': bool,
    'medium': str,
    'firstSpeaker': str,
    'initialOutputMedium': str,
    'vadSettings': dict,
    'firstSpeakerSettings': dict,
    'experimentalSettings': dict,
    'interactionConfig': dict,
    'joinTimeout': str
}

# Required fields
REQUIRED_FIELDS = ['systemPrompt']

class UltravoxConfig(BaseModel):
    """Ultravox configuration model."""
    api_key: Optional[str] = None
    model: str = DEFAULT_ULTRAVOX_MODEL
    voice: str = DEFAULT_VOICE
    language_hint: str = DEFAULT_LANGUAGE
    max_duration: str = DEFAULT_MAX_DURATION
    temperature: float = 0.7
    recording_enabled: bool = True
    
    @classmethod
    def from_env(cls) -> 'UltravoxConfig':
        """
        Create a configuration instance from environment variables.
        
        Returns:
            UltravoxConfig: Configuration instance
        """
        return cls(
            api_key=os.getenv('ULTRAVOX_API_KEY', '').strip(),
            model=os.getenv('ULTRAVOX_MODEL', DEFAULT_ULTRAVOX_MODEL),
            voice=os.getenv('ULTRAVOX_VOICE', DEFAULT_VOICE),
            language_hint=os.getenv('ULTRAVOX_LANGUAGE', DEFAULT_LANGUAGE),
            max_duration=os.getenv('ULTRAVOX_MAX_DURATION', DEFAULT_MAX_DURATION),
            temperature=float(os.getenv('ULTRAVOX_TEMPERATURE', '0.7')),
            recording_enabled=os.getenv('ULTRAVOX_RECORDING_ENABLED', 'True').lower() == 'true'
        )

def get_default_headers(api_key: str) -> Dict[str, str]:
    """
    Get default headers for Ultravox API requests.
    
    Args:
        api_key: The API key to use
        
    Returns:
        Dict[str, str]: Headers dictionary
    """
    return {
        'Content-Type': 'application/json',
        'X-API-Key': api_key,
        'Accept': 'application/json',
        'User-Agent': 'Ultravox-Client/1.0',
    }

def validate_call_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and sanitize a call configuration.
    
    Args:
        config: The call configuration to validate
        
    Returns:
        Dict[str, Any]: Sanitized configuration
        
    Raises:
        ValueError: If the configuration is invalid
    """
    sanitized_config: Dict[str, Any] = {}
    
    # Validate and sanitize fields
    for key, value in config.items():
        if key in VALID_FIELDS:
            expected_type = FIELD_TYPES.get(key)
            if expected_type and isinstance(value, expected_type):
                sanitized_config[key] = value
            else:
                raise ValueError(f"Invalid type for field '{key}'. Expected {expected_type}, got {type(value)}")
    
    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in sanitized_config:
            raise ValueError(f"Required field '{field}' is missing")
    
    # Ensure maxDuration has 's' suffix
    if 'maxDuration' in sanitized_config and not sanitized_config['maxDuration'].endswith('s'):
        sanitized_config['maxDuration'] = f"{sanitized_config['maxDuration']}s"
    
    return sanitized_config

def create_default_call_config(system_prompt: str, **kwargs) -> Dict[str, Any]:
    """
    Create a default call configuration with the given system prompt.
    
    Args:
        system_prompt: The system prompt to use
        **kwargs: Additional configuration options
        
    Returns:
        Dict[str, Any]: Call configuration
    """
    config = UltravoxConfig.from_env()
    
    call_config = {
        "systemPrompt": system_prompt,
        "model": config.model,
        "voice": config.voice,
        "languageHint": config.language_hint,
        "maxDuration": config.max_duration,
        "temperature": config.temperature,
        "recordingEnabled": config.recording_enabled,
    }
    
    # Override with any provided kwargs
    call_config.update(kwargs)
    
    return validate_call_config(call_config)