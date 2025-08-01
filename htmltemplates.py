css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

:root {
    --primary-color: #4a5568;
    --secondary-color: #718096;
    --accent-color: #2d3748;
    --background-color: #f8fafc;
    --surface-color: #ffffff;
    --text-primary: #2d3748;
    --text-secondary: #4a5568;
    --border-color: #e2e8f0;
    --success-color: #38a169;
    --warning-color: #d69e2e;
    --error-color: #e53e3e;
    --soft-blue: #ebf4ff;
    --soft-gray: #f7fafc;
    --input-background: #ffffff;
    --button-background: #f5f5f5;
    --button-hover-background: #e9ecef;
}

/* Critical: Remove overflow hidden from these elements */
html, body {
    height: 100vh !important;
    max-height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
}

[data-testid="stAppViewContainer"] {
    height: 100vh !important;
    max-height: 100vh !important;
    overflow: hidden !important;
}

.stApp {
    height: 100vh !important;
    max-height: 100vh !important;
    overflow: hidden !important;
}

/* Main content container - CRITICAL FIXES */
.main {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, var(--soft-gray) 0%, var(--soft-blue) 100%);
    height: 100vh !important;
    max-height: 100vh !important;
    padding: 1rem 1rem 0 1rem !important; /* Remove bottom padding */
    overflow: hidden !important;
    position: relative !important;
    display: flex !important;
    flex-direction: column !important;
}

.stApp > div:first-child {
    border: none !important;
    background: transparent !important;
}

/* Content area that can scroll */
.main .block-container {
    padding: 0 !important;
    max-width: none !important;
    height: calc(100vh - 90px) !important; /* Account for fixed input height */
    overflow-y: auto !important; /* Allow scrolling here */
    overflow-x: hidden !important;
    flex: 1 !important;
    margin-bottom: 0 !important;
}

/* FIXED INPUT BAR - ABSOLUTE POSITIONING */
.window-bottom-input {
    position: absolute !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    width: 100% !important;
    height: auto !important;
    z-index: 9999 !important;
    background: var(--surface-color) !important;
    border-top: 2px solid var(--border-color) !important;
    padding: 0.75rem 1rem !important;
    box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.15) !important;
    backdrop-filter: blur(10px) !important;
}

/* Alternative fixed input bar class */
.fixed-input-bar {
    position: absolute !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    width: 100% !important;
    background: var(--surface-color) !important;
    border-top: 2px solid var(--border-color) !important;
    padding: 0.75rem 1rem !important;
    z-index: 9999 !important;
    box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.15) !important;
    backdrop-filter: blur(10px) !important;
}

.input-bar-container {
    max-width: 1200px !important;
    margin: 0 auto !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    height: auto !important;
}

/* Ensure Streamlit containers don't interfere */
.stColumns {
    gap: 8px !important;
}

/* Scrollable content area */
.scrollable-content-area {
    overflow-y: auto !important;
    overflow-x: hidden !important;
    height: 100% !important;
    margin-bottom: 0 !important;
    padding-bottom: 20px !important;
    scroll-behavior: smooth !important;
}

/* Chat messages - ensure they don't go behind input */
.chat-message {
    padding: 1.2rem 1.5rem;
    border-radius: 20px;
    margin: 1rem 0;
    max-width: 85%;
    animation: fadeInUp 0.4s ease-out;
    word-wrap: break-word;
    line-height: 1.6;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    scroll-margin-bottom: 100px !important; /* Prevent hiding behind input */
    margin-bottom: 1.5rem;
}

.chat-message:last-child {
    margin-bottom: 2rem !important; /* Extra space for last message */
}

/* Rest of your existing styles... */
.main-header {
    position: sticky;
    top: 0;
    z-index: 999;
    padding: 1rem 0;
    margin-bottom: 1rem;
    border-bottom: 1px solid var(--border-color);
}

.sidebar .sidebar-content {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    border-radius: 15px;
    padding: 1rem;
}

.sidebar-header {
    font-size: 1rem;
    font-weight: 600;
    color: white;
    text-align: center;
    margin-bottom: 0.8rem;
    padding: 0.6rem;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    backdrop-filter: blur(10px);
}

.session-item {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 0.6rem;
    margin-bottom: 0.4rem;
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.session-item:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
}

