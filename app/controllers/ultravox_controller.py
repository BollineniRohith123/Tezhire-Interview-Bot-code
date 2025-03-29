import httpx
from fastapi import HTTPException
from typing import Dict, Any, Optional

async def join_ultravox_call(api_key: str, call_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a new Ultravox call and returns the join URL.
    
    Parameters:
    - api_key: Ultravox API key for authentication
    - call_config: Configuration for the Ultravox call
    """
    try:
        # Create the Ultravox call
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.ultravox.ai/api/calls",
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": api_key,
                },
                json=call_config,
                timeout=30.0  # Set an appropriate timeout
            )
            
            # Check if the response is successful
            if response.status_code not in [200, 201]:
                error_text = response.text
                raise HTTPException(
                    status_code=response.status_code, 
                    detail=f"Failed to create Ultravox call: {error_text}"
                )
            
            # Parse the response
            data = response.json()
            
            # Return the join URL and call ID
            return {
                "joinUrl": data.get("joinUrl", ""),
                "callId": data.get("callId", None),
                "created": data.get("created", None)
            }
            
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

async def get_call_details(api_key: str, call_id: str) -> Dict[str, Any]:
    """
    Retrieves detailed information about a specific Ultravox call.
    
    Parameters:
    - api_key: Ultravox API key for authentication
    - call_id: Unique identifier of the call to retrieve
    """
    try:
        # Fetch the call details
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.ultravox.ai/api/calls/{call_id}",
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": api_key,
                },
                timeout=30.0  # Set an appropriate timeout
            )
            
            # Check if the response is successful
            if response.status_code != 200:
                error_text = response.text
                raise HTTPException(
                    status_code=response.status_code, 
                    detail=f"Failed to retrieve call details: {error_text}"
                )
            
            # Parse the response
            data = response.json()
            
            # Return the call details
            return data
            
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

async def create_ultravox_call(api_key: str, call_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a new Ultravox call with comprehensive configuration options.
    
    Parameters:
    - api_key: Ultravox API key for authentication
    - call_config: Comprehensive call configuration parameters
    """
    try:
        # Create the Ultravox call
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.ultravox.ai/api/calls",
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": api_key,
                },
                json=call_config,
                timeout=30.0  # Set an appropriate timeout
            )
            
            # Check if the response is successful
            if response.status_code not in [200, 201]:
                error_text = response.text
                raise HTTPException(
                    status_code=response.status_code, 
                    detail=f"Failed to create Ultravox call: {error_text}"
                )
            
            # Parse the response
            data = response.json()
            
            # Return the call details
            return data
            
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

async def list_ultravox_calls(api_key: str, cursor: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieves a list of all Ultravox calls associated with the API key.
    
    Parameters:
    - api_key: Ultravox API key for authentication
    - cursor: Optional pagination cursor for fetching next page of results
    """
    try:
        # Prepare the URL with optional cursor parameter
        url = "https://api.ultravox.ai/api/calls"
        params = {}
        if cursor:
            params["cursor"] = cursor
            
        # Fetch the list of calls
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                params=params,
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": api_key,
                },
                timeout=30.0  # Set an appropriate timeout
            )
            
            # Check if the response is successful
            if response.status_code != 200:
                error_text = response.text
                raise HTTPException(
                    status_code=response.status_code, 
                    detail=f"Failed to list Ultravox calls: {error_text}"
                )
            
            # Parse the response
            data = response.json()
            
            # Return the list of calls
            return data
            
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

async def list_call_messages(api_key: str, call_id: str, cursor: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieves a list of messages for a specific Ultravox call.
    
    Parameters:
    - api_key: Ultravox API key for authentication
    - call_id: Unique identifier of the call to retrieve messages for
    - cursor: Optional pagination cursor for fetching next page of results
    """
    try:
        # Prepare the URL with optional cursor parameter
        url = f"https://api.ultravox.ai/api/calls/{call_id}/messages"
        params = {}
        if cursor:
            params["cursor"] = cursor
            
        # Fetch the list of call messages
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                params=params,
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": api_key,
                },
                timeout=30.0  # Set an appropriate timeout
            )
            
            # Check if the response is successful
            if response.status_code != 200:
                error_text = response.text
                raise HTTPException(
                    status_code=response.status_code, 
                    detail=f"Failed to list call messages: {error_text}"
                )
            
            # Parse the response
            data = response.json()
            
            # Return the list of call messages
            return data
            
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

async def list_call_stages(api_key: str, call_id: str, cursor: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieves a list of stages for a specific Ultravox call.
    
    Parameters:
    - api_key: Ultravox API key for authentication
    - call_id: Unique identifier of the call to retrieve stages for
    - cursor: Optional pagination cursor for fetching next page of results
    """
    try:
        # Prepare the URL with optional cursor parameter
        url = f"https://api.ultravox.ai/api/calls/{call_id}/stages"
        params = {}
        if cursor:
            params["cursor"] = cursor
            
        # Fetch the list of call stages
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                params=params,
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": api_key,
                },
                timeout=30.0  # Set an appropriate timeout
            )
            
            # Check if the response is successful
            if response.status_code != 200:
                error_text = response.text
                raise HTTPException(
                    status_code=response.status_code, 
                    detail=f"Failed to list call stages: {error_text}"
                )
            
            # Parse the response
            data = response.json()
            
            # Return the list of call stages
            return data
            
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

async def get_call_stage_details(api_key: str, call_id: str, call_stage_id: str) -> Dict[str, Any]:
    """
    Retrieves detailed information about a specific call stage.
    
    Parameters:
    - api_key: Ultravox API key for authentication
    - call_id: Unique identifier of the call
    - call_stage_id: Unique identifier of the call stage to retrieve
    """
    try:
        # Prepare payload with API key, call ID, and call stage ID
        payload = {
            "apiKey": api_key,
            "callId": call_id,
            "callStageId": call_stage_id
        }
            
        # Fetch the call stage details
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://prod-voice-pgaenaxiea-uc.a.run.app/ultravox/call-stage-details",
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30.0  # Set an appropriate timeout
            )
            
            # Check if the response is successful
            if response.status_code != 200:
                error_text = response.text
                raise HTTPException(
                    status_code=response.status_code, 
                    detail=f"Failed to retrieve call stage details: {error_text}"
                )
            
            # Parse the response
            data = response.json()
            
            # Return the call stage details
            return data
            
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")