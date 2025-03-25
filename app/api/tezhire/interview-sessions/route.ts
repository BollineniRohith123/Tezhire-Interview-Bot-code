import { NextResponse, NextRequest } from 'next/server';
import { SessionRequest, SessionResponse, ErrorResponse } from '@/lib/tezhire-types';
import { CallConfig } from '@/lib/types';

// Helper function to validate the session request
function validateSessionRequest(request: SessionRequest): { isValid: boolean; error?: string } {
  // Check required fields
  if (!request.session?.sessionId) {
    return { isValid: false, error: 'Session ID is required' };
  }
  
  if (!request.candidate?.candidateId || !request.candidate?.name || !request.candidate?.email) {
    return { isValid: false, error: 'Candidate information is incomplete' };
  }
  
  if (!request.job?.jobId || !request.job?.companyId || !request.job?.title) {
    return { isValid: false, error: 'Job information is incomplete' };
  }
  
  return { isValid: true };
}

// Helper function to generate system prompt from request data
function generateSystemPrompt(request: SessionRequest): string {
  const { candidate, job, interview } = request;
  
  // Create a structured system prompt for the interview
  return `
# INTERVIEW CONTEXT
You are conducting a technical interview for ${job.title} position at a company.

## CANDIDATE INFORMATION
- Name: ${candidate.name}
- Position applying for: ${job.title}
- Experience level: ${job.experienceLevel}

## JOB DETAILS
- Title: ${job.title}
- Department: ${job.department}
- Description: ${job.description}
- Requirements: ${job.requirements.join(', ')}
- Responsibilities: ${job.responsibilities.join(', ')}

## INTERVIEW CONFIGURATION
- Difficulty level: ${interview.difficultyLevel}
- Style: ${interview.interviewStyle}
- Duration: ${interview.duration} minutes
- Focus areas: ${interview.topicsToFocus.join(', ')}
- Areas to avoid: ${interview.topicsToAvoid.join(', ')}

## CANDIDATE BACKGROUND
${candidate.resumeData.rawText}

## INTERVIEW INSTRUCTIONS
1. Begin by introducing yourself and making the candidate comfortable
2. Ask questions related to the candidate's experience and the job requirements
3. Focus on the specified topics: ${interview.topicsToFocus.join(', ')}
4. Avoid discussing: ${interview.topicsToAvoid.join(', ')}
5. Include these specific questions: ${interview.customQuestions.join('; ')}
6. Assess technical skills, problem-solving abilities, and communication
7. Provide a comprehensive evaluation at the end of the interview

## EVALUATION CRITERIA
- Technical knowledge relevant to the position
- Problem-solving approach and critical thinking
- Communication skills and clarity of expression
- Cultural fit and alignment with company values
- Overall suitability for the role

Remember to maintain a professional and supportive tone throughout the interview.
`;
}

export async function POST(request: NextRequest) {
  // Handle CORS
  if (request.method === 'OPTIONS') {
    return new NextResponse(null, {
      status: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-API-Key',
      },
    });
  }

  try {
    // Get API key from request header or environment variable
    const apiKey = request.headers.get('X-API-Key') || process.env.ULTRAVOX_API_KEY;
    
    if (!apiKey) {
      return NextResponse.json(
        { error: 'API key is required' } as ErrorResponse,
        { status: 401 }
      );
    }

    // Parse and validate request body
    let sessionRequest: SessionRequest;
    try {
      sessionRequest = await request.json();
      const validation = validateSessionRequest(sessionRequest);
      
      if (!validation.isValid) {
        return NextResponse.json(
          { error: 'Invalid request', details: validation.error } as ErrorResponse,
          { status: 400 }
        );
      }
    } catch (error) {
      return NextResponse.json(
        { error: 'Invalid request format', details: 'Could not parse request body' } as ErrorResponse,
        { status: 400 }
      );
    }

    // Generate system prompt from request data
    const systemPrompt = generateSystemPrompt(sessionRequest);
    
    // Create call configuration for Ultravox
    const callConfig: CallConfig = {
      systemPrompt,
      model: 'fixie-ai/ultravox-70B',
      voice: sessionRequest.configuration?.voiceId,
      languageHint: sessionRequest.configuration?.language || 'en-US',
      maxDuration: `${sessionRequest.interview.duration * 60}s`, // Convert minutes to seconds
      recordingEnabled: true,
      selectedTools: [],
    };

    // Call Ultravox API to create a session
    const response = await fetch('https://api.ultravox.ai/api/calls', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': apiKey,
        'Accept': 'application/json',
      },
      body: JSON.stringify(callConfig),
    });

    if (!response.ok) {
      const errorText = await response.text();
      let errorMessage = errorText;
      
      try {
        const errorJson = JSON.parse(errorText);
        errorMessage = errorJson.error || errorJson.message || errorText;
      } catch {
        // Use raw error text if parsing fails
      }
      
      return NextResponse.json(
        { error: 'Failed to create interview session', details: errorMessage } as ErrorResponse,
        { status: response.status }
      );
    }

    // Parse Ultravox response
    const ultravoxResponse = await response.json();
    
    // Store session data in database or cache for later retrieval
    // This would typically involve saving the mapping between sessionRequest.session.sessionId
    // and ultravoxResponse.callId, along with other relevant data
    
    // For now, we'll just return the response
    const sessionResponse: SessionResponse = {
      success: true,
      sessionId: sessionRequest.session.sessionId,
      joinUrl: ultravoxResponse.joinUrl,
      expiry: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(), // 24 hours from now
      status: 'created'
    };

    return NextResponse.json(sessionResponse);
  } catch (error) {
    console.error('Error creating interview session:', error);
    
    return NextResponse.json(
      { 
        error: 'Internal server error',
        details: error instanceof Error ? error.message : 'Unknown error'
      } as ErrorResponse,
      { status: 500 }
    );
  }
}