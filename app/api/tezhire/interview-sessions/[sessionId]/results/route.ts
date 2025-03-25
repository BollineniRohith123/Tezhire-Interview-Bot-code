import { NextResponse, NextRequest } from 'next/server';
import { InterviewResultsResponse, ErrorResponse } from '@/lib/tezhire-types';

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
    // 2. Call Ultravox API to get the call messages and details
    // 3. Process the messages to generate an analysis
    // 4. Transform the response to match our API format
    
    // For now, we'll simulate this process with mock data
    // In a production environment, you would replace this with actual database lookups
    // and API calls to Ultravox
    
    // Mock response for demonstration
    const resultsResponse: InterviewResultsResponse = {
      sessionId: sessionId,
      candidateId: 'candidate-123',
      jobId: 'job-456',
      companyId: 'company-789',
      overallScore: 78,
      feedback: {
        summary: 'The candidate demonstrated strong technical knowledge and problem-solving skills. Communication was clear and professional.',
        strengths: [
          'Strong understanding of core programming concepts',
          'Excellent problem-solving approach',
          'Clear communication of technical ideas'
        ],
        areasForImprovement: [
          'Could improve knowledge of advanced algorithms',
          'More experience with distributed systems would be beneficial'
        ],
        technicalAssessment: 'The candidate showed proficiency in most technical areas relevant to the position.',
        communicationAssessment: 'Communication was clear, concise, and professional throughout the interview.',
        fitScore: 82,
        recommendation: 'Hire'
      },
      questions: [
        {
          questionId: 'q1',
          question: 'Can you explain your approach to solving complex technical problems?',
          timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
          answerTranscript: 'I typically start by breaking down the problem into smaller components...',
          answerDuration: 45,
          evaluation: {
            score: 85,
            feedback: 'Excellent problem decomposition approach',
            keyInsights: ['Methodical', 'Structured thinking', 'Clear communication']
          }
        },
        {
          questionId: 'q2',
          question: 'Describe your experience with distributed systems.',
          timestamp: new Date(Date.now() - 1000 * 60 * 25).toISOString(),
          answerTranscript: 'I have worked on several projects involving distributed architectures...',
          answerDuration: 60,
          evaluation: {
            score: 70,
            feedback: 'Good understanding but limited practical experience',
            keyInsights: ['Theoretical knowledge', 'Limited hands-on experience']
          }
        }
      ],
      transcript: {
        full: 'Full interview transcript would be here...',
        url: 'https://api.example.com/transcripts/interview-123.txt'
      },
      audio: {
        url: 'https://api.example.com/recordings/interview-123.mp3',
        duration: 1800
      }
    };

    return NextResponse.json(resultsResponse);
  } catch (error) {
    console.error('Error retrieving interview results:', error);
    
    return NextResponse.json(
      { 
        error: 'Internal server error',
        details: error instanceof Error ? error.message : 'Unknown error'
      } as ErrorResponse,
      { status: 500 }
    );
  }
}