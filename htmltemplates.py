css = """
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* Color Variables - More Subdued Palette */
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
}

/* Global Styles - Remove big white box */
.main {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, var(--soft-gray) 0%, var(--soft-blue) 100%);
    min-height: 100vh;
    padding: 1rem;
    padding-bottom: 90px !important; /* Space for fixed input */
}

/* Remove Streamlit's default containers */
.stApp > div:first-child {
    border: none !important;
    background: transparent !important;
}

/* Fixed bottom input - stays at window bottom */
.fixed-bottom-input {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: var(--surface-color);
    border-top: 2px solid var(--border-color);
    padding: 0.8rem 1rem;
    z-index: 1000;
    box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.1);
}

.input-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: 8px;
    background: var(--surface-color);
    padding: 6px;
    border-radius: 25px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    border: 1px solid var(--border-color);
}

/* Chat area - clean without big white box */
.chat-area {
    height: calc(100vh - 160px);
    overflow-y: auto;
    padding: 0;
    margin: 0;
    background: transparent;
}

/* Fixed input buttons */
.fixed-bottom-input .stButton > button {
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    transition: all 0.3s ease;
    padding: 0;
}

.fixed-bottom-input .stButton > button:hover {
    background: var(--accent-color);
    transform: scale(1.1);
}

/* Custom scrollbar for chat area */
.chat-area::-webkit-scrollbar {
    width: 6px;
}

.chat-area::-webkit-scrollbar-track {
    background: var(--soft-gray);
    border-radius: 3px;
}

.chat-area::-webkit-scrollbar-thumb {
    background: var(--primary-color);
    border-radius: 3px;
}

.chat-area::-webkit-scrollbar-thumb:hover {
    background: var(--accent-color);
}

/* Sidebar Styles - More Compact */
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

/* Current Session Indicator */
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

/* Upload Modal Overlay */
.upload-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.6);
    z-index: 2000;
    display: flex;
    align-items: center;
    justify-content: center;
}

.upload-modal {
    background: var(--surface-color);
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    border: 1px solid var(--border-color);
    max-width: 800px;
    width: 90%;
    max-height: 80vh;
    overflow-y: auto;
    position: relative;
    z-index: 2001;
    animation: slideDown 0.3s ease-out;
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

/* Compact right panel */
# .compact-right-panel {
#     background: var(--surface-color);
#     border-radius: 15px;
#     padding: 1rem;
#     box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
#     border: 1px solid var(--border-color);
#     height: calc(100vh - 160px);
#     overflow-y: auto;
#     position: sticky;
#     top: 20px;
# }

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

/* Compact buttons */
.compact-right-panel .stButton > button {
    background: var(--surface-color);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 0.4rem 0.8rem;
    font-weight: 500;
    font-size: 0.85rem;
    transition: all 0.3s ease;
    width: 100%;
    margin-bottom: 0.3rem;
}

.compact-right-panel .stButton > button:hover {
    background: var(--primary-color);
    color: white;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Chat Messages - Clean styling */
.chat-message {
    padding: 1.2rem 1.5rem;
    border-radius: 20px;
    margin: 1rem 0;
    max-width: 85%;
    animation: fadeInUp 0.4s ease-out;
    word-wrap: break-word;
    line-height: 1.6;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    scroll-margin-bottom: 20px;
    margin-bottom: 1.5rem;
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

/* Source indicator */
.source-indicator {
    text-align: left;
    margin-left: 0;
    font-size: 0.8rem;
    color: #4a5568;
    margin-top: -0.5rem;
    margin-bottom: 1rem;
    opacity: 0.7;
}

/* Auto-scroll animation */
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

/* Status Indicators */
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

/* Stats Display */
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

/* Typing Indicator */
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

/* Enhanced fade-in animation */
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

/* Hide Streamlit Elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* Custom scrollbar */
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

/* Responsive Design */
@media (max-width: 768px) {
    .chat-message {
        max-width: 95%;
    }
    
    .upload-modal {
        width: 95%;
        margin: 0.5rem;
    }
    
    .compact-right-panel {
        position: relative;
        top: 0;
        height: auto;
        padding: 0.8rem;
    }
    
    .fixed-bottom-input {
        padding: 0.5rem;
    }
    
    .input-container {
        margin: 0 5px;
        padding: 4px;
    }
    
    .chat-area {
        height: calc(100vh - 140px);
    }
    
    .fixed-bottom-input .stButton > button {
        width: 36px;
        height: 36px;
        font-size: 14px;
    }
    
    .main {
        padding-bottom: 70px !important;
    }
}
</style>
"""

# Templates
bot_template = """
<div class="chat-message bot">
    <div>{{MSG}}</div>
</div>
"""

user_template = """
<div class="chat-message user">
    <div>{{MSG}}</div>
</div>
"""
