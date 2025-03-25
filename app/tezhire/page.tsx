'use client';

import React, { useState } from 'react';
import TezhireInterviewSession from '@/app/components/TezhireInterviewSession';
import { SessionRequest, SessionResponse } from '@/lib/tezhire-types';

export default function TezhireDemoPage() {
  const [apiKey, setApiKey] = useState<string>('');
  const [isCreatingSession, setIsCreatingSession] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [sessionResponse, setSessionResponse] = useState<SessionResponse | null>(null);
  
  // Form state for session creation
  const [formData, setFormData] = useState<{
    candidateName: string;
    candidateEmail: string;
    jobTitle: string;
    jobDescription: string;
    duration: number;
    difficultyLevel: string;
  }>({
    candidateName: '',
    candidateEmail: '',
    jobTitle: 'Software Engineer',
    jobDescription: 'We are looking for a skilled software engineer with experience in web development.',
    duration: 30,
    difficultyLevel: 'Medium'
  });
  
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  const handleCreateSession = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!apiKey) {
      setError('API key is required');
      return;
    }
    
    try {
      setIsCreatingSession(true);
      setError(null);
      
      // Create session request payload
      const sessionId = `demo-${Date.now()}`;
      const sessionRequest: SessionRequest = {
        session: {
          sessionId,
          callbackUrl: window.location.origin + '/api/tezhire/webhooks/callback'
        },
        candidate: {
          candidateId: `candidate-${Date.now()}`,
          name: formData.candidateName,
          email: formData.candidateEmail,
          resumeData: {
            skills: ['JavaScript', 'React', 'Node.js', 'TypeScript'],
            experience: [
              {
                company: 'Example Corp',
                role: 'Frontend Developer',
                duration: '2 years',
                description: 'Developed and maintained web applications using React and TypeScript.'
              }
            ],
            education: [
              {
                institution: 'University of Technology',
                degree: 'Bachelor of Science',
                fieldOfStudy: 'Computer Science',
                year: 2020
              }
            ],
            projects: [
              {
                name: 'E-commerce Platform',
                description: 'Built a full-stack e-commerce platform with React, Node.js, and MongoDB.',
                technologies: ['React', 'Node.js', 'MongoDB', 'Express']
              }
            ],
            rawText: 'Experienced software developer with skills in JavaScript, React, Node.js, and TypeScript. 2 years of experience as a Frontend Developer at Example Corp. Bachelor of Science in Computer Science from University of Technology.'
          }
        },
        job: {
          jobId: `job-${Date.now()}`,
          companyId: 'company-tezhire',
          recruiterUserId: 'recruiter-1',
          title: formData.jobTitle,
          department: 'Engineering',
          description: formData.jobDescription,
          requirements: ['JavaScript', 'React', 'Node.js', 'TypeScript'],
          responsibilities: ['Develop and maintain web applications', 'Collaborate with cross-functional teams', 'Write clean, maintainable code'],
          location: 'Remote',
          employmentType: 'Full-time',
          experienceLevel: '2+ years'
        },
        interview: {
          duration: formData.duration,
          difficultyLevel: formData.difficultyLevel,
          topicsToFocus: ['Technical skills', 'Problem-solving', 'Communication'],
          topicsToAvoid: ['Salary expectations', 'Personal information'],
          customQuestions: [
            'Can you describe a challenging project you worked on recently?',
            'How do you approach debugging a complex issue?',
            'What is your experience with state management in React?'
          ],
          interviewStyle: 'Conversational',
          feedbackDetail: 'Detailed'
        },
        configuration: {
          language: 'en-US',
          enableTranscription: true,
          audioQuality: 'High',
          timeZone: 'UTC'
        }
      };
      
      // Call the API to create a session
      const response = await fetch('/api/tezhire/interview-sessions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': apiKey
        },
        body: JSON.stringify(sessionRequest)
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || data.details || 'Failed to create interview session');
      }
      
      setSessionResponse(data);
    } catch (err) {
      console.error('Error creating session:', err);
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setIsCreatingSession(false);
    }
  };
  
  const handleEndSession = () => {
    setSessionResponse(null);
  };
  
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <h1 className="text-2xl font-bold text-gray-900">Tezhire Interview Bot Demo</h1>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {!sessionResponse ? (
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Create Interview Session</h2>
            
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
                {error}
              </div>
            )}
            
            <form onSubmit={handleCreateSession}>
              <div className="mb-4">
                <label htmlFor="apiKey" className="block text-sm font-medium text-gray-700 mb-1">
                  API Key
                </label>
                <input
                  type="text"
                  id="apiKey"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  placeholder="Enter your Ultravox API key"
                  required
                />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <label htmlFor="candidateName" className="block text-sm font-medium text-gray-700 mb-1">
                    Candidate Name
                  </label>
                  <input
                    type="text"
                    id="candidateName"
                    name="candidateName"
                    value={formData.candidateName}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    placeholder="John Doe"
                    required
                  />
                </div>
                
                <div>
                  <label htmlFor="candidateEmail" className="block text-sm font-medium text-gray-700 mb-1">
                    Candidate Email
                  </label>
                  <input
                    type="email"
                    id="candidateEmail"
                    name="candidateEmail"
                    value={formData.candidateEmail}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    placeholder="john.doe@example.com"
                    required
                  />
                </div>
              </div>
              
              <div className="mb-4">
                <label htmlFor="jobTitle" className="block text-sm font-medium text-gray-700 mb-1">
                  Job Title
                </label>
                <input
                  type="text"
                  id="jobTitle"
                  name="jobTitle"
                  value={formData.jobTitle}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  placeholder="Software Engineer"
                  required
                />
              </div>
              
              <div className="mb-4">
                <label htmlFor="jobDescription" className="block text-sm font-medium text-gray-700 mb-1">
                  Job Description
                </label>
                <textarea
                  id="jobDescription"
                  name="jobDescription"
                  value={formData.jobDescription}
                  onChange={handleInputChange}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  placeholder="Describe the job position"
                  required
                />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div>
                  <label htmlFor="duration" className="block text-sm font-medium text-gray-700 mb-1">
                    Interview Duration (minutes)
                  </label>
                  <input
                    type="number"
                    id="duration"
                    name="duration"
                    value={formData.duration}
                    onChange={handleInputChange}
                    min={5}
                    max={60}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    required
                  />
                </div>
                
                <div>
                  <label htmlFor="difficultyLevel" className="block text-sm font-medium text-gray-700 mb-1">
                    Difficulty Level
                  </label>
                  <select
                    id="difficultyLevel"
                    name="difficultyLevel"
                    value={formData.difficultyLevel}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    required
                  >
                    <option value="Easy">Easy</option>
                    <option value="Medium">Medium</option>
                    <option value="Hard">Hard</option>
                  </select>
                </div>
              </div>
              
              <div className="flex justify-end">
                <button
                  type="submit"
                  disabled={isCreatingSession}
                  className={`px-4 py-2 text-white rounded-md ${
                    isCreatingSession
                      ? 'bg-indigo-400 cursor-not-allowed'
                      : 'bg-indigo-600 hover:bg-indigo-700'
                  }`}
                >
                  {isCreatingSession ? 'Creating Session...' : 'Create Interview Session'}
                </button>
              </div>
            </form>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="bg-white shadow rounded-lg p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-medium text-gray-900">Interview Session</h2>
                <button
                  onClick={handleEndSession}
                  className="text-sm text-gray-500 hover:text-gray-700"
                >
                  Create New Session
                </button>
              </div>
              
              <div className="bg-gray-50 p-4 rounded-md mb-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm font-medium text-gray-500">Session ID</p>
                    <p className="mt-1 text-sm text-gray-900">{sessionResponse.sessionId}</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-500">Status</p>
                    <p className="mt-1 text-sm text-gray-900">{sessionResponse.status}</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-500">Expiry</p>
                    <p className="mt-1 text-sm text-gray-900">{new Date(sessionResponse.expiry).toLocaleString()}</p>
                  </div>
                </div>
              </div>
            </div>
            
            <TezhireInterviewSession
              joinUrl={sessionResponse.joinUrl}
              sessionId={sessionResponse.sessionId}
              candidateName={formData.candidateName}
              jobTitle={formData.jobTitle}
              onSessionEnd={() => {
                // In a real application, you would fetch the interview results here
                console.log('Session ended');
              }}
            />
          </div>
        )}
      </main>
    </div>
  );
}