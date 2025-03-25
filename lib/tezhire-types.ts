// Tezhire-Ultravox Integration Types

// Session Types
export interface SessionRequest {
  session: {
    sessionId: string;
    callbackUrl: string;
  };
  candidate: {
    candidateId: string;
    name: string;
    email: string;
    phone?: string;
    resumeData: {
      skills: string[];
      experience: Array<{
        company: string;
        role: string;
        duration: string;
        description: string;
      }>;
      education: Array<{
        institution: string;
        degree: string;
        fieldOfStudy: string;
        year: number;
      }>;
      projects: Array<{
        name: string;
        description: string;
        technologies: string[];
      }>;
      rawText: string;
    };
  };
  job: {
    jobId: string;
    companyId: string;
    recruiterUserId: string;
    title: string;
    department: string;
    description: string;
    requirements: string[];
    responsibilities: string[];
    location: string;
    employmentType: string;
    experienceLevel: string;
    salaryRange?: {
      min: number;
      max: number;
      currency: string;
    };
  };
  interview: {
    duration: number;
    difficultyLevel: string;
    topicsToFocus: string[];
    topicsToAvoid: string[];
    customQuestions: string[];
    interviewStyle: string;
    feedbackDetail: string;
  };
  configuration: {
    language: string;
    voiceId?: string;
    enableTranscription: boolean;
    audioQuality: string;
    timeZone: string;
  };
}

export interface SessionResponse {
  success: boolean;
  sessionId: string;
  joinUrl: string;
  expiry: string;
  status: string;
}

// Session Status Types
export interface SessionStatusResponse {
  sessionId: string;
  status: string;
  candidateId: string;
  jobId: string;
  startTime: string | null;
  endTime: string | null;
  duration: number;
  progress: number;
  questionsAsked: number;
}

// End Session Types
export interface EndSessionRequest {
  reason?: string;
}

export interface EndSessionResponse {
  success: boolean;
  sessionId: string;
  status: string;
  duration: number;
}

// Interview Results Types
export interface InterviewResultsResponse {
  sessionId: string;
  candidateId: string;
  jobId: string;
  companyId: string;
  overallScore: number;
  feedback: {
    summary: string;
    strengths: string[];
    areasForImprovement: string[];
    technicalAssessment: string;
    communicationAssessment: string;
    fitScore: number;
    recommendation: string;
  };
  questions: Array<{
    questionId: string;
    question: string;
    timestamp: string;
    answerTranscript: string;
    answerDuration: number;
    evaluation: {
      score: number;
      feedback: string;
      keyInsights: string[];
    };
  }>;
  transcript: {
    full: string;
    url: string;
  };
  audio: {
    url: string;
    duration: number;
  };
}

// Webhook Types
export interface WebhookRequest {
  url: string;
  secret: string;
  events: string[];
}

export interface WebhookEvent {
  event: string;
  timestamp: string;
  sessionId: string;
  data: Record<string, any>;
}

// Error Response Type
export interface ErrorResponse {
  error: string;
  details?: string;
}