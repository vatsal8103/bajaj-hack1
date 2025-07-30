css = """
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* Global Styles */
.main {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #ffeef8 0%, #f0f8ff 100%);
    min-height: 100vh;
    padding: 1rem;
}

/* Header Styling */
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 20px;
    margin-bottom: 1rem;
    text-align: center;
    box-shadow: 0 10px 40px rgba(102, 126, 234, 0.2);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.main-header h1 {
    margin: 0;
    font-size: 2.2rem;
    font-weight: 700;
    color: white;
    text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
    font-family: 'Poppins', sans-serif;
}

.main-header p {
    margin: 0.5rem 0 0 0;
    color: rgba(255, 255, 255, 0.9);
    font-size: 1rem;
    font-weight: 400;
}

/* Search Container with Plus Button */
.search-container {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 1rem 0;
    background: rgba(255, 255, 255, 0.9);
    padding: 8px;
    border-radius: 20px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.3);
}

/* Small Plus Button */
.plus-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 18px;
    font-weight: bold;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.plus-btn:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
}

/* Fixed Upload Modal - Removed overlay issues */
.upload-modal-container {
    position: relative;
    z-index: 1000;
    margin: 1rem 0;
}

.upload-modal {
    background: rgba(255, 255, 255, 0.98);
    padding: 1.5rem;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    animation: slideDown 0.3s ease-out;
    margin-bottom: 1rem;
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

/* Right Panel Styling */
.right-panel {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    height: fit-content;
    position: sticky;
    top: 20px;
}

.panel-section {
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(102, 126, 234, 0.1);
}

.panel-section:last-child {
    border-bottom: none;
    margin-bottom: 0;
}

.panel-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #667eea;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Chat Messages with Subtle Colors */
.chat-message {
    padding: 1.2rem 1.5rem;
    border-radius: 20px;
    margin: 1rem 0;
    max-width: 85%;
    animation: fadeInUp 0.4s ease-out;
    word-wrap: break-word;
    line-height: 1.6;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
}

.chat-message.user {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    margin-left: auto;
    margin-right: 0;
    border-bottom-right-radius: 8px;
}

.chat-message.bot {
    background: linear-gradient(135deg, #f8f9ff 0%, #e6f3ff 100%);
    color: #2d3748;
    margin-left: 0;
    margin-right: auto;
    border-bottom-left-radius: 8px;
    border: 1px solid rgba(102, 126, 234, 0.1);
}

/* Status Indicators with Subtle Colors */
.status-indicator {
    padding: 0.6rem 1.2rem;
    border-radius: 15px;
    text-align: center;
    font-weight: 500;
    margin: 0.8rem 0;
    font-size: 0.9rem;
}

.status-ready {
    background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
    color: #155724;
    border: 1px solid #c3e6cb;
}

.status-waiting {
    background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
    color: #856404;
    border: 1px solid #ffeaa7;
}

/* Quick Actions Buttons */
.quick-btn {
    background: linear-gradient(135deg, #f8f9ff 0%, #e6f3ff 100%);
    color: #667eea;
    border: 1px solid rgba(102, 126, 234, 0.2);
    border-radius: 10px;
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
    font-weight: 500;
    transition: all 0.3s ease;
    cursor: pointer;
    width: 100%;
    margin-bottom: 0.5rem;
}

.quick-btn:hover {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* Control Buttons */
.control-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    font-weight: 500;
    transition: all 0.3s ease;
    cursor: pointer;
    width: 100%;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
}

.control-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

/* Stats Display */
.stats-container {
    background: linear-gradient(135deg, #f8f9ff 0%, #e6f3ff 100%);
    border-radius: 12px;
    padding: 1rem;
    border: 1px solid rgba(102, 126, 234, 0.1);
    font-size: 0.85rem;
}

.stats-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.3rem;
    color: #4a5568;
}

.stats-item:last-child {
    margin-bottom: 0;
}

/* Response Length Pills */
.length-pills {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
}

.length-pill {
    background: rgba(102, 126, 234, 0.1);
    color: #667eea;
    border: 1px solid rgba(102, 126, 234, 0.2);
    border-radius: 20px;
    padding: 0.4rem 0.8rem;
    font-size: 0.75rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
}

.length-pill.active {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-color: #667eea;
}

.length-pill:hover {
    background: rgba(102, 126, 234, 0.2);
    transform: translateY(-1px);
}

/* Typing Indicator */
.typing-indicator {
    display: flex;
    align-items: center;
    padding: 1rem 1.5rem;
    background: linear-gradient(135deg, #f8f9ff 0%, #e6f3ff 100%);
    border-radius: 20px;
    margin: 1rem 0;
    max-width: 100px;
    animation: fadeInUp 0.4s ease-out;
    border: 1px solid rgba(102, 126, 234, 0.1);
}

.typing-dots {
    display: flex;
    gap: 4px;
}

.typing-dots span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #667eea;
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

/* File Upload Styling */
.upload-section {
    background: rgba(102, 126, 234, 0.05);
    border: 2px dashed rgba(102, 126, 234, 0.2);
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.upload-section:hover {
    border-color: rgba(102, 126, 234, 0.4);
    background: rgba(102, 126, 234, 0.1);
}

/* Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
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

/* Responsive Design */
@media (max-width: 768px) {
    .chat-message {
        max-width: 95%;
    }
    
    .upload-modal {
        width: 95%;
        margin: 0.5rem;
    }
    
    .right-panel {
        position: relative;
        top: 0;
    }
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
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
