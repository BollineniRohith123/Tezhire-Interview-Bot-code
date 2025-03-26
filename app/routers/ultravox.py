import os
import json
import logging
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Request, HTTPException, status, Depends, Query
from fastapi.responses import JSONResponse
import httpx
import traceback

from app.models.ultravox import (
    CallConfig, JoinUrlResponse, ValidateKeyRequest, 
    ValidateKeyResponse, AccountInfo, ErrorResponse, Message
)
from app.utils.api import get_api_key, handle_api_error
from app.utils.ultravox_config import (
    ULTRAVOX_ENDPOINTS, get_default_headers, validate_call_config,
    create_default_call_config, UltravoxConfig
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Timeout settings
DEFAULT_TIMEOUT = 30.0
MESSAGES_TIMEOUT = 10.0
ACCOUNT_TIMEOUT = 10.0

async def make_ultravox_request(
    method: str,
    endpoint: str,
    api_key: str,
    json_data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: float = DEFAULT_TIMEOUT
) -> Dict[str, Any]:
    """
    Make a request to the Ultravox API.
    
    Args:
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint
        api_key: Ultravox API key
        json_data: JSON data for request body (optional)
        params: Query parameters (optional)
        timeout: Request timeout in seconds (optional)
        
    Returns:
        Dict[str, Any]: API response
        
    Raises:
        HTTPException: If the request fails
    """
    headers = get_default_headers(api_key)
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method,
                endpoint,
                headers=headers,
                json=json_data,
                params=params,
                timeout=timeout
            )
            
            logger.info("Ultravox API response: %s", {
                "status": response.status_code,
                "ok": response.is_success,
                "status_text": response.reason_phrase,
                "endpoint": endpoint
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
                
                raise HTTPException(
                    status_code=response.status_code,
                    detail={"error": "Ultravox API error", "details": error_message}
                )
            
            return response.json()
            
    except httpx.TimeoutException:
        logger.error(f"Ultravox API request timed out: {endpoint}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail={"error": "API request timed out", "details": "The Ultravox API did not respond in time"}
        )
    except httpx.RequestError as e:
        logger.error(f"Ultravox API request failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"error": "API request failed", "details": str(e)}
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error in Ultravox API request: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal server error", "details": str(e)}
        )


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
            
            # Validate and sanitize the call configuration
            body = validate_call_config(raw_body)
                
        except ValueError as e:
            logger.error(f"Error validating request body: {str(e)}")
            return JSONResponse(
                content={"error": "Invalid request", "details": str(e)},
                status_code=400
            )
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
        
        # Make request to Ultravox API
        return await make_ultravox_request(
            "POST",
            ULTRAVOX_ENDPOINTS["calls"],
            api_key,
            json_data=body
        )
            
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        logger.error(f"Error in API route: {str(e)}")
        logger.error(traceback.format_exc())
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
        account_info = await make_ultravox_request(
            "GET",
            ULTRAVOX_ENDPOINTS["account"],
            api_key,
            timeout=ACCOUNT_TIMEOUT
        )
        
        return {
            "valid": True,
            "accountInfo": account_info
        }
        
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        logger.error(f"Error validating key: {str(e)}")
        logger.error(traceback.format_exc())
        raise handle_api_error(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Validation failed",
            str(e)
        )


@router.get("/messages", response_model=Dict[str, Any])
async def get_messages(
    request: Request, 
    call_id: str = Query(..., description="The ID of the call to fetch messages for")
):
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
        
        # Format the messages endpoint with the call ID
        endpoint = ULTRAVOX_ENDPOINTS["messages"].format(call_id=call_id)
        
        # Make request to Ultravox API
        return await make_ultravox_request(
            "GET",
            endpoint,
            api_key,
            timeout=MESSAGES_TIMEOUT
        )
        
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        logger.error(f"Error in API route: {str(e)}")
        logger.error(traceback.format_exc())
        raise handle_api_error(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Internal server error",
            str(e)
        )


@router.post("/create-with-defaults", response_model=Dict[str, Any])
async def create_call_with_defaults(
    request: Request,
    system_prompt: str = Query(..., description="The system prompt for the call"),
    model: Optional[str] = Query(None, description="The model to use"),
    voice: Optional[str] = Query(None, description="The voice to use"),
    max_duration: Optional[str] = Query(None, description="Maximum duration in seconds"),
    temperature: Optional[float] = Query(None, description="Temperature for model generation")
):
    """
    Create a new Ultravox call with default settings.
    """
    try:
        # Get API key
        api_key = get_api_key(request)
        
        # Create default call configuration
        kwargs = {}
        if model:
            kwargs["model"] = model
        if voice:
            kwargs["voice"] = voice
        if max_duration:
            kwargs["maxDuration"] = max_duration
        if temperature is not None:
            kwargs["temperature"] = temperature
            
        call_config = create_default_call_config(system_prompt, **kwargs)
        
        # Make request to Ultravox API
        return await make_ultravox_request(
            "POST",
            ULTRAVOX_ENDPOINTS["calls"],
            api_key,
            json_data=call_config
        )
        
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except ValueError as e:
        # Handle validation errors
        logger.error(f"Error validating call configuration: {str(e)}")
        return JSONResponse(
            content={"error": "Invalid request", "details": str(e)},
            status_code=400
        )
    except Exception as e:
        logger.error(f"Error in API route: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            content={
                "error": "Internal server error",
                "details": str(e)
            },
            status_code=500
        )


@router.get("/health", response_model=Dict[str, Any])
async def ultravox_health_check(request: Request):
    """
    Check the health of the Ultravox API.
    """
    try:
        # Get API key
        api_key = get_api_key(request)
        
        # Check account info as a health check
        await make_ultravox_request(
            "GET",
            ULTRAVOX_ENDPOINTS["account"],
            api_key,
            timeout=ACCOUNT_TIMEOUT
        )
        
        return {
            "status": "healthy",
            "message": "Ultravox API is operational"
        }
        
    except HTTPException as e:
        # Return unhealthy status with error details
        status_code = e.status_code
        detail = e.detail
        
        return JSONResponse(
            content={
                "status": "unhealthy",
                "message": "Ultravox API is not operational",
                "error": detail.get("error") if isinstance(detail, dict) else str(detail),
                "status_code": status_code
            },
            status_code=200  # Always return 200 for health checks
        )
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        logger.error(traceback.format_exc())
        
        return JSONResponse(
            content={
                "status": "unhealthy",
                "message": "Ultravox API is not operational",
                "error": str(e)
            },
            status_code=200  # Always return 200 for health checks
        )