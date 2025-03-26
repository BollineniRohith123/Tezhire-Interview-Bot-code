import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Request, HTTPException, status, Path
from fastapi.responses import JSONResponse
import httpx

from app.models.tezhire import (
    SessionRequest, SessionResponse, SessionStatusResponse,
    EndSessionRequest, EndSessionResponse, InterviewResultsResponse,
    WebhookRequest, ErrorResponse
)
from app.models.ultravox import CallConfig
from app.utils.api import get_api_key, validate_session_id, handle_api_error

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


def validate_session_request(request: SessionRequest) -> Dict[str, Any]:
    """
    Validate the session request.
    
    Args:
        request: The session request to validate
        
    Returns:
        Dict[str, Any]: Validation result with isValid and optional error
    """
    # Check required fields
    if not request.session.session_id:
        return {"is_valid": False, "error": "Session ID is required"}
    
    if not request.candidate.candidate_id or not request.candidate.name or not request.candidate.email:
        return {"is_valid": False, "error": "Candidate information is incomplete"}
    
    if not request.job.job_id or not request.job.company_id or not request.job.title:
        return {"is_valid": False, "error": "Job information is incomplete"}
    
    return {"is_valid": True}


def generate_system_prompt(request: SessionRequest) -> str:
    """
    Generate a system prompt from the request data.
    
    Args:
        request: The session request
        
    Returns:
        str: The generated system prompt
    """
    candidate = request.candidate
    job = request.job
    interview = request.interview
    
    # Create a structured system prompt for the interview
    return f"""
# INTERVIEW CONTEXT
You are conducting a technical interview for {job.title} position at a company.

## CANDIDATE INFORMATION
- Name: {candidate.name}
- Position applying for: {job.title}
- Experience level: {job.experience_level}

## JOB DETAILS
- Title: {job.title}
- Department: {job.department}
- Description: {job.description}
- Requirements: {', '.join(job.requirements)}
- Responsibilities: {', '.join(job.responsibilities)}

## INTERVIEW CONFIGURATION
- Difficulty level: {interview.difficulty_level}
- Style: {interview.interview_style}
- Duration: {interview.duration} minutes
- Focus areas: {', '.join(interview.topics_to_focus)}
- Areas to avoid: {', '.join(interview.topics_to_avoid)}

## CANDIDATE BACKGROUND
{candidate.resume_data.raw_text}

## INTERVIEW INSTRUCTIONS
1. Begin by introducing yourself and making the candidate comfortable
2. Ask questions related to the candidate's experience and the job requirements
3. Focus on the specified topics: {', '.join(interview.topics_to_focus)}
4. Avoid discussing: {', '.join(interview.topics_to_avoid)}
5. Include these specific questions: {'; '.join(interview.custom_questions)}
6. Assess technical skills, problem-solving abilities, and communication
7. Provide a comprehensive evaluation at the end of the interview

## EVALUATION CRITERIA
- Technical knowledge relevant to the position
- Problem-solving approach and critical thinking
- Communication skills and clarity of expression
- Cultural fit and alignment with company values
- Overall suitability for the role

Remember to maintain a professional and supportive tone throughout the interview.
"""