.current-session {
    background: rgba(255, 255, 255, 0.25) !important;
    border: 2px solid rgba(255, 255, 255, 0.4) !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.session-time {
    font-size: 0.7rem;
    color: rgba(255, 255, 255, 0.7);
    text-align: center;
    margin-top: 0.3rem;
}

.current-session-indicator {
    background: var(--surface-color);
    color: var(--text-primary);
    padding: 0.5rem 1rem;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 1rem;
    font-weight: 500;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    border: 1px solid var(--border-color);
}


@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.compact-section {
    margin-bottom: 1rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid var(--border-color);
}

.compact-section:last-child {
    border-bottom: none;
    margin-bottom: 0;
}

.compact-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 6px;
}

.chat-message.user {
    background: var(--primary-color);
    color: white;
    margin-left: auto;
    margin-right: 0;
    border-bottom-right-radius: 8px;
}

.chat-message.bot {
    background: var(--soft-blue);
    color: var(--text-primary);
    margin-left: 0;
    margin-right: auto;
    border-bottom-left-radius: 8px;
    border: 1px solid var(--border-color);
}

.chat-message.bot.chatgpt-style {
    background: var(--surface-color);
    border: 1px solid var(--border-color);
}

.source-indicator {
    text-align: left;
    margin-left: 0;
    font-size: 0.8rem;
    color: #4a5568;
    margin-top: -0.5rem;
    margin-bottom: 1rem;
    opacity: 0.7;
}

@keyframes smoothScrollUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.chat-message:last-child {
    animation: smoothScrollUp 0.5s ease-out;
}

.status-indicator {
    padding: 0.4rem 0.8rem;
    border-radius: 12px;
    text-align: center;
    font-weight: 500;
    margin: 0.5rem 0;
    font-size: 0.8rem;
}

.status-ready {
    background: rgba(56, 161, 105, 0.1);
    color: var(--success-color);
    border: 1px solid rgba(56, 161, 105, 0.2);
}

.status-waiting {
    background: rgba(214, 158, 46, 0.1);
    color: var(--warning-color);
    border: 1px solid rgba(214, 158, 46, 0.2);
}

.stats-container {
    background: var(--soft-gray);
    border-radius: 8px;
    padding: 0.8rem;
    border: 1px solid var(--border-color);
    font-size: 0.8rem;
}

.stats-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.2rem;
    color: var(--text-secondary);
}

.stats-item:last-child {
    margin-bottom: 0;
}

.typing-indicator {
    display: flex;
    align-items: center;
    padding: 1rem 1.5rem;
    background: var(--soft-blue);
    border-radius: 20px;
    margin: 1rem 0;
    max-width: 100px;
    animation: fadeInUp 0.4s ease-out;
    border: 1px solid var(--border-color);
}

.typing-dots {
    display: flex;
    gap: 4px;
}

.typing-dots span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--primary-color);
    animation: typingAnimation 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) { animation-delay: -0.32s; }
.typing-dots span:nth-child(2) { animation-delay: -0.16s; }
.typing-dots span:nth-child(3) { animation-delay: 0s; }

@keyframes typingAnimation {
    0%, 80%, 100% { 
        transform: scale(0.8);
        opacity: 0.5;
    }
    40% { 
        transform: scale(1);
        opacity: 1;
    }
}
/* Upload Modal Fixes - Add these to your existing CSS */

/* Hide any default Streamlit file uploader dialogs */
.stFileUploader > div {
    position: relative !important;
    z-index: 10001 !important;
}


/* Upload modal container */


/* Modal animation */
@keyframes modalSlideIn {
    from {
        opacity: 0;
        transform: scale(0.9) translateY(-20px);
    }
    to {
        opacity: 1;
        transform: scale(1) translateY(0);
    }
}

/* Hide default Streamlit file uploader when modal is open */
.modal-open .stFileUploader {
    pointer-events: none !important;
    opacity: 0.5 !important;
}

/* Prevent body scroll when modal is open */
.modal-open {
    overflow: hidden !important;
}

