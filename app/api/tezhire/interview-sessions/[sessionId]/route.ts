import { NextResponse, NextRequest } from 'next/server';
import { SessionStatusResponse, ErrorResponse } from '@/lib/tezhire-types';

export async function GET(
  request: NextRequest,
  { params }: { params: { sessionId: string } }
) {
  try {
    const sessionId = params.sessionId;
    
    if (!sessionId) {
      return NextResponse.json(
        { error: 'Session ID is required' } as ErrorResponse,
        { status: 400 }
      );
    }

    // Get API key from request header or environment variable
    const apiKey = request.headers.get('X-API-Key') || process.env.ULTRAVOX_API_KEY;
    
    if (!apiKey) {
      return NextResponse.json(
        { error: 'API key is required' } as ErrorResponse,
        { status: 401 }
      );
    }

    // In a real implementation, we would:
    // 1. Retrieve the mapping between Tezhire sessionId and Ultravox callId from database
    // 2. Call Ultravox API to get the call status
    // 3. Transform the response to match our API format
    
    // For now, we'll simulate this process with mock data
    // In a production environment, you would replace this with actual database lookups
    // and API calls to Ultravox
    
    // Mock data for demonstration
    const mockStatus: SessionStatusResponse = {
      sessionId: sessionId,
      status: 'in_progress', // Possible values: created, waiting, in_progress, completed, cancelled, error
      candidateId: 'candidate-123',
      jobId: 'job-456',
      startTime: new Date().toISOString(),
      endTime: null,
      duration: 300, // seconds
      progress: 45, // percentage
      questionsAsked: 5
    };

    return NextResponse.json(mockStatus);
  } catch (error) {
    console.error('Error retrieving session status:', error);
    
    return NextResponse.json(
      { 
        error: 'Internal server error',
        details: error instanceof Error ? error.message : 'Unknown error'
      } as ErrorResponse,
      { status: 500 }
    );
  }
}