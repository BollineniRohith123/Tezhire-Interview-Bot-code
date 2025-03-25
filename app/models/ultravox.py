from typing import List, Dict, Optional, Any, Union, Literal
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime


class RoleEnum(str, Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    TOOL_CALL = "TOOL_CALL"
    TOOL_RESULT = "TOOL_RESULT"


class ParameterLocation(str, Enum):
    UNSPECIFIED = "PARAMETER_LOCATION_UNSPECIFIED"
    QUERY = "PARAMETER_LOCATION_QUERY"
    PATH = "PARAMETER_LOCATION_PATH"
    HEADER = "PARAMETER_LOCATION_HEADER"
    BODY = "PARAMETER_LOCATION_BODY"


class KnownParamEnum(str, Enum):
    UNSPECIFIED = "KNOWN_PARAM_UNSPECIFIED"
    CALL_ID = "KNOWN_PARAM_CALL_ID"
    CONVERSATION_HISTORY = "KNOWN_PARAM_CONVERSATION_HISTORY"


class Message(BaseModel):
    ordinal: Optional[int] = None
    role: RoleEnum
    text: str
    invocation_id: Optional[str] = Field(None, alias="invocationId")
    tool_name: Optional[str] = Field(None, alias="toolName")


class DynamicParameter(BaseModel):
    name: str
    location: ParameterLocation
    schema: Dict[str, Any]
    required: Optional[bool] = None


class StaticParameter(BaseModel):
    name: str
    location: ParameterLocation
    value: Any


class AutomaticParameter(BaseModel):
    name: str
    location: ParameterLocation
    known_value: KnownParamEnum = Field(..., alias="knownValue")


class QueryApiKeyRequirement(BaseModel):
    name: str


class HeaderApiKeyRequirement(BaseModel):
    name: str


class HttpAuthRequirement(BaseModel):
    scheme: str


class SecurityRequirement(BaseModel):
    query_api_key: Optional[QueryApiKeyRequirement] = Field(None, alias="queryApiKey")
    header_api_key: Optional[HeaderApiKeyRequirement] = Field(None, alias="headerApiKey")
    http_auth: Optional[HttpAuthRequirement] = Field(None, alias="httpAuth")


class SecurityRequirements(BaseModel):
    requirements: Dict[str, SecurityRequirement]


class SecurityOptions(BaseModel):
    options: List[SecurityRequirements]


class ToolRequirements(BaseModel):
    http_security_options: SecurityOptions = Field(..., alias="httpSecurityOptions")
    required_parameter_overrides: List[str] = Field(..., alias="requiredParameterOverrides")


class BaseHttpToolDetails(BaseModel):
    base_url_pattern: str = Field(..., alias="baseUrlPattern")
    http_method: str = Field(..., alias="httpMethod")


class BaseToolDefinition(BaseModel):
    model_tool_name: Optional[str] = Field(None, alias="modelToolName")
    description: str
    dynamic_parameters: Optional[List[DynamicParameter]] = Field(None, alias="dynamicParameters")
    static_parameters: Optional[List[StaticParameter]] = Field(None, alias="staticParameters")
    automatic_parameters: Optional[List[AutomaticParameter]] = Field(None, alias="automaticParameters")
    requirements: Optional[ToolRequirements] = None
    http: Optional[BaseHttpToolDetails] = None
    client: Optional[Dict[str, Any]] = None


class SelectedTool(BaseModel):
    tool_id: Optional[str] = Field(None, alias="toolId")
    tool_name: Optional[str] = Field(None, alias="toolName")
    temporary_tool: Optional[BaseToolDefinition] = Field(None, alias="temporaryTool")
    name_override: Optional[str] = Field(None, alias="nameOverride")
    auth_tokens: Optional[Dict[str, str]] = Field(None, alias="authTokens")
    parameter_overrides: Optional[Dict[str, Any]] = Field(None, alias="parameterOverrides")


class VadSettings(BaseModel):
    min_silence_duration: Optional[float] = Field(None, alias="minSilenceDuration")
    max_silence_duration: Optional[float] = Field(None, alias="maxSilenceDuration")
    silence_threshold: Optional[float] = Field(None, alias="silenceThreshold")


class FirstSpeakerSettings(BaseModel):
    allow_interruptions: Optional[bool] = Field(None, alias="allowInterruptions")
    wait_for_user_response: Optional[bool] = Field(None, alias="waitForUserResponse")


class ExperimentalSettings(BaseModel):
    allowed_response_duration: Optional[str] = Field(None, alias="allowedResponseDuration")
    max_response_duration: Optional[str] = Field(None, alias="maxResponseDuration")


class InteractionConfig(BaseModel):
    allow_interruptions: Optional[bool] = Field(None, alias="allowInterruptions")
    min_silence_threshold: Optional[float] = Field(None, alias="minSilenceThreshold")
    max_silence_threshold: Optional[float] = Field(None, alias="maxSilenceThreshold")


class CallConfig(BaseModel):
    system_prompt: str = Field(..., alias="systemPrompt")
    temperature: Optional[float] = None
    model: Optional[str] = None
    voice: Optional[str] = None
    language_hint: Optional[str] = Field(None, alias="languageHint")
    initial_messages: Optional[List[Message]] = Field(None, alias="initialMessages")
    join_timeout: Optional[str] = Field(None, alias="joinTimeout")
    max_duration: Optional[str] = Field(None, alias="maxDuration")
    time_exceeded_message: Optional[str] = Field(None, alias="timeExceededMessage")
    inactivity_messages: Optional[List[str]] = Field(None, alias="inactivityMessages")
    selected_tools: Optional[List[SelectedTool]] = Field(None, alias="selectedTools")
    medium: Optional[str] = None
    recording_enabled: Optional[bool] = Field(None, alias="recordingEnabled")
    first_speaker: Optional[str] = Field(None, alias="firstSpeaker")
    transcript_optional: Optional[bool] = Field(None, alias="transcriptOptional")
    initial_output_medium: Optional[str] = Field(None, alias="initialOutputMedium")
    vad_settings: Optional[VadSettings] = Field(None, alias="vadSettings")
    first_speaker_settings: Optional[FirstSpeakerSettings] = Field(None, alias="firstSpeakerSettings")
    experimental_settings: Optional[ExperimentalSettings] = Field(None, alias="experimentalSettings")
    interaction_config: Optional[InteractionConfig] = Field(None, alias="interactionConfig")


class JoinUrlResponse(BaseModel):
    call_id: str = Field(..., alias="callId")
    created: datetime
    ended: Optional[datetime] = None
    model: str
    system_prompt: str = Field(..., alias="systemPrompt")
    temperature: float
    join_url: str = Field(..., alias="joinUrl")


class DemoConfig(BaseModel):
    title: str
    overview: str
    session_id: str = Field(..., alias="sessionId")
    call_config: CallConfig = Field(..., alias="callConfig")


class AccountInfo(BaseModel):
    name: str
    billing_url: str = Field(..., alias="billingUrl")
    free_time_used: str = Field(..., alias="freeTimeUsed")
    free_time_remaining: str = Field(..., alias="freeTimeRemaining")
    has_active_subscription: bool = Field(..., alias="hasActiveSubscription")
    active_calls: int = Field(..., alias="activeCalls")
    allowed_concurrent_calls: int = Field(..., alias="allowedConcurrentCalls")
    allowed_voices: int = Field(..., alias="allowedVoices")


class ValidateKeyRequest(BaseModel):
    api_key: str = Field(..., alias="apiKey")


class ValidateKeyResponse(BaseModel):
    valid: bool
    account_info: AccountInfo = Field(..., alias="accountInfo")


class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None