// Sample JSON configuration for the interview session
const sampleJson = {
    "session": {
        "sessionId": "demo-session-" + Date.now(),
        "callbackUrl": "https://example.com/webhook"
    },
    "candidate": {
        "candidateId": "candidate-123",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "resumeData": {
            "skills": [
                "JavaScript", "React", "Node.js", "Python", "SQL", "AWS"
            ],
            "experience": [
                {
                    "company": "Tech Solutions Inc.",
                    "role": "Senior Frontend Developer",
                    "duration": "2 years",
                    "description": "Developed and maintained web applications using React and Redux."
                },
                {
                    "company": "Digital Innovations",
                    "role": "Full Stack Developer",
                    "duration": "3 years",
                    "description": "Built RESTful APIs with Node.js and Express, and implemented frontend using React."
                }
            ],
            "education": [
                {
                    "institution": "University of Technology",
                    "degree": "Bachelor of Science",
                    "fieldOfStudy": "Computer Science",
                    "year": 2018
                }
            ],
            "projects": [
                {
                    "name": "E-commerce Platform",
                    "description": "Developed a full-stack e-commerce platform with React, Node.js, and MongoDB.",
                    "technologies": ["React", "Node.js", "Express", "MongoDB"]
                },
                {
                    "name": "Task Management App",
                    "description": "Created a task management application with real-time updates using Socket.io.",
                    "technologies": ["React", "Socket.io", "Express", "PostgreSQL"]
                }
            ],
            "rawText": "John Doe is a skilled software developer with 5+ years of experience in web development. Proficient in JavaScript, React, Node.js, Python, SQL, and AWS. Strong problem-solving abilities and excellent communication skills. Passionate about creating efficient, scalable, and user-friendly applications."
        }
    },
    "job": {
        "jobId": "job-456",
        "companyId": "company-789",
        "recruiterUserId": "recruiter-101",
        "title": "Senior Frontend Developer",
        "department": "Engineering",
        "description": "We are looking for a Senior Frontend Developer to join our team and help build innovative web applications.",
        "requirements": [
            "5+ years of experience in frontend development",
            "Strong proficiency in JavaScript, HTML, CSS",
            "Experience with React and state management libraries",
            "Knowledge of responsive design and cross-browser compatibility",
            "Understanding of RESTful APIs and asynchronous request handling"
        ],
        "responsibilities": [
            "Develop and maintain frontend components using React",
            "Collaborate with backend developers to integrate frontend with APIs",
            "Optimize applications for maximum speed and scalability",
            "Implement responsive design and ensure cross-browser compatibility",
            "Participate in code reviews and provide constructive feedback"
        ],
        "location": "San Francisco, CA (Remote)",
        "employmentType": "Full-time",
        "experienceLevel": "Senior",
        "salaryRange": {
            "min": 120000,
            "max": 150000,
            "currency": "USD"
        }
    },
    "interview": {
        "duration": 30,
        "difficultyLevel": "Medium",
        "topicsToFocus": [
            "React", "JavaScript", "Frontend Architecture", "Performance Optimization"
        ],
        "topicsToAvoid": [
            "Backend Development", "Database Design"
        ],
        "customQuestions": [
            "Can you explain your approach to component design in React?",
            "How do you handle state management in large applications?",
            "What strategies do you use for optimizing frontend performance?",
            "Describe a challenging project you worked on and how you overcame obstacles."
        ],
        "interviewStyle": "Conversational",
        "feedbackDetail": "Comprehensive"
    },
    "configuration": {
        "language": "en-US",
        "voiceId": "terrence",
        "enableTranscription": true,
        "audioQuality": "high",
        "timeZone": "America/Los_Angeles"
    }
};

// Function to load sample JSON into the textarea
function loadSampleJson() {
    document.getElementById('json-input').value = JSON.stringify(sampleJson, null, 2);
}

// Add event listener to the load sample button
document.addEventListener('DOMContentLoaded', function() {
    const loadSampleButton = document.getElementById('load-sample');
    if (loadSampleButton) {
        loadSampleButton.addEventListener('click', loadSampleJson);
    }
});