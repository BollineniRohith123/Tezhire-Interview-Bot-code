// Global variables
let currentSessionId = null;
let currentCallId = null;
let apiKey = 'YOUR_API_KEY'; // In a real application, this would be securely stored or obtained from the user

// DOM elements
document.addEventListener('DOMContentLoaded', function() {
    // Initialize event listeners
    const validateJsonButton = document.getElementById('validate-json');
    const createSessionButton = document.getElementById('create-session');
    const endInterviewButton = document.getElementById('end-interview');
    
    if (validateJsonButton) {
        validateJsonButton.addEventListener('click', validateJson);
    }
    
    if (createSessionButton) {
        createSessionButton.addEventListener('click', createInterviewSession);
    }
    
    if (endInterviewButton) {
        endInterviewButton.addEventListener('click', endInterviewSession);
    }
});

// Function to validate JSON input
function validateJson() {
    const jsonInput = document.getElementById('json-input').value;
    
    try {
        const parsedJson = JSON.parse(jsonInput);
        
        // Check for required fields
        if (!parsedJson.session || !parsedJson.session.sessionId) {
            showNotification('Session ID is required', 'error');
            return false;
        }
        
        if (!parsedJson.candidate || !parsedJson.candidate.candidateId || !parsedJson.candidate.name || !parsedJson.candidate.email) {
            showNotification('Candidate information is incomplete', 'error');
            return false;
        }
        
        if (!parsedJson.job || !parsedJson.job.jobId || !parsedJson.job.companyId || !parsedJson.job.title) {
            showNotification('Job information is incomplete', 'error');
            return false;
        }
        
        showNotification('JSON is valid', 'success');
        return true;
    } catch (error) {
        showNotification('Invalid JSON format: ' + error.message, 'error');
        return false;
    }
}

// Function to create an interview session
async function createInterviewSession() {
    if (!validateJson()) {
        return;
    }
    
    const jsonInput = document.getElementById('json-input').value;
    const parsedJson = JSON.parse(jsonInput);
    
    // In a real application, this would make an API call to the backend
    // For demo purposes, we'll simulate the API call
    
    try {
        // Show loading state
        showNotification('Creating interview session...', 'info');
        
        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // Simulate API response
        const response = {
            success: true,
            sessionId: parsedJson.session.sessionId,
            joinUrl: `https://api.ultravox.ai/join/${Math.random().toString(36).substring(2, 15)}`,
            expiry: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
            status: 'created'
        };
        
        // Store session ID
        currentSessionId = response.sessionId;
        
        // Show success notification
        showNotification('Interview session created successfully', 'success');
        
        // Start the WebRTC call
        startWebRTCCall(response.joinUrl);
    } catch (error) {
        showNotification('Error creating interview session: ' + error.message, 'error');
    }
}

// Function to start the WebRTC call
function startWebRTCCall(joinUrl) {
    // Show the interview section
    document.getElementById('interview-section').style.display = 'block';
    
    // Update status
    updateCallStatus('Connecting...', 'connecting');
    
    // In a real application, this would initialize the WebRTC connection
    // For demo purposes, we'll simulate the WebRTC call
    
    // Create iframe for WebRTC (in a real implementation, this would be replaced with actual WebRTC code)
    const webrtcContainer = document.getElementById('webrtc-container');
    webrtcContainer.innerHTML = '';
    
    const iframe = document.createElement('iframe');
    iframe.src = joinUrl;
    iframe.width = '100%';
    iframe.height = '400px';
    iframe.style.border = 'none';
    iframe.allow = 'camera; microphone; display-capture; autoplay; clipboard-write';
    
    webrtcContainer.appendChild(iframe);
    
    // Simulate connection established after a delay
    setTimeout(() => {
        updateCallStatus('Connected', 'connected');
        
        // Simulate interview questions being asked
        simulateInterview();
    }, 2000);
}

// Function to simulate the interview process
function simulateInterview() {
    // In a real application, this would be handled by the WebRTC call
    // For demo purposes, we'll simulate the interview process
    
    // Simulate interview duration (shortened for demo)
    setTimeout(() => {
        // End the interview automatically after the simulated duration
        endInterviewSession(true);
    }, 10000); // 10 seconds for demo purposes
}

// Function to end the interview session
async function endInterviewSession(automatic = false) {
    if (!currentSessionId) {
        showNotification('No active interview session', 'error');
        return;
    }
    
    try {
        // Show loading state
        if (!automatic) {
            showNotification('Ending interview session...', 'info');
        }
        
        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Update status
        updateCallStatus('Disconnected', 'disconnected');
        
        // Hide the interview section
        document.getElementById('interview-section').style.display = 'none';
        
        // Show the summary section
        document.getElementById('summary-section').style.display = 'block';
        
        // Generate and display the interview summary
        generateInterviewSummary();
        
        // Show success notification
        if (!automatic) {
            showNotification('Interview session ended successfully', 'success');
        }
    } catch (error) {
        showNotification('Error ending interview session: ' + error.message, 'error');
    }
}

