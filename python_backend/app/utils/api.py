import os
from typing import Optional
from fastapi import Request, HTTPException, status

def get_api_key(request: Request) -> str:
    """
    Get the API key from the request header or environment variable.
    
    Args:
        request: The FastAPI request object
        
    Returns:
        str: The API key
        
    Raises:
        HTTPException: If no API key is available
    """
    # Get API key from request header
    client_api_key = request.headers.get('X-API-Key')
    
    # Use environment variable as fallback
    api_key = os.getenv('ULTRAVOX_API_KEY', '').strip() or client_api_key
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required"
        )
    
    return api_key


def validate_session_id(session_id: Optional[str]) -> None:
    """
    Validate that a session ID is provided.
    
    Args:
        session_id: The session ID to validate
        
    Raises:
        HTTPException: If no session ID is provided
    """
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session ID is required"
        )


def handle_api_error(status_code: int, error_message: str, error_details: Optional[str] = None) -> HTTPException:
    """
    Create a standardized HTTP exception for API errors.
    
    Args:
        status_code: The HTTP status code
        error_message: The main error message
        error_details: Additional error details (optional)
        
    Returns:
        HTTPException: A formatted HTTP exception
    """
    detail = {"error": error_message}
    if error_details:
        detail["details"] = error_details
    
    return HTTPException(
        status_code=status_code,
        detail=detail
    )