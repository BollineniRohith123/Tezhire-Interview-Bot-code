from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime


class Experience(BaseModel):
    company: str
    role: str
    duration: str
    description: str


class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: str = Field(..., alias="fieldOfStudy")
    year: int


class Project(BaseModel):
    name: str
    description: str
    technologies: List[str]


class ResumeData(BaseModel):
    skills: List[str]
    experience: List[Experience]
    education: List[Education]
    projects: List[Project]
    raw_text: str = Field(..., alias="rawText")


class SalaryRange(BaseModel):
    min: int
    max: int
    currency: str


class Candidate(BaseModel):
    candidate_id: str = Field(..., alias="candidateId")
    name: str
    email: str
    phone: Optional[str] = None
    resume_data: ResumeData = Field(..., alias="resumeData")


class Job(BaseModel):
    job_id: str = Field(..., alias="jobId")
    company_id: str = Field(..., alias="companyId")
    recruiter_user_id: str = Field(..., alias="recruiterUserId")
    title: str
    department: str
    description: str
    requirements: List[str]
    responsibilities: List[str]
    location: str
    employment_type: str = Field(..., alias="employmentType")
    experience_level: str = Field(..., alias="experienceLevel")
    salary_range: Optional[SalaryRange] = Field(None, alias="salaryRange")


class Interview(BaseModel):
    duration: int
    difficulty_level: str = Field(..., alias="difficultyLevel")
    topics_to_focus: List[str] = Field(..., alias="topicsToFocus")
    topics_to_avoid: List[str] = Field(..., alias="topicsToAvoid")
    custom_questions: List[str] = Field(..., alias="customQuestions")
    interview_style: str = Field(..., alias="interviewStyle")
    feedback_detail: str = Field(..., alias="feedbackDetail")


class Configuration(BaseModel):
    language: str
    voice_id: Optional[str] = Field(None, alias="voiceId")
    enable_transcription: bool = Field(..., alias="enableTranscription")
    audio_quality: str = Field(..., alias="audioQuality")
    time_zone: str = Field(..., alias="timeZone")


class Session(BaseModel):
    session_id: str = Field(..., alias="sessionId")
    callback_url: str = Field(..., alias="callbackUrl")


class SessionRequest(BaseModel):
    session: Session
    candidate: Candidate
    job: Job
    interview: Interview
    configuration: Configuration


class SessionResponse(BaseModel):
    success: bool
    session_id: str = Field(..., alias="sessionId")
    join_url: str = Field(..., alias="joinUrl")
    expiry: str
    status: str


class SessionStatusResponse(BaseModel):
    session_id: str = Field(..., alias="sessionId")
    status: str
    candidate_id: str = Field(..., alias="candidateId")
    job_id: str = Field(..., alias="jobId")
    start_time: Optional[str] = Field(None, alias="startTime")
    end_time: Optional[str] = Field(None, alias="endTime")
    duration: int
    progress: int
    questions_asked: int = Field(..., alias="questionsAsked")


class EndSessionRequest(BaseModel):
    reason: Optional[str] = None


class EndSessionResponse(BaseModel):
    success: bool
    session_id: str = Field(..., alias="sessionId")
    status: str
    duration: int


class QuestionEvaluation(BaseModel):
    score: int
    feedback: str
    key_insights: List[str] = Field(..., alias="keyInsights")


class Question(BaseModel):
    question_id: str = Field(..., alias="questionId")
    question: str
    timestamp: str
    answer_transcript: str = Field(..., alias="answerTranscript")
    answer_duration: int = Field(..., alias="answerDuration")
    evaluation: QuestionEvaluation


class Feedback(BaseModel):
    summary: str
    strengths: List[str]
    areas_for_improvement: List[str] = Field(..., alias="areasForImprovement")
    technical_assessment: str = Field(..., alias="technicalAssessment")
    communication_assessment: str = Field(..., alias="communicationAssessment")
    fit_score: int = Field(..., alias="fitScore")
    recommendation: str


class Transcript(BaseModel):
    full: str
    url: str


class Audio(BaseModel):
    url: str
    duration: int


class InterviewResultsResponse(BaseModel):
    session_id: str = Field(..., alias="sessionId")
    candidate_id: str = Field(..., alias="candidateId")
    job_id: str = Field(..., alias="jobId")
    company_id: str = Field(..., alias="companyId")
    overall_score: int = Field(..., alias="overallScore")
    feedback: Feedback
    questions: List[Question]
    transcript: Transcript
    audio: Audio


class WebhookRequest(BaseModel):
    url: str
    secret: str
    events: List[str]


class WebhookEvent(BaseModel):
    event: str
    timestamp: str
    session_id: str = Field(..., alias="sessionId")
    data: Dict[str, Any]


class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None