// Function to generate the interview summary
function generateInterviewSummary() {
    // In a real application, this would make an API call to get the interview results
    // For demo purposes, we'll generate a mock summary
    
    // Generate random scores
    const technicalScore = Math.floor(Math.random() * 30) + 70; // 70-100
    const communicationScore = Math.floor(Math.random() * 30) + 70; // 70-100
    const overallScore = Math.floor((technicalScore + communicationScore) / 2);
    
    // Update score displays
    document.getElementById('technical-score').textContent = technicalScore;
    document.getElementById('communication-score').textContent = communicationScore;
    document.getElementById('overall-score').textContent = overallScore;
    
    // Generate summary text
    const summaryText = `The candidate demonstrated strong technical knowledge in frontend development, particularly in React and JavaScript. Their communication was clear and professional throughout the interview.`;
    document.getElementById('summary-text').textContent = summaryText;
    
    // Generate strengths
    const strengths = [
        'Strong understanding of React component architecture',
        'Excellent knowledge of JavaScript fundamentals',
        'Clear communication of technical concepts',
        'Good problem-solving approach'
    ];
    
    const strengthsList = document.getElementById('strengths-list');
    strengthsList.innerHTML = '';
    strengths.forEach(strength => {
        const li = document.createElement('li');
        li.textContent = strength;
        strengthsList.appendChild(li);
    });
    
    // Generate areas for improvement
    const improvements = [
        'Could improve knowledge of advanced performance optimization techniques',
        'More experience with state management libraries would be beneficial',
        'Consider deepening understanding of frontend testing methodologies'
    ];
    
    const improvementList = document.getElementById('improvement-list');
    improvementList.innerHTML = '';
    improvements.forEach(improvement => {
        const li = document.createElement('li');
        li.textContent = improvement;
        improvementList.appendChild(li);
    });
    
    // Generate recommendation
    let recommendation = '';
    if (overallScore >= 85) {
        recommendation = 'Strong Hire - The candidate demonstrates excellent technical skills and communication abilities that would be a great fit for the role.';
    } else if (overallScore >= 75) {
        recommendation = 'Hire - The candidate has the necessary skills and experience for the position with some areas for growth.';
    } else {
        recommendation = 'Consider - The candidate shows potential but may need additional training or experience in key areas.';
    }
    
    document.getElementById('recommendation-text').textContent = recommendation;
    
    // Generate transcript
    const transcript = `
Interviewer: Hello, thank you for joining us today. Could you start by introducing yourself and your background in frontend development?

Candidate: Hi, thank you for having me. I'm John Doe, a frontend developer with over 5 years of experience. I've been working primarily with React and JavaScript, building responsive and user-friendly web applications.

Interviewer: Great. Can you explain your approach to component design in React?

Candidate: I follow a modular approach to component design. I break down the UI into reusable components, focusing on single responsibility. I use composition over inheritance and ensure components are loosely coupled. For state management, I determine whether state should be local or global based on its usage across the application.

Interviewer: How do you handle state management in large applications?

Candidate: For large applications, I prefer using Redux or Context API depending on the complexity. Redux works well for complex state with many actions, while Context API is simpler for less complex state. I also follow best practices like normalizing state shape and using selectors for derived data.

Interviewer: What strategies do you use for optimizing frontend performance?

Candidate: I focus on several areas: code splitting to reduce bundle size, memoization with React.memo and useMemo to prevent unnecessary re-renders, lazy loading for components and images, and optimizing network requests with techniques like caching and request batching.

Interviewer: Describe a challenging project you worked on and how you overcame obstacles.

Candidate: I worked on a real-time dashboard that needed to display data from multiple sources with frequent updates. The challenge was maintaining performance while handling constant data updates. I implemented a virtualized list for rendering only visible items, used WebSockets for efficient real-time updates, and optimized render cycles with memoization and careful state management.
`;
    
    document.getElementById('transcript').textContent = transcript;
}

// Function to update the call status
function updateCallStatus(statusText, statusClass) {
    const statusIndicator = document.getElementById('status-indicator');
    const statusTextElement = document.getElementById('status-text');
    
    statusTextElement.textContent = statusText;
    
    // Remove all status classes
    statusIndicator.classList.remove('connected', 'error');
    
    // Add the current status class
    if (statusClass === 'connected') {
        statusIndicator.classList.add('connected');
    } else if (statusClass === 'error') {
        statusIndicator.classList.add('error');
    }
}

// Function to show notifications
function showNotification(message, type = 'info') {
    // In a real application, this would use a proper notification system
    // For demo purposes, we'll use alert
    alert(`${type.toUpperCase()}: ${message}`);
}