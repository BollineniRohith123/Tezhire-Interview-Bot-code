import { NextResponse, NextRequest } from 'next/server';
import { EndSessionRequest, EndSessionResponse, ErrorResponse } from '@/lib/tezhire-types';

export async function POST(
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

    // Parse request body
    let endRequest: EndSessionRequest = {};
    try {
      const body = await request.json();
      endRequest = body;
    } catch (error) {
      // If parsing fails, use empty object (reason is optional)
      console.warn('Failed to parse request body, using default values');
    }

    // In a real implementation, we would:
    // 1. Retrieve the mapping between Tezhire sessionId and Ultravox callId from database
    // 2. Call Ultravox API to end the call
    // 3. Transform the response to match our API format
    
    // For now, we'll simulate this process with mock data
    // In a production environment, you would replace this with actual database lookups
    // and API calls to Ultravox
    
    // Mock response for demonstration
    const endResponse: EndSessionResponse = {
      success: true,
      sessionId: sessionId,
      status: 'ended',
      duration: 720 // seconds
    };

    return NextResponse.json(endResponse);
  } catch (error) {
    console.error('Error ending session:', error);
    
    return NextResponse.json(
      { 
        error: 'Internal server error',
        details: error instanceof Error ? error.message : 'Unknown error'
      } as ErrorResponse,
      { status: 500 }
    );
  }
}