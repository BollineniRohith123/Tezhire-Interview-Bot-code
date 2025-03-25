import os
import json
import logging
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
import httpx

from app.models.ultravox import (
    CallConfig, JoinUrlResponse, ValidateKeyRequest, 
    ValidateKeyResponse, AccountInfo, ErrorResponse
)
from app.utils.api import get_api_key, handle_api_error

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# List of valid fields for Ultravox API
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
    'experimentalSettings'
]

@router.post("/", response_model=Dict[str, Any])
async def create_call(request: Request):
    """
    Create a new Ultravox call.
    """
    # Handle CORS preflight request
    if request.method == "OPTIONS":
        return JSONResponse(
            content={},
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization, X-API-Key",
            },
        )
    
    try:
        # Get API key
        api_key = get_api_key(request)
        
        # Debug log environment variables
        logger.info("Environment check: %s", {
            "node_env": os.getenv("NODE_ENV"),
            "has_api_key": bool(os.getenv("ULTRAVOX_API_KEY")),
            "has_client_api_key": bool(request.headers.get("X-API-Key")),
            "api_key_length": len(os.getenv("ULTRAVOX_API_KEY", "")) if os.getenv("ULTRAVOX_API_KEY") else 0
        })
        
        # Validate request body
        try:
            raw_body = await request.json()
            
            # Type-safe body construction with field validation
            sanitized_body: Dict[str, Any] = {}
            
            for key, value in raw_body.items():
                if key in VALID_FIELDS:
                    # Type checking for each field
                    if key in ['systemPrompt', 'model', 'voice', 'languageHint', 'maxDuration', 'timeExceededMessage']:
                        if isinstance(value, str):
                            sanitized_body[key] = value
                    elif key == 'temperature':
                        if isinstance(value, (int, float)):
                            sanitized_body[key] = value
                    elif key in ['selectedTools', 'initialMessages', 'inactivityMessages']:
                        if isinstance(value, list):
                            sanitized_body[key] = value
                    elif key in ['recordingEnabled', 'transcriptOptional']:
                        if isinstance(value, bool):
                            sanitized_body[key] = value
            
            # Ensure required fields are present
            if 'systemPrompt' not in sanitized_body:
                raise ValueError("System prompt is required")
            
            body = sanitized_body
            
            # Ensure maxDuration has 's' suffix
            if 'maxDuration' in body and not body['maxDuration'].endswith('s'):
                body['maxDuration'] = f"{body['maxDuration']}s"
                
        except Exception as e:
            logger.error(f"Error parsing request body: {str(e)}")
            return JSONResponse(
                content={"error": "Invalid request", "details": "Invalid request body format"},
                status_code=400
            )
        
        logger.info("Making API request to Ultravox with config: %s", {
            "has_system_prompt": bool(body.get("systemPrompt")),
            "model": body.get("model"),
            "max_duration": body.get("maxDuration")
        })
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    'https://api.ultravox.ai/api/calls',
                    headers={
                        'Content-Type': 'application/json',
                        'X-API-Key': api_key,
                        'Accept': 'application/json',
                        'User-Agent': 'Ultravox-Client/1.0',
                    },
                    json={
                        **body,
                        "model": body.get("model", "fixie-ai/ultravox-70B"),
                    },
                    timeout=30.0
                )
            
            logger.info("Ultravox API response: %s", {
                "status": response.status_code,
                "ok": response.is_success,
                "status_text": response.reason_phrase
            })
            
            if not response.is_success:
                error_text = response.text
                logger.error(f"Ultravox API error response: {error_text}")
                
                try:
                    error_json = response.json()
                    error_message = error_json.get("error") or error_json.get("message") or error_text
                except:
                    # Use raw error text if parsing fails
                    error_message = error_text
                
                return JSONResponse(
                    content={"error": "Ultravox API error", "details": error_message},
                    status_code=response.status_code
                )
            
            data = response.json()
            return data
            
        except Exception as e:
            logger.error(f"Ultravox API call failed: {str(e)}")
            return JSONResponse(
                content={
                    "error": "API request failed",
                    "details": str(e)
                },
                status_code=500
            )
            
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        logger.error(f"Error in API route: {str(e)}")
        return JSONResponse(
            content={
                "error": "Internal server error",
                "details": str(e)
            },
            status_code=500
        )


@router.post("/validate-key", response_model=ValidateKeyResponse)
async def validate_key(request: ValidateKeyRequest):
    """
    Validate an Ultravox API key.
    """
    try:
        api_key = request.api_key
        
        if not api_key:
            raise handle_api_error(
                status.HTTP_400_BAD_REQUEST,
                "Security key is required"
            )
        
        # Validate by fetching account info
        async with httpx.AsyncClient() as client:
            response = await client.get(
                'https://api.ultravox.ai/api/accounts/me',
                headers={
                    'Content-Type': 'application/json',
                    'X-API-Key': api_key,
                },
                timeout=10.0
            )
        
        if not response.is_success:
            raise handle_api_error(
                status.HTTP_401_UNAUTHORIZED,
                "Invalid security key"
            )
        
        account_info = response.json()
        return {
            "valid": True,
            "accountInfo": account_info
        }
        
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        logger.error(f"Error validating key: {str(e)}")
        raise handle_api_error(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Validation failed",
            str(e)
        )


@router.get("/messages", response_model=Dict[str, Any])
async def get_messages(request: Request, call_id: str):
    """
    Get messages for a specific call.
    """
    try:
        if not call_id:
            raise handle_api_error(
                status.HTTP_400_BAD_REQUEST,
                "Call ID is required"
            )
        
        # Get API key
        api_key = get_api_key(request)
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f'https://api.ultravox.ai/api/calls/{call_id}/messages',
                headers={
                    'Content-Type': 'application/json',
                    'X-API-Key': api_key,
                    'Accept': 'application/json',
                },
                timeout=10.0
            )
        
        if not response.is_success:
            error_text = response.text
            
            try:
                error_json = response.json()
                error_message = error_json.get("error") or error_json.get("message") or error_text
            except:
                # Use raw error text if parsing fails
                error_message = error_text
            
            raise handle_api_error(
                response.status_code,
                "Failed to fetch messages",
                error_message
            )
        
        data = response.json()
        return data
        
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        logger.error(f"Error in API route: {str(e)}")
        raise handle_api_error(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Internal server error",
            str(e)
        )