'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { Transcript, Role } from 'ultravox-client';
import { createWebRTCSession, UltravoxWebRTCSession } from '@/lib/ultravoxWebRTC';

interface TezhireInterviewSessionProps {
  joinUrl: string;
  sessionId: string;
  candidateName: string;
  jobTitle: string;
  onSessionEnd?: (transcripts: Transcript[]) => void;
}

const TezhireInterviewSession: React.FC<TezhireInterviewSessionProps> = ({
  joinUrl,
  sessionId,
  candidateName,
  jobTitle,
  onSessionEnd
}) => {
  const [status, setStatus] = useState<string>('initializing');
  const [transcripts, setTranscripts] = useState<Transcript[]>([]);
  const [isMicMuted, setIsMicMuted] = useState<boolean>(false);
  const [isSpeakerMuted, setIsSpeakerMuted] = useState<boolean>(false);
  const [sessionControls, setSessionControls] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  
  // Initialize the WebRTC session
  useEffect(() => {
    let mounted = true;
    
    const initSession = async () => {
      try {
        setStatus('connecting');
        
        const controls = await createWebRTCSession({
          joinUrl,
          onStatusChange: (newStatus) => {
            if (mounted) {
              setStatus(typeof newStatus === 'string' ? newStatus : newStatus.toString());
            }
          },
          onTranscriptChange: (newTranscripts) => {
            if (mounted) {
              setTranscripts(newTranscripts);
            }
          },
          onError: (err) => {
            if (mounted) {
              setError(err.message);
              setStatus('error');
            }
          },
          debug: process.env.NODE_ENV === 'development'
        });
        
        if (mounted) {
          setSessionControls(controls);
          setStatus('connected');
        }
      } catch (err) {
        if (mounted) {
          setError(err instanceof Error ? err.message : 'Failed to initialize interview session');
          setStatus('error');
        }
      }
    };
    
    initSession();
    
    return () => {
      mounted = false;
      // Clean up session if component unmounts
      if (sessionControls) {
        sessionControls.endSession().catch(console.error);
      }
    };
  }, [joinUrl]);
  
  // Handle mic toggle
  const handleMicToggle = useCallback(() => {
    if (sessionControls) {
      sessionControls.toggleUserMic();
      setIsMicMuted(!isMicMuted);
    }
  }, [sessionControls, isMicMuted]);
  
  // Handle speaker toggle
  const handleSpeakerToggle = useCallback(() => {
    if (sessionControls) {
      sessionControls.toggleSpeaker();
      setIsSpeakerMuted(!isSpeakerMuted);
    }
  }, [sessionControls, isSpeakerMuted]);
  
  // Handle end session
  const handleEndSession = useCallback(async () => {
    try {
      if (sessionControls) {
        await sessionControls.endSession();
        setStatus('ended');
        onSessionEnd?.(transcripts);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to end interview session');
    }
  }, [sessionControls, transcripts, onSessionEnd]);
  
  // Render loading state
  if (status === 'initializing' || status === 'connecting') {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] p-6 bg-gray-50 rounded-lg">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-deep-purple mb-4"></div>
        <p className="text-lg font-medium text-gray-700">
          {status === 'initializing' ? 'Initializing interview session...' : 'Connecting to interview...'}
        </p>
      </div>
    );
  }
  
  // Render error state
  if (status === 'error' || error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] p-6 bg-red-50 rounded-lg">
        <div className="text-red-500 mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <p className="text-lg font-medium text-red-700 mb-2">Failed to connect to interview session</p>
        <p className="text-sm text-red-600">{error || 'Unknown error occurred'}</p>
        <button 
          className="mt-4 px-4 py-2 bg-deep-purple text-white rounded-md hover:bg-medium-purple transition-colors"
          onClick={() => window.location.reload()}
        >
          Retry
        </button>
      </div>
    );
  }
  
  // Render ended state
  if (status === 'ended') {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] p-6 bg-gray-50 rounded-lg">
        <div className="text-green-500 mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <p className="text-lg font-medium text-gray-700 mb-2">Interview session ended</p>
        <p className="text-sm text-gray-600">Thank you for participating in the interview.</p>
      </div>
    );
  }
  
  // Render active session
  return (
    <div className="flex flex-col min-h-[600px] bg-white rounded-lg shadow-md overflow-hidden">
      {/* Header */}
      <div className="bg-deep-purple text-white p-4 flex justify-between items-center">
        <div>
          <h2 className="text-lg font-semibold">{jobTitle} Interview</h2>
          <p className="text-sm opacity-80">Candidate: {candidateName}</p>
        </div>
        <div className="flex items-center space-x-2">
          <button 
            onClick={handleMicToggle}
            className={`p-2 rounded-full ${isMicMuted ? 'bg-red-500' : 'bg-white/20'}`}
            title={isMicMuted ? 'Unmute microphone' : 'Mute microphone'}
          >
            {isMicMuted ? (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3l18 18" />
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
            )}
          </button>
          <button 
            onClick={handleSpeakerToggle}
            className={`p-2 rounded-full ${isSpeakerMuted ? 'bg-red-500' : 'bg-white/20'}`}
            title={isSpeakerMuted ? 'Unmute speaker' : 'Mute speaker'}
          >
            {isSpeakerMuted ? (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
              </svg>
            )}
          </button>
        </div>
      </div>
      
      {/* Conversation area */}
      <div className="flex-grow p-4 overflow-y-auto bg-gray-50">
        <div className="space-y-4">
          {transcripts.map((transcript, index) => (
            <div 
              key={index} 
              className={`flex ${transcript.speaker === Role.USER ? 'justify-end' : 'justify-start'}`}
            >
              <div 
                className={`max-w-[80%] p-3 rounded-lg ${
                  transcript.speaker === Role.USER 
                    ? 'bg-deep-purple text-white rounded-tr-none' 
                    : 'bg-white shadow rounded-tl-none'
                }`}
              >
                {transcript.text}
              </div>
            </div>
          ))}
          
          {transcripts.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              <p>The interview will begin shortly. Please wait for the interviewer to start.</p>
            </div>
          )}
        </div>
      </div>
      
      {/* Footer */}
      <div className="p-4 border-t border-gray-200 bg-white">
        <div className="flex justify-between items-center">
          <div className="text-sm text-gray-500">
            {status === 'connected' ? 'Connected' : status}
          </div>
          <button
            onClick={handleEndSession}
            className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors"
          >
            End Interview
          </button>
        </div>
      </div>
    </div>
  );
};

export default TezhireInterviewSession;