from typing import List, Dict, Optional, Any, Union, Literal
from enum import Enum
from pydantic import BaseModel, Field, validator
from datetime import datetime


class RoleEnum(str, Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    TOOL_CALL = "TOOL_CALL"
    TOOL_RESULT = "TOOL_RESULT"
    MESSAGE_ROLE_UNSPECIFIED = "MESSAGE_ROLE_UNSPECIFIED"


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


class MessageMediumEnum(str, Enum):
    UNSPECIFIED = "MESSAGE_MEDIUM_UNSPECIFIED"
    TEXT = "MESSAGE_MEDIUM_TEXT"
    VOICE = "MESSAGE_MEDIUM_VOICE"
    TOOL = "MESSAGE_MEDIUM_TOOL"


class FirstSpeakerEnum(str, Enum):
    UNSPECIFIED = "FIRST_SPEAKER_UNSPECIFIED"
    USER = "FIRST_SPEAKER_USER"
    AGENT = "FIRST_SPEAKER_AGENT"


class EndBehaviorEnum(str, Enum):
    UNSPECIFIED = "END_BEHAVIOR_UNSPECIFIED"
    END_CALL = "END_BEHAVIOR_END_CALL"
    CONTINUE = "END_BEHAVIOR_CONTINUE"


class ParticipantTypeEnum(str, Enum):
    UNSPECIFIED = "PARTICIPANT_TYPE_UNSPECIFIED"
    USER = "PARTICIPANT_TYPE_USER"
    AGENT = "PARTICIPANT_TYPE_AGENT"


class ParticipantStatusEnum(str, Enum):
    UNSPECIFIED = "PARTICIPANT_STATUS_UNSPECIFIED"
    ACTIVE = "PARTICIPANT_STATUS_ACTIVE"
    INACTIVE = "PARTICIPANT_STATUS_INACTIVE"


class ToolStatusEnum(str, Enum):
    UNSPECIFIED = "TOOL_STATUS_UNSPECIFIED"
    ACTIVE = "TOOL_STATUS_ACTIVE"
    INACTIVE = "TOOL_STATUS_INACTIVE"


class CallStatusEnum(str, Enum):
    UNSPECIFIED = "CALL_STATUS_UNSPECIFIED"
    CREATED = "CALL_STATUS_CREATED"
    ACTIVE = "CALL_STATUS_ACTIVE"
    ENDED = "CALL_STATUS_ENDED"


class Message(BaseModel):
    ordinal: Optional[int] = None
    role: RoleEnum
    text: str
    invocation_id: Optional[str] = Field(None, alias="invocationId")
    tool_name: Optional[str] = Field(None, alias="toolName")
    error_details: Optional[str] = Field(None, alias="errorDetails")
    medium: Optional[MessageMediumEnum] = None
    call_stage_message_index: Optional[int] = Field(None, alias="callStageMessageIndex")
    call_stage_id: Optional[str] = Field(None, alias="callStageId")
    call_state: Optional[Dict[str, Any]] = Field(None, alias="callState")


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


class UltravoxCallTokenRequirement(BaseModel):
    scopes: List[str]


class SecurityOptionRequirement(BaseModel):
    requirements: Optional[Dict[str, Any]] = {}
    ultravox_call_token_requirement: Optional[UltravoxCallTokenRequirement] = Field(None, alias="ultravoxCallTokenRequirement")


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
    timeout: Optional[str] = None
    precomputable: Optional[bool] = None
    http: Optional[BaseHttpToolDetails] = None
    client: Optional[Dict[str, Any]] = None
    default_reaction: Optional[str] = Field(None, alias="defaultReaction")


class SelectedTool(BaseModel):
    tool_id: Optional[str] = Field(None, alias="toolId")
    tool_name: Optional[str] = Field(None, alias="toolName")
    temporary_tool: Optional[BaseToolDefinition] = Field(None, alias="temporaryTool")
    name_override: Optional[str] = Field(None, alias="nameOverride")
    auth_tokens: Optional[Dict[str, str]] = Field(None, alias="authTokens")
    parameter_overrides: Optional[Dict[str, Any]] = Field(None, alias="parameterOverrides")


class VadSettings(BaseModel):
    turn_endpoint_delay: Optional[str] = Field(None, alias="turnEndpointDelay")
    minimum_turn_duration: Optional[str] = Field(None, alias="minimumTurnDuration")
    minimum_interruption_duration: Optional[str] = Field(None, alias="minimumInterruptionDuration")
    frame_activation_threshold: Optional[float] = Field(None, alias="frameActivationThreshold")


class UserFallbackSettings(BaseModel):
    delay: Optional[str] = None
    text: Optional[str] = None


class UserFirstSpeakerSettings(BaseModel):
    fallback: Optional[UserFallbackSettings] = None


class AgentFirstSpeakerSettings(BaseModel):
    uninterruptible: Optional[bool] = None
    text: Optional[str] = None
    delay: Optional[str] = None


class FirstSpeakerSettings(BaseModel):
    user: Optional[UserFirstSpeakerSettings] = None
    agent: Optional[AgentFirstSpeakerSettings] = None


class InactivityMessage(BaseModel):
    duration: str
    message: str
    end_behavior: Optional[EndBehaviorEnum] = Field(None, alias="endBehavior")


class WebRtcMedium(BaseModel):
    pass


class TwilioMedium(BaseModel):
    pass


class ServerWebSocketMedium(BaseModel):
    input_sample_rate: Optional[int] = Field(None, alias="inputSampleRate")
    output_sample_rate: Optional[int] = Field(None, alias="outputSampleRate")
    client_buffer_size_ms: Optional[int] = Field(None, alias="clientBufferSizeMs")


class TelnyxMedium(BaseModel):
    pass


class PlivoMedium(BaseModel):
    pass


class ExotelMedium(BaseModel):
    pass


class Medium(BaseModel):
    web_rtc: Optional[WebRtcMedium] = Field(None, alias="webRtc")
    twilio: Optional[TwilioMedium] = None
    server_web_socket: Optional[ServerWebSocketMedium] = Field(None, alias="serverWebSocket")
    telnyx: Optional[TelnyxMedium] = None
    plivo: Optional[PlivoMedium] = None
    exotel: Optional[ExotelMedium] = None


class PronunciationDictionary(BaseModel):
    dictionary_id: str = Field(..., alias="dictionaryId")
    version_id: Optional[str] = Field(None, alias="versionId")


class ElevenLabsVoice(BaseModel):
    voice_id: str = Field(..., alias="voiceId")
    model: Optional[str] = None
    speed: Optional[float] = None
    use_speaker_boost: Optional[bool] = Field(None, alias="useSpeakerBoost")
    style: Optional[float] = None
    similarity_boost: Optional[float] = Field(None, alias="similarityBoost")
    stability: Optional[float] = None
    pronunciation_dictionaries: Optional[List[PronunciationDictionary]] = Field(None, alias="pronunciationDictionaries")


class CartesiaVoice(BaseModel):
    voice_id: str = Field(..., alias="voiceId")
    model: Optional[str] = None
    speed: Optional[float] = None
    emotion: Optional[str] = None


class PlayHtVoice(BaseModel):
    user_id: str = Field(..., alias="userId")
    voice_id: str = Field(..., alias="voiceId")
    model: Optional[str] = None
    speed: Optional[float] = None
    quality: Optional[str] = None
    temperature: Optional[float] = None
    emotion: Optional[float] = None
    voice_guidance: Optional[float] = Field(None, alias="voiceGuidance")
    style_guidance: Optional[float] = Field(None, alias="styleGuidance")
    text_guidance: Optional[float] = Field(None, alias="textGuidance")
    voice_conditioning_seconds: Optional[float] = Field(None, alias="voiceConditioningSeconds")


class LmntVoice(BaseModel):
    voice_id: str = Field(..., alias="voiceId")
    model: Optional[str] = None
    speed: Optional[float] = None
    conversational: Optional[bool] = None


class ExternalVoice(BaseModel):
    eleven_labs: Optional[ElevenLabsVoice] = Field(None, alias="elevenLabs")
    cartesia: Optional[CartesiaVoice] = None
    play_ht: Optional[PlayHtVoice] = Field(None, alias="playHt")
    lmnt: Optional[LmntVoice] = None


class ExperimentalSettings(BaseModel):
    pass


# Request Models
class JoinRequest(BaseModel):
    api_key: str = Field(..., alias="apiKey")
    system_prompt: Optional[str] = Field(None, alias="systemPrompt")
    model: Optional[str] = None
    language_hint: Optional[str] = Field(None, alias="languageHint")
    voice: Optional[str] = None
    temperature: Optional[float] = None

    @validator('temperature')
    def validate_temperature(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('Temperature must be between 0.0 and 1.0')
        return v


class CreateCallRequest(BaseModel):
    api_key: str = Field(..., alias="apiKey")
    system_prompt: Optional[str] = Field(None, alias="systemPrompt")
    temperature: Optional[float] = None
    model: Optional[str] = None
    voice: Optional[str] = None
    external_voice: Optional[ExternalVoice] = Field(None, alias="externalVoice")
    language_hint: Optional[str] = Field(None, alias="languageHint")
    initial_messages: Optional[List[Message]] = Field(None, alias="initialMessages")
    join_timeout: Optional[str] = Field(None, alias="joinTimeout")
    max_duration: Optional[str] = Field(None, alias="maxDuration")
    time_exceeded_message: Optional[str] = Field(None, alias="timeExceededMessage")
    inactivity_messages: Optional[List[InactivityMessage]] = Field(None, alias="inactivityMessages")
    selected_tools: Optional[List[SelectedTool]] = Field(None, alias="selectedTools")
    medium: Optional[Medium] = None
    recording_enabled: Optional[bool] = Field(None, alias="recordingEnabled")
    first_speaker: Optional[FirstSpeakerEnum] = Field(None, alias="firstSpeaker")
    transcript_optional: Optional[bool] = Field(None, alias="transcriptOptional")
    initial_output_medium: Optional[MessageMediumEnum] = Field(None, alias="initialOutputMedium")
    vad_settings: Optional[VadSettings] = Field(None, alias="vadSettings")
    first_speaker_settings: Optional[FirstSpeakerSettings] = Field(None, alias="firstSpeakerSettings")
    experimental_settings: Optional[Dict[str, Any]] = Field(None, alias="experimentalSettings")
    metadata: Optional[Dict[str, Any]] = None
    initial_state: Optional[Dict[str, Any]] = Field(None, alias="initialState")

    @validator('temperature')
    def validate_temperature(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('Temperature must be between 0.0 and 1.0')
        return v


class ListCallsRequest(BaseModel):
    api_key: str = Field(..., alias="apiKey")
    cursor: Optional[str] = None


class CallDetailsRequest(BaseModel):
    api_key: str = Field(..., alias="apiKey")
    call_id: str = Field(..., alias="callId")


class CallMessagesRequest(BaseModel):
    api_key: str = Field(..., alias="apiKey")
    call_id: str = Field(..., alias="callId")
    cursor: Optional[str] = None


# Response Models
class JoinUrlResponse(BaseModel):
    join_url: str = Field(..., alias="joinUrl")
    call_id: Optional[str] = Field(None, alias="callId")
    created: Optional[str] = None


class Participant(BaseModel):
    id: str
    type: ParticipantTypeEnum
    joined_at: Optional[str] = Field(None, alias="joinedAt")
    status: ParticipantStatusEnum


class ToolStatus(BaseModel):
    tool_id: str = Field(..., alias="toolId")
    tool_name: str = Field(..., alias="toolName")
    status: ToolStatusEnum


class InitialMessage(BaseModel):
    id: str
    text: str
    timestamp: str
    role: RoleEnum


class RecordingDetails(BaseModel):
    is_recording: bool = Field(..., alias="isRecording")
    recording_id: Optional[str] = Field(None, alias="recordingId")
    started_at: Optional[str] = Field(None, alias="startedAt")


class TranscriptDetails(BaseModel):
    is_transcribing: bool = Field(..., alias="isTranscribing")
    transcript_id: Optional[str] = Field(None, alias="transcriptId")
    language: Optional[str] = None


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[str] = None
    timestamp: str


class CallConfiguration(BaseModel):
    system_prompt: Optional[str] = Field(None, alias="systemPrompt")
    temperature: Optional[float] = None
    model: Optional[str] = None
    voice: Optional[str] = None
    language_hint: Optional[str] = Field(None, alias="languageHint")
    external_voice: Optional[ExternalVoice] = Field(None, alias="externalVoice")
    join_timeout: Optional[str] = Field(None, alias="joinTimeout")
    max_duration: Optional[str] = Field(None, alias="maxDuration")
    recording_enabled: Optional[bool] = Field(None, alias="recordingEnabled")
    transcript_optional: Optional[bool] = Field(None, alias="transcriptOptional")


class CreateCallResponse(BaseModel):
    call_id: str = Field(..., alias="callId")
    join_url: str = Field(..., alias="joinUrl")
    status: Optional[CallStatusEnum] = None
    created_at: Optional[str] = Field(None, alias="createdAt")
    updated_at: Optional[str] = Field(None, alias="updatedAt")
    configuration: Optional[CallConfiguration] = None
    participants: Optional[List[Participant]] = None
    tools: Optional[List[ToolStatus]] = None
    initial_messages: Optional[List[InitialMessage]] = Field(None, alias="initialMessages")
    recording_details: Optional[RecordingDetails] = Field(None, alias="recordingDetails")
    transcript_details: Optional[TranscriptDetails] = Field(None, alias="transcriptDetails")
    errors: Optional[List[ErrorDetail]] = None
    metadata: Optional[Dict[str, Any]] = None
    experimental_features: Optional[Dict[str, Any]] = Field(None, alias="experimentalFeatures")


class CallDetails(BaseModel):
    call_id: str = Field(..., alias="callId")
    client_version: Optional[str] = Field(None, alias="clientVersion")
    created: Optional[str] = None
    joined: Optional[str] = None
    ended: Optional[str] = None
    end_reason: Optional[str] = Field(None, alias="endReason")
    first_speaker: Optional[FirstSpeakerEnum] = Field(None, alias="firstSpeaker")
    first_speaker_settings: Optional[FirstSpeakerSettings] = Field(None, alias="firstSpeakerSettings")
    inactivity_messages: Optional[List[InactivityMessage]] = Field(None, alias="inactivityMessages")
    initial_output_medium: Optional[MessageMediumEnum] = Field(None, alias="initialOutputMedium")
    join_timeout: Optional[str] = Field(None, alias="joinTimeout")
    join_url: Optional[str] = Field(None, alias="joinUrl")
    language_hint: Optional[str] = Field(None, alias="languageHint")
    max_duration: Optional[str] = Field(None, alias="maxDuration")
    medium: Optional[Medium] = None
    model: Optional[str] = None
    recording_enabled: Optional[bool] = Field(None, alias="recordingEnabled")
    system_prompt: Optional[str] = Field(None, alias="systemPrompt")
    temperature: Optional[float] = None
    time_exceeded_message: Optional[str] = Field(None, alias="timeExceededMessage")
    voice: Optional[str] = None
    external_voice: Optional[ExternalVoice] = Field(None, alias="externalVoice")
    transcript_optional: Optional[bool] = Field(None, alias="transcriptOptional")
    error_count: Optional[int] = Field(None, alias="errorCount")
    vad_settings: Optional[VadSettings] = Field(None, alias="vadSettings")
    short_summary: Optional[str] = Field(None, alias="shortSummary")
    summary: Optional[str] = None
    experimental_settings: Optional[Dict[str, Any]] = Field(None, alias="experimentalSettings")
    metadata: Optional[Dict[str, Any]] = None
    initial_state: Optional[Dict[str, Any]] = Field(None, alias="initialState")


class CallMessageResponse(BaseModel):
    role: RoleEnum
    text: str
    invocation_id: Optional[str] = Field(None, alias="invocationId")
    tool_name: Optional[str] = Field(None, alias="toolName")
    error_details: Optional[str] = Field(None, alias="errorDetails")
    medium: Optional[MessageMediumEnum] = None
    call_stage_message_index: Optional[int] = Field(None, alias="callStageMessageIndex")
    call_stage_id: Optional[str] = Field(None, alias="callStageId")
    call_state: Optional[Dict[str, Any]] = Field(None, alias="callState")


class PaginatedCallMessages(BaseModel):
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[CallMessageResponse]
    total: Optional[int] = None


class PaginatedCallList(BaseModel):
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[CallDetails]
    total: Optional[int] = None


class ValidateKeyRequest(BaseModel):
    api_key: str = Field(..., alias="apiKey")


class AccountInfo(BaseModel):
    name: str
    billing_url: str = Field(..., alias="billingUrl")
    free_time_used: str = Field(..., alias="freeTimeUsed")
    free_time_remaining: str = Field(..., alias="freeTimeRemaining")
    has_active_subscription: bool = Field(..., alias="hasActiveSubscription")
    active_calls: int = Field(..., alias="activeCalls")
    allowed_concurrent_calls: int = Field(..., alias="allowedConcurrentCalls")
    allowed_voices: int = Field(..., alias="allowedVoices")


class ValidateKeyResponse(BaseModel):
    valid: bool
    account_info: AccountInfo = Field(..., alias="accountInfo")


class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None