@router.post("/interview-sessions", response_model=SessionResponse)
async def create_interview_session(request: Request, session_request: SessionRequest):
    """
    Create a new interview session.
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
        
        # Validate request
        validation = validate_session_request(session_request)
        if not validation["is_valid"]:
            return JSONResponse(
                content={"error": "Invalid request", "details": validation["error"]},
                status_code=400
            )
        
        # Generate system prompt
        system_prompt = generate_system_prompt(session_request)
        
        # Create call configuration for Ultravox
        call_config = {
            "systemPrompt": system_prompt,
            "model": "fixie-ai/ultravox-70B",
            "voice": session_request.configuration.voice_id,
            "languageHint": session_request.configuration.language or "en-US",
            "maxDuration": f"{session_request.interview.duration * 60}s",  # Convert minutes to seconds
            "recordingEnabled": True,
            "selectedTools": [],
        }
        
        # Call Ultravox API to create a session
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://api.ultravox.ai/api/calls',
                headers={
                    'Content-Type': 'application/json',
                    'X-API-Key': api_key,
                    'Accept': 'application/json',
                },
                json=call_config,
                timeout=30.0
            )
        
        if not response.is_success:
            error_text = response.text
            
            try:
                error_json = response.json()
                error_message = error_json.get("error") or error_json.get("message") or error_text
            except:
                # Use raw error text if parsing fails
                error_message = error_text
            
            return JSONResponse(
                content={"error": "Failed to create interview session", "details": error_message},
                status_code=response.status_code
            )
        
        # Parse Ultravox response
        ultravox_response = response.json()
        
        # Store session data in database or cache for later retrieval
        # This would typically involve saving the mapping between session_request.session.session_id
        # and ultravox_response.callId, along with other relevant data
        
        # For now, we'll just return the response
        session_response = {
            "success": True,
            "sessionId": session_request.session.session_id,
            "joinUrl": ultravox_response["joinUrl"],
            "expiry": (datetime.now() + timedelta(days=1)).isoformat(),  # 24 hours from now
            "status": "created"
        }
        
        return session_response
        
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        logger.error(f"Error creating interview session: {str(e)}")
        return JSONResponse(
            content={
                "error": "Internal server error",
                "details": str(e)
            },
            status_code=500
        )


@router.get("/interview-sessions/{session_id}", response_model=SessionStatusResponse)
async def get_session_status(
    request: Request,
    session_id: str = Path(..., description="The ID of the interview session")
):
    """
    Get the status of an interview session.
    """
    try:
        validate_session_id(session_id)
        
        # Get API key
        api_key = get_api_key(request)
        
        # In a real implementation, we would:
        # 1. Retrieve the mapping between Tezhire sessionId and Ultravox callId from database
        # 2. Call Ultravox API to get the call status
        # 3. Transform the response to match our API format
        
        # For now, we'll simulate this process with mock data
        # In a production environment, you would replace this with actual database lookups
        # and API calls to Ultravox
        
        # Mock data for demonstration
        mock_status = {
            "sessionId": session_id,
            "status": "in_progress",  # Possible values: created, waiting, in_progress, completed, cancelled, error
            "candidateId": "candidate-123",
            "jobId": "job-456",
            "startTime": datetime.now().isoformat(),
            "endTime": None,
            "duration": 300,  # seconds
            "progress": 45,  # percentage
            "questionsAsked": 5
        }
        
        return mock_status
        
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        logger.error(f"Error retrieving session status: {str(e)}")
        return JSONResponse(
            content={
                "error": "Internal server error",
                "details": str(e)
            },
            status_code=500
        )


@router.post("/interview-sessions/{session_id}/end", response_model=EndSessionResponse)
async def end_session(
    request: Request,
    end_request: Optional[EndSessionRequest] = None,
    session_id: str = Path(..., description="The ID of the interview session to end")
):
    """
    End an interview session.
    """
    try:
        validate_session_id(session_id)
        
        # Get API key
        api_key = get_api_key(request)
        
        # In a real implementation, we would:
        # 1. Retrieve the mapping between Tezhire sessionId and Ultravox callId from database
        # 2. Call Ultravox API to end the call
        # 3. Transform the response to match our API format
        
        # For now, we'll simulate this process with mock data
        # In a production environment, you would replace this with actual database lookups
        # and API calls to Ultravox
        
        # Mock response for demonstration
        end_response = {
            "success": True,
            "sessionId": session_id,
            "status": "ended",
            "duration": 720  # seconds
        }
        
        return end_response
        
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        logger.error(f"Error ending session: {str(e)}")
        return JSONResponse(
            content={
                "error": "Internal server error",
                "details": str(e)
            },
            status_code=500
        )


@router.get("/interview-sessions/{session_id}/results", response_model=InterviewResultsResponse)
async def get_interview_results(
    request: Request,
    session_id: str = Path(..., description="The ID of the interview session")
):
    """
    Get the results of an interview session.
    """
    try:
        validate_session_id(session_id)
        
        # Get API key
        api_key = get_api_key(request)
        
        # In a real implementation, we would:
        # 1. Retrieve the mapping between Tezhire sessionId and Ultravox callId from database
        # 2. Call Ultravox API to get the call messages and details
        # 3. Process the messages to generate an analysis
        # 4. Transform the response to match our API format
        
        # For now, we'll simulate this process with mock data
        # In a production environment, you would replace this with actual database lookups
        # and API calls to Ultravox
        
        # Mock response for demonstration
        results_response = {
            "sessionId": session_id,
            "candidateId": "candidate-123",
            "jobId": "job-456",
            "companyId": "company-789",
            "overallScore": 78,
            "feedback": {
                "summary": "The candidate demonstrated strong technical knowledge and problem-solving skills. Communication was clear and professional.",
                "strengths": [
                    "Strong understanding of core programming concepts",
                    "Excellent problem-solving approach",
                    "Clear communication of technical ideas"
                ],
                "areasForImprovement": [
                    "Could improve knowledge of advanced algorithms",
                    "More experience with distributed systems would be beneficial"
                ],
                "technicalAssessment": "The candidate showed proficiency in most technical areas relevant to the position.",
                "communicationAssessment": "Communication was clear, concise, and professional throughout the interview.",
                "fitScore": 82,
                "recommendation": "Hire"
            },
            "questions": [
                {
                    "questionId": "q1",
                    "question": "Can you explain your approach to solving complex technical problems?",
                    "timestamp": (datetime.now() - timedelta(minutes=30)).isoformat(),
                    "answerTranscript": "I typically start by breaking down the problem into smaller components...",
                    "answerDuration": 45,
                    "evaluation": {
                        "score": 85,
                        "feedback": "Excellent problem decomposition approach",
                        "keyInsights": ["Methodical", "Structured thinking", "Clear communication"]
                    }
                },
                {
                    "questionId": "q2",
                    "question": "Describe your experience with distributed systems.",
                    "timestamp": (datetime.now() - timedelta(minutes=25)).isoformat(),
                    "answerTranscript": "I have worked on several projects involving distributed architectures...",
                    "answerDuration": 60,
                    "evaluation": {
                        "score": 70,
                        "feedback": "Good understanding but limited practical experience",
                        "keyInsights": ["Theoretical knowledge", "Limited hands-on experience"]
                    }
                }
            ],
            "transcript": {
                "full": "Full interview transcript would be here...",
                "url": "https://api.example.com/transcripts/interview-123.txt"
            },
            "audio": {
                "url": "https://api.example.com/recordings/interview-123.mp3",
                "duration": 1800
            }
        }
        
        return results_response
        
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        logger.error(f"Error retrieving interview results: {str(e)}")
        return JSONResponse(
            content={
                "error": "Internal server error",
                "details": str(e)
            },
            status_code=500
        )


@router.post("/webhooks")
async def configure_webhook(request: Request, webhook_request: WebhookRequest):
    """
    Configure a webhook for interview events.
    """
    try:
        # Get API key
        api_key = get_api_key(request)
        
        # Validate event types
        valid_event_types = [
            'interview.created',
            'interview.started',
            'interview.completed',
            'interview.cancelled',
            'interview.error',
            'results.available'
        ]
        
        invalid_events = [event for event in webhook_request.events if event not in valid_event_types]
        if invalid_events:
            return JSONResponse(
                content={
                    "error": "Invalid event types",
                    "details": f"The following event types are not supported: {', '.join(invalid_events)}"
                },
                status_code=400
            )
        
        # In a real implementation, we would:
        # 1. Store the webhook configuration in a database
        # 2. Set up event listeners for the specified events
        # 3. Configure the webhook to send events to the specified URL
        
        # For now, we'll just return a success response
        return {
            "success": True,
            "message": "Webhook configured successfully",
            "webhookId": f"webhook-{int(datetime.now().timestamp())}",
            "url": webhook_request.url,
            "events": webhook_request.events
        }
        
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        logger.error(f"Error configuring webhook: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            content={
                "error": "Internal server error",
                "details": str(e)
            },
            status_code=500
        )