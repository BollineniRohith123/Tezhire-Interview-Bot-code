import { NextResponse, NextRequest } from 'next/server';
import { WebhookRequest, ErrorResponse } from '@/lib/tezhire-types';

export async function POST(request: NextRequest) {
  try {
    // Get API key from request header or environment variable
    const apiKey = request.headers.get('X-API-Key') || process.env.ULTRAVOX_API_KEY;
    
    if (!apiKey) {
      return NextResponse.json(
        { error: 'API key is required' } as ErrorResponse,
        { status: 401 }
      );
    }

    // Parse request body
    let webhookRequest: WebhookRequest;
    try {
      webhookRequest = await request.json();
      
      // Validate required fields
      if (!webhookRequest.url) {
        return NextResponse.json(
          { error: 'Webhook URL is required' } as ErrorResponse,
          { status: 400 }
        );
      }
      
      if (!webhookRequest.secret) {
        return NextResponse.json(
          { error: 'Webhook secret is required for security' } as ErrorResponse,
          { status: 400 }
        );
      }
      
      if (!webhookRequest.events || webhookRequest.events.length === 0) {
        return NextResponse.json(
          { error: 'At least one event type must be specified' } as ErrorResponse,
          { status: 400 }
        );
      }
    } catch (error) {
      return NextResponse.json(
        { error: 'Invalid request format', details: 'Could not parse request body' } as ErrorResponse,
        { status: 400 }
      );
    }

    // Validate event types
    const validEventTypes = [
      'interview.created',
      'interview.started',
      'interview.completed',
      'interview.cancelled',
      'interview.error',
      'results.available'
    ];
    
    const invalidEvents = webhookRequest.events.filter(event => !validEventTypes.includes(event));
    if (invalidEvents.length > 0) {
      return NextResponse.json(
        { 
          error: 'Invalid event types', 
          details: `The following event types are not supported: ${invalidEvents.join(', ')}` 
        } as ErrorResponse,
        { status: 400 }
      );
    }

    // In a real implementation, we would:
    // 1. Store the webhook configuration in a database
    // 2. Set up event listeners for the specified events
    // 3. Configure the webhook to send events to the specified URL
    
    // For now, we'll just return a success response
    return NextResponse.json({
      success: true,
      message: 'Webhook configured successfully',
      webhookId: `webhook-${Date.now()}`,
      url: webhookRequest.url,
      events: webhookRequest.events
    });
  } catch (error) {
    console.error('Error configuring webhook:', error);
    
    return NextResponse.json(
      { 
        error: 'Internal server error',
        details: error instanceof Error ? error.message : 'Unknown error'
      } as ErrorResponse,
      { status: 500 }
    );
  }
}