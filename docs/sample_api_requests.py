"""
Sample Python API requests for the Interview Bot API.
"""
import json
import httpx
import asyncio
from typing import Dict, Any, Optional


# Configuration
API_BASE_URL = "http://localhost:8000"
ULTRAVOX_API_KEY = "your_ultravox_api_key"  # Replace with your actual API key


async def create_ultravox_call() -> Dict[str, Any]:
    """
    Create a new Ultravox call.
    
    Returns:
        Dict[str, Any]: The response from the API
    """
    url = f"{API_BASE_URL}/api/ultravox"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": ULTRAVOX_API_KEY
    }
    payload = {
        "systemPrompt": "You are an interviewer for a software engineering position. Ask questions about Python programming.",
        "temperature": 0.7,
        "model": "fixie-ai/ultravox-70B",
        "voice": "echo",
        "languageHint": "en-US",
        "maxDuration": "1800s",
        "recordingEnabled": True
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()


async def get_call_messages(call_id: str) -> Dict[str, Any]:
    """
    Get messages for a specific call.
    
    Args:
        call_id: The ID of the call to fetch messages for
        
    Returns:
        Dict[str, Any]: The response from the API
    """
    url = f"{API_BASE_URL}/api/ultravox/messages?callId={call_id}"
    headers = {
        "X-API-Key": ULTRAVOX_API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()


async def validate_api_key(api_key: str) -> Dict[str, Any]:
    """
    Validate an Ultravox API key.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        Dict[str, Any]: The response from the API
    """
    url = f"{API_BASE_URL}/api/ultravox/validate-key"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "apiKey": api_key
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()


async def create_interview_session() -> Dict[str, Any]:
    """
    Create a new interview session.
    
    Returns:
        Dict[str, Any]: The response from the API
    """
    url = f"{API_BASE_URL}/api/tezhire/interview-sessions"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": ULTRAVOX_API_KEY
    }
    payload = {
        "session": {
            "sessionId": "session_123456",
            "callbackUrl": "https://example.com/callback"
        },
        "candidate": {
            "candidateId": "candidate_123",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "resumeData": {
                "skills": ["Python", "JavaScript", "React", "Node.js"],
                "experience": [
                    {
                        "company": "Example Corp",
                        "role": "Senior Developer",
                        "duration": "2 years",
                        "description": "Developed web applications using React and Node.js"
                    }
                ],
                "education": [
                    {
                        "institution": "Example University",
                        "degree": "Bachelor of Science",
                        "fieldOfStudy": "Computer Science",
                        "year": 2018
                    }
                ],
                "projects": [
                    {
                        "name": "Project X",
                        "description": "A web application for task management",
                        "technologies": ["React", "Node.js", "MongoDB"]
                    }
                ],
                "rawText": "John Doe\nSenior Developer\n\nSkills: Python, JavaScript, React, Node.js\n\nExperience:\nExample Corp - Senior Developer (2 years)\nDeveloped web applications using React and Node.js\n\nEducation:\nExample University - Bachelor of Science in Computer Science (2018)\n\nProjects:\nProject X - A web application for task management using React, Node.js, and MongoDB"
            }
        },
        "job": {
            "jobId": "job_456",
            "companyId": "company_789",
            "recruiterUserId": "recruiter_101",
            "title": "Senior Software Engineer",
            "department": "Engineering",
            "description": "We are looking for a Senior Software Engineer to join our team.",
            "requirements": [
                "5+ years of experience in software development",
                "Strong knowledge of Python",
                "Experience with web frameworks"
            ],
            "responsibilities": [
                "Develop and maintain web applications",
                "Collaborate with cross-functional teams",
                "Mentor junior developers"
            ],
            "location": "San Francisco, CA",
            "employmentType": "Full-time",
            "experienceLevel": "Senior",
            "salaryRange": {
                "min": 120000,
                "max": 150000,
                "currency": "USD"
            }
        },
        "interview": {
            "duration": 30,
            "difficultyLevel": "Medium",
            "topicsToFocus": ["Python", "Web Development", "System Design"],
            "topicsToAvoid": ["Personal Questions", "Salary Expectations"],
            "customQuestions": [
                "Describe a challenging project you worked on recently",
                "How do you approach debugging a complex issue?"
            ],
            "interviewStyle": "Conversational",
            "feedbackDetail": "Comprehensive"
        },
        "configuration": {
            "language": "en-US",
            "voiceId": "echo",
            "enableTranscription": True,
            "audioQuality": "high",
            "timeZone": "America/Los_Angeles"
        }
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()


async def get_session_status(session_id: str) -> Dict[str, Any]:
    """
    Get the status of an interview session.
    
    Args:
        session_id: The ID of the interview session
        
    Returns:
        Dict[str, Any]: The response from the API
    """
    url = f"{API_BASE_URL}/api/tezhire/interview-sessions/{session_id}"
    headers = {
        "X-API-Key": ULTRAVOX_API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()


async def end_session(session_id: str, reason: Optional[str] = None) -> Dict[str, Any]:
    """
    End an interview session.
    
    Args:
        session_id: The ID of the interview session to end
        reason: The reason for ending the session (optional)
        
    Returns:
        Dict[str, Any]: The response from the API
    """
    url = f"{API_BASE_URL}/api/tezhire/interview-sessions/{session_id}/end"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": ULTRAVOX_API_KEY
    }
    payload = {}
    if reason:
        payload["reason"] = reason
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()


async def get_interview_results(session_id: str) -> Dict[str, Any]:
    """
    Get the results of an interview session.
    
    Args:
        session_id: The ID of the interview session
        
    Returns:
        Dict[str, Any]: The response from the API
    """
    url = f"{API_BASE_URL}/api/tezhire/interview-sessions/{session_id}/results"
    headers = {
        "X-API-Key": ULTRAVOX_API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()


async def configure_webhook(webhook_url: str, secret: str, events: list) -> Dict[str, Any]:
    """
    Configure a webhook for interview events.
    
    Args:
        webhook_url: The URL to send webhook events to
        secret: The secret to use for webhook validation
        events: List of event types to subscribe to
        
    Returns:
        Dict[str, Any]: The response from the API
    """
    url = f"{API_BASE_URL}/api/tezhire/webhooks"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": ULTRAVOX_API_KEY
    }
    payload = {
        "url": webhook_url,
        "secret": secret,
        "events": events
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()


async def main():
    """
    Run sample API requests.
    """
    try:
        # Validate API key
        print("Validating API key...")
        validation_result = await validate_api_key(ULTRAVOX_API_KEY)
        print(f"API key validation result: {json.dumps(validation_result, indent=2)}\n")
        
        # Join Ultravox call (new API)
        print("Joining Ultravox call (new API)...")
        join_result = await join_ultravox_call()
        join_call_id = join_result.get("callId")
        join_url = join_result.get("joinUrl")
        print(f"Call joined: {json.dumps(join_result, indent=2)}\n")
        print(f"Join URL: {join_url}\n")
        
        # Create Ultravox call with advanced options (new API)
        print("Creating Ultravox call with advanced options (new API)...")
        advanced_call_result = await create_ultravox_call_advanced()
        advanced_call_id = advanced_call_result.get("callId")
        print(f"Advanced call created: {json.dumps(advanced_call_result, indent=2)}\n")
        
        # List Ultravox calls (new API)
        print("Listing Ultravox calls (new API)...")
        list_result = await list_ultravox_calls()
        print(f"Call list: {json.dumps(list_result, indent=2)}\n")
        
        # Get call details (new API)
        if join_call_id:
            print(f"Getting details for call {join_call_id} (new API)...")
            details_result = await get_ultravox_call_details(join_call_id)
            print(f"Call details: {json.dumps(details_result, indent=2)}\n")
        
        # Get call messages (new API)
        if join_call_id:
            print(f"Waiting 5 seconds for messages to be generated...")
            await asyncio.sleep(5)
            print(f"Getting messages for call {join_call_id} (new API)...")
            new_messages_result = await get_ultravox_call_messages(join_call_id)
            print(f"Call messages (new API): {json.dumps(new_messages_result, indent=2)}\n")
        
        # Create Ultravox call (legacy API)
        print("Creating Ultravox call (legacy API)...")
        call_result = await create_ultravox_call()
        call_id = call_result.get("callId")
        print(f"Call created: {json.dumps(call_result, indent=2)}\n")
        
        # Get call messages (legacy API)
        if call_id:
            print(f"Waiting 5 seconds for messages to be generated...")
            await asyncio.sleep(5)
            print(f"Getting messages for call {call_id} (legacy API)...")
            messages_result = await get_call_messages(call_id)
            print(f"Call messages (legacy API): {json.dumps(messages_result, indent=2)}\n")
        
        # Create interview session
        print("Creating interview session...")
        session_result = await create_interview_session()
        session_id = session_result.get("sessionId")
        print(f"Session created: {json.dumps(session_result, indent=2)}\n")
        
        # Get session status
        if session_id:
            print(f"Getting status for session {session_id}...")
            status_result = await get_session_status(session_id)
            print(f"Session status: {json.dumps(status_result, indent=2)}\n")
            
            # End session
            print(f"Ending session {session_id}...")
            end_result = await end_session(session_id, "Interview completed")
            print(f"Session ended: {json.dumps(end_result, indent=2)}\n")
            
            # Get interview results
            print(f"Getting results for session {session_id}...")
            results_result = await get_interview_results(session_id)
            print(f"Interview results: {json.dumps(results_result, indent=2)}\n")
        
        # Configure webhook
        print("Configuring webhook...")
        webhook_result = await configure_webhook(
            "https://example.com/webhook",
            "webhook_secret_123",
            ["interview.created", "interview.completed", "results.available"]
        )
        print(f"Webhook configured: {json.dumps(webhook_result, indent=2)}\n")
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())