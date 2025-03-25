'use client';

import { UltravoxSession, UltravoxSessionStatus, Transcript, Role } from 'ultravox-client';

// Types for the WebRTC session
interface WebRTCSessionConfig {
  joinUrl: string;
  onStatusChange?: (status: UltravoxSessionStatus | string) => void;
  onTranscriptChange?: (transcripts: Transcript[]) => void;
  onError?: (error: Error) => void;
  debug?: boolean;
}

interface WebRTCSessionControls {
  toggleUserMic: () => void;
  toggleSpeaker: () => void;
  endSession: () => Promise<void>;
  isUserMicMuted: boolean;
  isSpeakerMuted: boolean;
}

// Class to manage the Ultravox WebRTC session
export class UltravoxWebRTCSession {
  private session: UltravoxSession | null = null;
  private config: WebRTCSessionConfig;
  private transcripts: Transcript[] = [];
  
  constructor(config: WebRTCSessionConfig) {
    this.config = config;
  }
  
  // Initialize and join the WebRTC session
  async initialize(): Promise<WebRTCSessionControls> {
    try {
      if (this.session) {
        await this.endSession();
      }
      
      // Create a new AudioContext
      const audioContext = new window.AudioContext();
      
      // Initialize the Ultravox session
      this.session = new UltravoxSession({
        audioContext,
        handlers: {
          statusChange: (status: UltravoxSessionStatus) => {
            if (this.config.debug) {
              console.log('WebRTC status change:', status);
            }
            this.config.onStatusChange?.(status);
          },
          transcriptChange: (transcripts: Transcript[]) => {
            if (this.config.debug) {
              console.log('Transcript update:', transcripts?.length || 0, 'messages');
            }
            this.transcripts = transcripts;
            this.config.onTranscriptChange?.(transcripts);
          }
        }
      });
      
      // Join the call
      await this.session.joinCall(this.config.joinUrl);
      
      // Return controls for the session
      return {
        toggleUserMic: this.toggleUserMic.bind(this),
        toggleSpeaker: this.toggleSpeaker.bind(this),
        endSession: this.endSession.bind(this),
        get isUserMicMuted() {
          return this.session?.isMicMuted || false;
        },
        get isSpeakerMuted() {
          return this.session?.isSpeakerMuted || false;
        }
      };
    } catch (error) {
      console.error('Error initializing WebRTC session:', error);
      this.config.onError?.(error instanceof Error ? error : new Error('Unknown error'));
      throw error;
    }
  }
  
  // Toggle user microphone
  toggleUserMic(): void {
    if (!this.session) {
      console.error('Session not initialized');
      return;
    }
    
    if (this.session.isMicMuted) {
      this.session.unmuteMic();
    } else {
      this.session.muteMic();
    }
  }
  
  // Toggle speaker
  toggleSpeaker(): void {
    if (!this.session) {
      console.error('Session not initialized');
      return;
    }
    
    if (this.session.isSpeakerMuted) {
      this.session.unmuteSpeaker();
    } else {
      this.session.muteSpeaker();
    }
  }
  
  // End the session
  async endSession(): Promise<void> {
    try {
      if (this.session) {
        await this.session.leaveCall();
        this.session = null;
      }
    } catch (error) {
      console.error('Error ending WebRTC session:', error);
      throw error;
    }
  }
  
  // Get current transcripts
  getTranscripts(): Transcript[] {
    return this.transcripts;
  }
}

// Function to create and initialize a WebRTC session
export async function createWebRTCSession(config: WebRTCSessionConfig): Promise<WebRTCSessionControls> {
  const session = new UltravoxWebRTCSession(config);
  return await session.initialize();
}