/* Upload button styling in fixed bar */
.window-bottom-input button[data-testid*="upload"],
.fixed-input-bar button[data-testid*="upload"] {
    background: var(--button-background) !important;
    border: 2px solid var(--border-color) !important;
    border-radius: 50% !important;
    width: 45px !important;
    height: 45px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.2s ease !important;
    z-index: 1002 !important;
    position: relative !important;
}

.window-bottom-input button[data-testid*="upload"]:hover,
.fixed-input-bar button[data-testid*="upload"]:hover {
    background: var(--button-hover-background) !important;
    transform: scale(1.1) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
}

/* Fix for Streamlit's internal file uploader dialog */
div[data-testid="stFileUploader"] > div > div {
    display: none !important;
}



/* Close button for modal */
.modal-close-btn {
    position: absolute !important;
    top: 1rem !important;
    right: 1rem !important;
    background: none !important;
    border: none !important;
    font-size: 24px !important;
    cursor: pointer !important;
    color: var(--text-secondary) !important;
    z-index: 10002 !important;
    width: 32px !important;
    height: 32px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border-radius: 50% !important;
    transition: all 0.2s ease !important;
}

.modal-close-btn:hover {
    background: var(--border-color) !important;
    color: var(--text-primary) !important;
}


/* Prevent interference with your fixed input bar */
.window-bottom-input,
.fixed-input-bar {
    z-index: 1000 !important;
}

/* When modal is open, reduce z-index of input bar */
.modal-open .window-bottom-input,
.modal-open .fixed-input-bar {
    z-index: 999 !important;
}


@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* CRITICAL: Streamlit input styling */
.stChatInput {
    position: relative !important;
    z-index: 10000 !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 25px !important;
    background: var(--input-background) !important;
}

.stChatInput > div {
    border-radius: 25px !important;
    border: 1px solid var(--border-color) !important;
    background: var(--input-background) !important;
}

.stChatInput > div > div {
    border-radius: 25px !important;
    border: 1px solid var(--border-color) !important;
}

.stChatInput textarea {
    border: none !important;
    outline: none !important;
    resize: none !important;
    padding: 12px 20px !important;
    font-size: 14px !important;
    line-height: 1.4 !important;
    background: transparent !important;
}

/* Button styling */
.window-bottom-input button,
.fixed-input-bar button {
    border-radius: 50% !important;
    border: 1px solid var(--border-color) !important;
    background: var(--button-background) !important;
    color: var(--text-primary) !important;
    transition: all 0.2s ease !important;
    min-width: 45px !important;
    min-height: 45px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

.window-bottom-input button:hover,
.fixed-input-bar button:hover {
    background: var(--button-hover-background) !important;
    transform: scale(1.05) !important;
}

/* Hide default Streamlit chat input */
.stChatFloatingInputContainer {
    display: none !important;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: var(--soft-gray);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb {
    background: var(--primary-color);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--accent-color);
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .main {
        padding: 0.5rem 0.5rem 0 0.5rem !important;
    }
    
    .main .block-container {
        height: calc(100vh - 80px) !important;
    }
    
    .window-bottom-input,
    .fixed-input-bar {
        padding: 0.5rem !important;
        height: auto !important;
    }
    
    .chat-message {
        max-width: 95%;
    }

    
    .input-bar-container {
        margin: 0 !important;
        padding: 0 !important;
        gap: 4px !important;
    }
    
    .window-bottom-input button,
    .fixed-input-bar button {
        min-width: 40px !important;
        min-height: 40px !important;
        font-size: 16px !important;
    }
    
    .stChatInput textarea {
        padding: 10px 16px !important;
        font-size: 13px !important;
    }
}

/* Tablet responsiveness */
@media (max-width: 1024px) and (min-width: 769px) {
    .main {
        padding: 0.75rem 0.75rem 0 0.75rem !important;
    }
    
    .main .block-container {
        height: calc(100vh - 85px) !important;
    }
}

.main-content-wrapper {
    height: 100% !important;
    overflow: hidden !important;
    display: flex !important;
    flex-direction: column !important;
}

.element-container {
    max-height: none !important;
}

[data-testid="stSidebar"] {
    max-height: 100vh !important;
    overflow-y: auto !important;
}

/* Additional utility classes */
.no-scroll {
    overflow: hidden !important;
}

.full-height {
    height: 100vh !important;
    max-height: 100vh !important;
}
</style>
"""
