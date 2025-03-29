from fastapi import APIRouter, HTTPException
from app.models.ultravox_models import (
    UltravoxCallConfig, UltravoxResponse, CallDetailsRequest, 
    CallDetailsResponse, CreateUltravoxCallRequest, ListCallsRequest, 
    ListCallsResponse, ListCallMessagesRequest, ListCallMessagesResponse,
    ListCallStagesRequest, ListCallStagesResponse, GetCallStageRequest, CallStage
)
from app.controllers.ultravox_controller import (
    join_ultravox_call as controller_join_ultravox_call,
    get_call_details as controller_get_call_details,
    create_ultravox_call as controller_create_ultravox_call,
    list_ultravox_calls as controller_list_ultravox_calls,
    list_call_messages as controller_list_call_messages,
    list_call_stages as controller_list_call_stages,
    get_call_stage_details as controller_get_call_stage_details
)

router = APIRouter(prefix="/ultravox", tags=["Ultravox"])

@router.post("/join", response_model=UltravoxResponse)
async def join_ultravox_call(config: UltravoxCallConfig):
    """
    Creates a new Ultravox call and returns the join URL.
    
    Parameters:
    - apiKey: Ultravox API key for authentication
    - systemPrompt: Custom system prompt for the AI assistant
    - model: Ultravox model to use
    - languageHint: Language hint for the assistant
    - voice: Voice to use for the assistant
    - temperature: Temperature parameter for model responses
    """
    # Extract API key from request
    api_key = config.apiKey
    
    # Remove API key from config before sending to Ultravox
    call_config = config.dict(exclude={'apiKey'})
    
    # Call the controller function
    return await controller_join_ultravox_call(api_key, call_config)

@router.post("/call-details", response_model=CallDetailsResponse)
async def get_call_details(request: CallDetailsRequest):
    """
    Retrieves detailed information about a specific Ultravox call.
    
    Parameters:
    - apiKey: Ultravox API key for authentication
    - callId: Unique identifier of the call to retrieve
    """
    # Extract API key and call ID from request
    api_key = request.apiKey
    call_id = request.callId
    
    # Call the controller function
    return await controller_get_call_details(api_key, call_id)

@router.post("/create-call", response_model=CallDetailsResponse)
async def create_ultravox_call(request: CreateUltravoxCallRequest):
    """
    Creates a new Ultravox call with comprehensive configuration options.
    
    Parameters:
    - Comprehensive call configuration parameters
    - apiKey: Ultravox API key for authentication
    """
    # Extract API key from request
    api_key = request.apiKey
    
    # Remove API key from config before sending to Ultravox
    call_config = request.dict(exclude={'apiKey'})
    
    # Call the controller function
    return await controller_create_ultravox_call(api_key, call_config)

@router.post("/list-calls", response_model=ListCallsResponse)
async def list_ultravox_calls(request: ListCallsRequest):
    """
    Retrieves a list of all Ultravox calls associated with the API key.
    
    Parameters:
    - apiKey: Ultravox API key for authentication
    - cursor: Optional pagination cursor for fetching next page of results
    """
    # Extract API key and cursor from request
    api_key = request.apiKey
    cursor = request.cursor
    
    # Call the controller function
    return await controller_list_ultravox_calls(api_key, cursor)

@router.post("/call-messages", response_model=ListCallMessagesResponse)
async def list_call_messages(request: ListCallMessagesRequest):
    """
    Retrieves a list of messages for a specific Ultravox call.
    
    Parameters:
    - apiKey: Ultravox API key for authentication
    - callId: Unique identifier of the call to retrieve messages for
    - cursor: Optional pagination cursor for fetching next page of results
    """
    # Extract API key, call ID, and cursor from request
    api_key = request.apiKey
    call_id = request.callId
    cursor = request.cursor
    
    # Call the controller function
    return await controller_list_call_messages(api_key, call_id, cursor)

@router.post("/call-stages", response_model=ListCallStagesResponse)
async def list_call_stages(request: ListCallStagesRequest):
    """
    Retrieves a list of stages for a specific Ultravox call.
    
    Parameters:
    - apiKey: Ultravox API key for authentication
    - callId: Unique identifier of the call to retrieve stages for
    - cursor: Optional pagination cursor for fetching next page of results
    """
    # Extract API key, call ID, and cursor from request
    api_key = request.apiKey
    call_id = request.callId
    cursor = request.cursor
    
    # Call the controller function
    return await controller_list_call_stages(api_key, call_id, cursor)

@router.post("/call-stage-details", response_model=CallStage)
async def get_call_stage_details(request: GetCallStageRequest):
    """
    Retrieves detailed information about a specific call stage.
    
    Parameters:
    - apiKey: Ultravox API key for authentication
    - callId: Unique identifier of the call
    - callStageId: Unique identifier of the call stage to retrieve
    """
    # Extract API key, call ID, and call stage ID from request
    api_key = request.apiKey
    call_id = request.callId
    call_stage_id = request.callStageId
    
    # Call the controller function
    return await controller_get_call_stage_details(api_key, call_id, call_stage_id)