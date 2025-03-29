from pydantic import BaseModel, Field, validator
from typing import Dict, Any, Optional, List, Union

class UltravoxCallConfig(BaseModel):
    apiKey: str = Field(
        description="Ultravox API key for authentication"
    )
    systemPrompt: str = Field(
        default="You are a helpful AI assistant that can answer questions and provide information. Be concise, friendly, and helpful in your responses.",
        description="Custom system prompt for the AI assistant"
    )
    model: str = Field(
        default="fixie-ai/ultravox-70B", 
        description="Ultravox model to use"
    )
    languageHint: str = Field(
        default="en", 
        description="Language hint for the assistant"
    )
    voice: str = Field(
        default="terrence", 
        description="Voice to use for the assistant"
    )
    temperature: float = Field(
        default=0.4, 
        ge=0.0, 
        le=1.0, 
        description="Temperature parameter for model responses (0.0-1.0)"
    )

    @validator('apiKey')
    def validate_api_key(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("API key must not be empty")
        return v

class UltravoxResponse(BaseModel):
    joinUrl: str
    callId: Optional[str] = None
    created: Optional[str] = None

class FirstSpeakerSettings(BaseModel):
    user: Optional[Dict[str, Any]] = None
    agent: Optional[Dict[str, Any]] = None

class InactivityMessage(BaseModel):
    duration: Optional[str] = None
    message: Optional[str] = None
    endBehavior: Optional[str] = None

class MediumSettings(BaseModel):
    webRtc: Optional[Dict[str, Any]] = None
    twilio: Optional[Dict[str, Any]] = None
    serverWebSocket: Optional[Dict[str, Any]] = None
    telnyx: Optional[Dict[str, Any]] = None
    plivo: Optional[Dict[str, Any]] = None
    exotel: Optional[Dict[str, Any]] = None

class ElevenLabsVoice(BaseModel):
    voiceId: Optional[str] = None
    model: Optional[str] = None
    speed: Optional[float] = None
    useSpeakerBoost: Optional[bool] = None
    style: Optional[float] = None
    similarityBoost: Optional[float] = None
    stability: Optional[float] = None
    pronunciationDictionaries: Optional[List[Dict[str, str]]] = None

class CartesiaVoice(BaseModel):
    voiceId: Optional[str] = None
    model: Optional[str] = None
    speed: Optional[float] = None
    emotion: Optional[str] = None

class PlayHTVoice(BaseModel):
    userId: Optional[str] = None
    voiceId: Optional[str] = None
    model: Optional[str] = None
    speed: Optional[float] = None
    quality: Optional[str] = None
    temperature: Optional[float] = None
    emotion: Optional[float] = None
    voiceGuidance: Optional[float] = None
    styleGuidance: Optional[float] = None
    textGuidance: Optional[float] = None
    voiceConditioningSeconds: Optional[float] = None

class LmntVoice(BaseModel):
    voiceId: Optional[str] = None
    model: Optional[str] = None
    speed: Optional[float] = None
    conversational: Optional[bool] = None

class ExternalVoiceConfig(BaseModel):
    elevenLabs: Optional[ElevenLabsVoice] = None
    cartesia: Optional[CartesiaVoice] = None
    playHt: Optional[PlayHTVoice] = None
    lmnt: Optional[LmntVoice] = None

class VADSettings(BaseModel):
    turnEndpointDelay: Optional[str] = None
    minimumTurnDuration: Optional[str] = None
    minimumInterruptionDuration: Optional[str] = None
    frameActivationThreshold: Optional[float] = None

class CallDetailsRequest(BaseModel):
    apiKey: str = Field(
        description="Ultravox API key for authentication"
    )
    callId: str = Field(
        description="Unique identifier of the call to retrieve"
    )

    @validator('apiKey')
    def validate_api_key(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("API key must not be empty")
        return v

class CallDetailsResponse(BaseModel):
    callId: str
    clientVersion: Optional[str] = None
    created: Optional[str] = None
    joined: Optional[str] = None
    ended: Optional[str] = None
    endReason: Optional[str] = None
    firstSpeaker: Optional[str] = None
    firstSpeakerSettings: Optional[FirstSpeakerSettings] = None
    inactivityMessages: Optional[List[InactivityMessage]] = None
    initialOutputMedium: Optional[str] = None
    joinTimeout: Optional[str] = None
    joinUrl: Optional[str] = None
    languageHint: Optional[str] = None
    maxDuration: Optional[str] = None
    medium: Optional[MediumSettings] = None
    model: Optional[str] = None
    recordingEnabled: Optional[bool] = None
    systemPrompt: Optional[str] = None
    temperature: Optional[float] = None
    timeExceededMessage: Optional[str] = None
    voice: Optional[str] = None
    externalVoice: Optional[ExternalVoiceConfig] = None
    transcriptOptional: Optional[bool] = None
    errorCount: Optional[int] = None
    vadSettings: Optional[VADSettings] = None
    shortSummary: Optional[str] = None
    summary: Optional[str] = None
    experimentalSettings: Optional[Union[str, Dict[str, Any], None]] = None
    metadata: Optional[Dict[str, Any]] = None
    initialState: Optional[Dict[str, Any]] = None

class InitialMessage(BaseModel):
    role: Optional[str] = None
    text: Optional[str] = None
    invocationId: Optional[str] = None
    toolName: Optional[str] = None
    errorDetails: Optional[str] = None
    medium: Optional[str] = None
    callStageMessageIndex: Optional[int] = None
    callStageId: Optional[str] = None
    callState: Optional[Dict[str, Any]] = None

class DynamicParameter(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    schema: Optional[Dict[str, Any]] = None
    required: Optional[bool] = None

class StaticParameter(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    value: Optional[Any] = None

class AutomaticParameter(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    knownValue: Optional[str] = None

class HttpSecurityOption(BaseModel):
    requirements: Optional[Dict[str, Any]] = None
    ultravoxCallTokenRequirement: Optional[Dict[str, List[str]]] = None

class ToolRequirements(BaseModel):
    httpSecurityOptions: Optional[Dict[str, List[HttpSecurityOption]]] = None
    requiredParameterOverrides: Optional[List[str]] = None

class TemporaryTool(BaseModel):
    modelToolName: Optional[str] = None
    description: Optional[str] = None
    dynamicParameters: Optional[List[DynamicParameter]] = None
    staticParameters: Optional[List[StaticParameter]] = None
    automaticParameters: Optional[List[AutomaticParameter]] = None
    requirements: Optional[ToolRequirements] = None
    timeout: Optional[str] = None
    precomputable: Optional[bool] = None
    http: Optional[Dict[str, str]] = None
    client: Optional[Dict[str, Any]] = None
    defaultReaction: Optional[str] = None

class SelectedTool(BaseModel):
    toolId: Optional[str] = None
    toolName: Optional[str] = None
    temporaryTool: Optional[TemporaryTool] = None
    nameOverride: Optional[str] = None
    authTokens: Optional[Dict[str, Any]] = None
    parameterOverrides: Optional[Dict[str, Any]] = None

class CreateUltravoxCallRequest(BaseModel):
    systemPrompt: Optional[str] = None
    temperature: Optional[float] = None
    model: Optional[str] = None
    voice: Optional[str] = None
    externalVoice: Optional[ExternalVoiceConfig] = None
    languageHint: Optional[str] = None
    initialMessages: Optional[List[InitialMessage]] = None
    joinTimeout: Optional[str] = None
    maxDuration: Optional[str] = None
    timeExceededMessage: Optional[str] = None
    inactivityMessages: Optional[List[InactivityMessage]] = None
    selectedTools: Optional[List[SelectedTool]] = None
    medium: Optional[MediumSettings] = None
    recordingEnabled: Optional[bool] = None
    firstSpeaker: Optional[str] = None
    transcriptOptional: Optional[bool] = None
    initialOutputMedium: Optional[str] = None
    vadSettings: Optional[VADSettings] = None
    firstSpeakerSettings: Optional[FirstSpeakerSettings] = None
    experimentalSettings: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    initialState: Optional[Dict[str, Any]] = None
    apiKey: str = Field(
        description="Ultravox API key for authentication"
    )

    @validator('apiKey')
    def validate_api_key(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("API key must not be empty")
        return v

class CallSummary(BaseModel):
    callId: str
    clientVersion: Optional[str] = None
    created: Optional[str] = None
    joined: Optional[str] = None
    ended: Optional[str] = None
    endReason: Optional[str] = None
    firstSpeaker: Optional[str] = None
    firstSpeakerSettings: Optional[FirstSpeakerSettings] = None
    inactivityMessages: Optional[List[InactivityMessage]] = None
    initialOutputMedium: Optional[str] = None
    joinTimeout: Optional[str] = None
    joinUrl: Optional[str] = None
    languageHint: Optional[str] = None
    maxDuration: Optional[str] = None
    medium: Optional[MediumSettings] = None
    model: Optional[str] = None
    recordingEnabled: Optional[bool] = None
    systemPrompt: Optional[str] = None
    temperature: Optional[float] = None
    timeExceededMessage: Optional[str] = None
    voice: Optional[str] = None
    externalVoice: Optional[ExternalVoiceConfig] = None
    transcriptOptional: Optional[bool] = None
    errorCount: Optional[int] = None
    vadSettings: Optional[VADSettings] = None
    shortSummary: Optional[str] = None
    summary: Optional[str] = None
    experimentalSettings: Optional[Union[str, Dict[str, Any], None]] = None
    metadata: Optional[Dict[str, Any]] = None
    initialState: Optional[Dict[str, Any]] = None

class ListCallsRequest(BaseModel):
    apiKey: str = Field(
        description="Ultravox API key for authentication"
    )
    cursor: Optional[str] = Field(
        default=None,
        description="Pagination cursor for fetching next page of results"
    )

    @validator('apiKey')
    def validate_api_key(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("API key must not be empty")
        return v

class ListCallsResponse(BaseModel):
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[CallSummary]
    total: Optional[int] = None

class CallMessage(BaseModel):
    role: Optional[str] = None
    text: Optional[str] = None
    invocationId: Optional[str] = None
    toolName: Optional[str] = None
    errorDetails: Optional[str] = None
    medium: Optional[str] = None
    callStageMessageIndex: Optional[int] = None
    callStageId: Optional[str] = None
    callState: Optional[Dict[str, Any]] = None

class ListCallMessagesRequest(BaseModel):
    apiKey: str = Field(
        description="Ultravox API key for authentication"
    )
    callId: str = Field(
        description="Unique identifier of the call to retrieve messages for"
    )
    cursor: Optional[str] = Field(
        default=None,
        description="Pagination cursor for fetching next page of results"
    )

    @validator('apiKey')
    def validate_api_key(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("API key must not be empty")
        return v

class ListCallMessagesResponse(BaseModel):
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[CallMessage]
    total: Optional[int] = None

class CallStage(BaseModel):
    callId: str
    callStageId: str
    created: Optional[str] = None
    inactivityMessages: Optional[List[InactivityMessage]] = None
    languageHint: Optional[str] = None
    model: Optional[str] = None
    systemPrompt: Optional[str] = None
    temperature: Optional[float] = None
    timeExceededMessage: Optional[str] = None
    voice: Optional[str] = None
    externalVoice: Optional[ExternalVoiceConfig] = None
    errorCount: Optional[int] = None
    experimentalSettings: Optional[Union[str, Dict[str, Any], None]] = None
    initialState: Optional[Dict[str, Any]] = None

class ListCallStagesRequest(BaseModel):
    apiKey: str = Field(
        description="Ultravox API key for authentication"
    )
    callId: str = Field(
        description="Unique identifier of the call to retrieve stages for"
    )
    cursor: Optional[str] = Field(
        default=None,
        description="Pagination cursor for fetching next page of results"
    )

    @validator('apiKey')
    def validate_api_key(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("API key must not be empty")
        return v

class ListCallStagesResponse(BaseModel):
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[CallStage]
    total: Optional[int] = None

class GetCallStageRequest(BaseModel):
    apiKey: str = Field(
        description="Ultravox API key for authentication"
    )
    callId: str = Field(
        description="Unique identifier of the call"
    )
    callStageId: str = Field(
        description="Unique identifier of the call stage to retrieve"
    )

    @validator('apiKey')
    def validate_api_key(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("API key must not be empty")
        return v