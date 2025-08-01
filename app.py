import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredEmailLoader,
    WebBaseLoader
)
from langchain_groq import ChatGroq
import speech_recognition as sr
import pyttsx3
import time
import json
from datetime import datetime
from htmltemplates import css


# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Page configuration
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Load CSS
st.markdown(css, unsafe_allow_html=True)


# Chat Sessions Management
class ChatSessionManager:
    def __init__(self):
        self.sessions_file = "chat_sessions.json"
        
    def load_sessions(self):
        """Load chat sessions from file"""
        try:
            if os.path.exists(self.sessions_file):
                with open(self.sessions_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def save_sessions(self, sessions):
        """Save chat sessions to file"""
        try:
            with open(self.sessions_file, 'w') as f:
                json.dump(sessions, f, indent=2)
        except Exception as e:
            st.error(f"Error saving sessions: {str(e)}")
    
    def create_new_session(self):
        """Create a new chat session"""
        sessions = self.load_sessions()
        session_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        session_name = f"Chat {len(sessions) + 1}"
        
        sessions[session_id] = {
            "name": session_name,
            "created_at": datetime.now().isoformat(),
            "chat_history": [],
            "processed_docs": False,
            "vectorstore_data": None,
            "last_updated": datetime.now().isoformat()
        }
        
        self.save_sessions(sessions)
        return session_id
    
    def update_session(self, session_id, chat_history, processed_docs=False, vectorstore_data=None):
        """Update session data"""
        sessions = self.load_sessions()
        if session_id in sessions:
            sessions[session_id]["chat_history"] = chat_history
            sessions[session_id]["processed_docs"] = processed_docs
            if vectorstore_data:
                sessions[session_id]["vectorstore_data"] = vectorstore_data
            sessions[session_id]["last_updated"] = datetime.now().isoformat()
            self.save_sessions(sessions)
    
    def delete_session(self, session_id):
        """Delete a chat session"""
        sessions = self.load_sessions()
        if session_id in sessions:
            del sessions[session_id]
            self.save_sessions(sessions)
    
    def rename_session(self, session_id, new_name):
        """Rename a chat session"""
        sessions = self.load_sessions()
        if session_id in sessions:
            sessions[session_id]["name"] = new_name
            sessions[session_id]["last_updated"] = datetime.now().isoformat()
            self.save_sessions(sessions)


# Initialize session manager
session_manager = ChatSessionManager()


# Enhanced auto-scroll JavaScript function - ChatGPT-like
def add_auto_scroll():
    """Enhanced JavaScript for ChatGPT-like auto-scrolling"""
    st.markdown("""
    <script>
    function scrollToLatestMessage() {
        const chatContainer = document.querySelector('.scrollable-chat-container');
        if (chatContainer) {
            // Smooth scroll to bottom like ChatGPT
            chatContainer.scrollTo({
                top: chatContainer.scrollHeight,
                behavior: 'smooth'
            });
        }
        
        // Also find the last message and ensure it's visible
        const lastMessage = document.querySelector('.chat-message:last-of-type');
        if (lastMessage) {
            lastMessage.scrollIntoView({
                behavior: 'smooth',
                block: 'end'
            });
        }
    }
    
    // Observer for new messages - ChatGPT-style
    const observer = new MutationObserver(function(mutations) {
        let hasNewMessage = false;
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length > 0) {
                for (let node of mutation.addedNodes) {
                    if (node.nodeType === 1 && 
                        (node.classList?.contains('chat-message') || 
                         node.querySelector?.('.chat-message'))) {
                        hasNewMessage = true;
                        break;
                    }
                }
            }
        });
        
        if (hasNewMessage) {
            setTimeout(scrollToLatestMessage, 100);
        }
    });
    
    // Start observing
    if (document.body) {
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
    
    // Initial scroll
    setTimeout(scrollToLatestMessage, 300);
    </script>
    """, unsafe_allow_html=True)


# Initialize session state
def init_session_state():
    defaults = {
        "current_session_id": None,
        "conversation": None,
        "chat_history": [],
        "processed_docs": False,
        "is_processing": False,
        "vectorstore": None,
        "llm": None,
        "show_upload": False,
        "length_preference": "medium",
        "show_stats": False,
        "should_scroll": False,
        "sessions": {},
        "context_memory": {},
        "new_message": False,
        "chatgpt_mode": False  # New ChatGPT-like mode
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Load sessions
    st.session_state.sessions = session_manager.load_sessions()
    
    # Create initial session if none exists
    if not st.session_state.current_session_id and not st.session_state.sessions:
        st.session_state.current_session_id = session_manager.create_new_session()
        st.session_state.sessions = session_manager.load_sessions()


def load_session(session_id):
    """Load a specific chat session"""
    sessions = session_manager.load_sessions()
    if session_id in sessions:
        session_data = sessions[session_id]
        st.session_state.current_session_id = session_id
        st.session_state.chat_history = session_data.get("chat_history", [])
        st.session_state.processed_docs = session_data.get("processed_docs", False)
        
        # Load context memory for this session
        if session_id not in st.session_state.context_memory:
            st.session_state.context_memory[session_id] = []


def save_current_session():
    """Save current session data"""
    if st.session_state.current_session_id:
        session_manager.update_session(
            st.session_state.current_session_id,
            st.session_state.chat_history,
            st.session_state.processed_docs
        )


# Simple embedding function
@st.cache_resource
def create_simple_embeddings():
    """Create embeddings using OpenAI or simple text matching"""
    try:
        from langchain.embeddings import OpenAIEmbeddings
        return OpenAIEmbeddings()
    except:
        return None


# Process documents
@st.cache_data
def process_documents(pdf_docs, docx_docs, eml_docs, web_urls):
    documents = []
    
    def save_temp_file(uploaded_file):
        suffix = "." + uploaded_file.name.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(uploaded_file.read())
            return tmp_file.name

    loaders = [
        (pdf_docs, PyPDFLoader),
        (docx_docs, UnstructuredWordDocumentLoader),
        (eml_docs, UnstructuredEmailLoader)
    ]
    
    for docs, loader_class in loaders:
        for doc in docs:
            try:
                path = save_temp_file(doc)
                loader = loader_class(path)
                documents.extend(loader.load())
                os.remove(path)
            except Exception as e:
                st.error(f"Error processing {doc.name}: {str(e)}")

    if web_urls:
        try:
            loader = WebBaseLoader(web_urls)
            documents.extend(loader.load())
        except Exception as e:
            st.error(f"Error processing web URLs: {str(e)}")

    if not documents:
        return []
    
    full_text = "\n".join([doc.page_content for doc in documents])
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )
    return text_splitter.split_text(full_text)


@st.cache_resource
def create_vectorstore(text_chunks):
    try:
        embeddings = create_simple_embeddings()
        if embeddings:
            return Chroma.from_texts(texts=text_chunks, embedding=embeddings)
        else:
            return text_chunks
    except Exception as e:
        st.error(f"Embedding error: {str(e)}")
        return text_chunks


def initialize_llm():
    return ChatGroq(
        model_name="llama3-70b-8192",
        temperature=0.7,
        api_key=GROQ_API_KEY
    )


def get_context_for_session(session_id, current_question):
    """Get relevant context from session memory"""
    if session_id not in st.session_state.context_memory:
        st.session_state.context_memory[session_id] = []
    
    context_memory = st.session_state.context_memory[session_id]
    
    # Get last 5 exchanges for context
    recent_context = context_memory[-10:] if len(context_memory) > 10 else context_memory
    
    if recent_context:
        context_str = "\n".join([f"Q: {item['question']}\nA: {item['answer'][:200]}..." for item in recent_context])
        return f"Previous conversation context:\n{context_str}\n\nCurrent question: {current_question}"
    
    return current_question


def update_context_memory(session_id, question, answer):
    """Update context memory for the session"""
    if session_id not in st.session_state.context_memory:
        st.session_state.context_memory[session_id] = []
    
    st.session_state.context_memory[session_id].append({
        "question": question,
        "answer": answer,
        "timestamp": datetime.now().isoformat()
    })
    
    # Keep only last 20 exchanges to manage memory
    if len(st.session_state.context_memory[session_id]) > 20:
        st.session_state.context_memory[session_id] = st.session_state.context_memory[session_id][-20:]


def get_chatgpt_like_answer(question, llm, length_pref="medium", context=None):
    """Get ChatGPT-like conversational answer"""
    if length_pref == "short":
        format_instruction = "Provide a concise, helpful answer in a conversational tone, similar to ChatGPT. Keep it under 150 words."
    elif length_pref == "long":
        format_instruction = "Provide a detailed, comprehensive answer in a conversational and friendly tone, similar to ChatGPT. Include examples and explanations. Aim for 300-500 words."
    else:
        format_instruction = "Provide a well-structured, informative answer in a conversational tone, similar to ChatGPT. Aim for 200-300 words with good detail."
    
    # Include context if available
    context_instruction = ""
    if context and len(st.session_state.chat_history) > 0:
        context_instruction = f"\nPrevious conversation context: {context}\n"
    
    prompt = f"""You are a helpful AI assistant similar to ChatGPT. Be conversational, friendly, and informative in your responses.
{context_instruction}
Question: {question}

Instructions: {format_instruction}

Please provide a helpful, accurate, and engaging response that feels natural and conversational:"""
    
    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        return f"I apologize, but I encountered an error while processing your question: {str(e)}"


def get_general_knowledge_answer(question, llm, length_pref="medium", context=None):
    """Get general knowledge answer from LLM with context"""
    if st.session_state.chatgpt_mode:
        return get_chatgpt_like_answer(question, llm, length_pref, context)
    
    if length_pref == "short":
        format_instruction = "Provide a concise, helpful answer in 100-200 words with clear bullet points"
    elif length_pref == "long":
        format_instruction = "Provide a detailed, comprehensive answer in 400-600 words with examples, explanations, and thorough coverage"
    else:
        format_instruction = "Provide a well-structured, informative answer in 250-400 words with good detail and examples"
    
    # Include context if available
    context_instruction = ""
    if context and len(st.session_state.chat_history) > 0:
        context_instruction = f"\nContext from previous conversation: {context}\n"
    
    prompt = f"""You are a helpful AI assistant. Answer the following question using your general knowledge.
{context_instruction}
Question: {question}

Instructions: {format_instruction}

Please provide a helpful, accurate, and well-formatted response that considers the conversation context:"""
    
    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        return f"I apologize, but I encountered an error while processing your question: {str(e)}"


def get_document_based_answer(question, vectorstore, llm, length_pref="medium", context=None):
    """Get document-based answer using vectorstore with context"""
    if length_pref == "short":
        format_instruction = "Based on the documents, provide a concise answer in 100-200 words"
    elif length_pref == "long":
        format_instruction = "Based on the documents, provide a detailed answer in 400-600 words with specific examples from the content"
    else:
        format_instruction = "Based on the documents, provide a well-structured answer in 250-400 words"
    
    context_instruction = ""
    if context and len(st.session_state.chat_history) > 0:
        context_instruction = f"\nPrevious conversation context: {context}\n"
    
    try:
        if isinstance(vectorstore, list):
            relevant_text = " ".join(vectorstore[:3])
            prompt = f"""Based on the following document content, answer the question.
{context_instruction}
Document Content: {relevant_text}

Question: {question}

Instructions: {format_instruction}

Answer based on the document content considering the conversation context:"""
        else:
            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
            relevant_docs = retriever.get_relevant_documents(question)
            
            if relevant_docs:
                context_text = "\n".join([doc.page_content for doc in relevant_docs])
                prompt = f"""Based on the following document content, answer the question.
{context_instruction}
Document Content: {context_text}

Question: {question}

Instructions: {format_instruction}

Answer based on the document content considering the conversation context:"""
            else:
                return get_general_knowledge_answer(question, llm, length_pref, context)
        
        response = llm.invoke(prompt)
        return response.content.strip()
    
    except Exception as e:
        return get_general_knowledge_answer(question, llm, length_pref, context)


def get_hybrid_answer(question, vectorstore, llm, length_pref="medium"):
    """Smart hybrid approach with context memory"""
    session_id = st.session_state.current_session_id
    context = get_context_for_session(session_id, question)
    
    document_keywords = [
        'document', 'documents', 'uploaded', 'file', 'files', 'pdf', 'content',
        'text', 'summary', 'summarize', 'tell me about the', 'what is in',
        'according to', 'based on', 'from the document', 'in the file'
    ]
    
    is_document_query = any(keyword in question.lower() for keyword in document_keywords)
    
    if vectorstore and st.session_state.processed_docs and is_document_query:
        answer = get_document_based_answer(question, vectorstore, llm, length_pref, context)
        source = "documents"
    else:
        answer = get_general_knowledge_answer(question, llm, length_pref, context)
        source = "general_knowledge"
    
    # Update context memory
    update_context_memory(session_id, question, answer)
    
    return {"answer": answer, "source": source}


def handle_user_input(user_question):
    typing_placeholder = st.empty()
    typing_placeholder.markdown("""
    <div class="typing-indicator">
        <div class="typing-dots">
            <span></span><span></span><span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        if not st.session_state.llm:
            st.session_state.llm = initialize_llm()
        
        result = get_hybrid_answer(
            user_question, 
            st.session_state.vectorstore, 
            st.session_state.llm,
            st.session_state.length_preference
        )
        
        answer = result["answer"]
        source = result["source"]
        
        st.session_state.chat_history.extend([
            {"type": "user", "content": user_question},
            {"type": "bot", "content": answer, "source": source}
        ])
        
        # Save session after each interaction
        save_current_session()
        
        # Set flags for auto-scroll
        st.session_state.should_scroll = True
        st.session_state.new_message = True
        typing_placeholder.empty()
        
    except Exception as e:
        typing_placeholder.empty()
        st.error(f"Error generating response: {str(e)}")


def display_chat_history():
    """Display chat history with ChatGPT-like styling"""
    for i, message in enumerate(st.session_state.chat_history):
        if message["type"] == "user":
            st.markdown(f'<div class="chat-message user">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            source = message.get("source", "unknown")
            if not st.session_state.chatgpt_mode:
                source_emoji = "📄" if source == "documents" else "🧠"
                source_text = "From Documents" if source == "documents" else "General Knowledge"
                
                st.markdown(f'<div class="chat-message bot">{message["content"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="source-indicator">{source_emoji} {source_text}</div>', unsafe_allow_html=True)
            else:
                # ChatGPT-like mode - no source indicators
                st.markdown(f'<div class="chat-message bot chatgpt-style">{message["content"]}</div>', unsafe_allow_html=True)


def show_upload_modal():
    if st.session_state.show_upload:
        with st.container():
            st.markdown('<div class="upload-modal-overlay">', unsafe_allow_html=True)
            st.markdown('<div class="upload-modal">', unsafe_allow_html=True)
            
            st.markdown("### 📁 Upload Documents")
            
            col1, col2 = st.columns(2)
            
            with col1:
                pdf_docs = st.file_uploader("📄 PDF Files", accept_multiple_files=True, type="pdf", key="pdf_upload")
                docx_docs = st.file_uploader("📝 Word Files", accept_multiple_files=True, type="docx", key="docx_upload")
            
            with col2:
                eml_docs = st.file_uploader("📧 Email Files", accept_multiple_files=True, type="eml", key="eml_upload")
                web_input = st.text_area("🌐 Web URLs (one per line)", placeholder="https://example.com", height=60, key="web_upload")
                web_urls = [url.strip() for url in web_input.split('\n') if url.strip()] if web_input else []
            
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                if st.button("🚀 Process Documents", type="primary", key="process_docs"):
                    if pdf_docs or docx_docs or eml_docs or web_urls:
                        with st.spinner("📖 Processing documents..."):
                            text_chunks = process_documents(pdf_docs, docx_docs, eml_docs, web_urls)
                            
                            if text_chunks:
                                st.session_state.vectorstore = create_vectorstore(text_chunks)
                                st.session_state.llm = initialize_llm()
                                st.session_state.processed_docs = True
                                st.session_state.show_upload = False
                                save_current_session()
                                st.success(f"✅ Successfully processed {len(text_chunks)} text chunks!")
                                st.rerun()
                            else:
                                st.error("❌ No content could be extracted from the documents.")
                    else:
                        st.warning("⚠️ Please upload at least one document or enter a URL.")
            
            with col_btn2:
                if st.button("🔄 Reset", key="reset_upload"):
                    st.rerun()
            
            with col_btn3:
                if st.button("❌ Close", key="close_upload"):
                    st.session_state.show_upload = False
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)


def show_stats():
    if st.session_state.chat_history:
        total_messages = len(st.session_state.chat_history)
        user_messages = len([msg for msg in st.session_state.chat_history if msg["type"] == "user"])
        bot_messages = len([msg for msg in st.session_state.chat_history if msg["type"] == "bot"])
        doc_responses = len([msg for msg in st.session_state.chat_history if msg.get("source") == "documents"])
        general_responses = len([msg for msg in st.session_state.chat_history if msg.get("source") == "general_knowledge"])
        
        st.markdown('<div class="stats-container">', unsafe_allow_html=True)
        st.markdown('<div class="stats-item"><span>Questions:</span><span>{}</span></div>'.format(user_messages), unsafe_allow_html=True)
        st.markdown('<div class="stats-item"><span>Responses:</span><span>{}</span></div>'.format(bot_messages), unsafe_allow_html=True)
        st.markdown('<div class="stats-item"><span>Document-based:</span><span>{}</span></div>'.format(doc_responses), unsafe_allow_html=True)
        st.markdown('<div class="stats-item"><span>General Knowledge:</span><span>{}</span></div>'.format(general_responses), unsafe_allow_html=True)
        st.markdown('<div class="stats-item"><span>Documents Status:</span><span>{}</span></div>'.format("Ready" if st.session_state.processed_docs else "None"), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No conversation yet! Start chatting to see statistics.")


def sidebar_chat_sessions():
    """Display chat sessions in sidebar"""
    with st.sidebar:
        st.markdown('<div class="sidebar-header">💬 Chat Sessions</div>', unsafe_allow_html=True)
        
        # New Chat Button
        if st.button("➕ New Chat", key="new_chat_btn", help="Start a new chat session"):
            # Save current session before creating new one
            save_current_session()
            
            # Create new session
            new_session_id = session_manager.create_new_session()
            st.session_state.current_session_id = new_session_id
            st.session_state.chat_history = []
            st.session_state.processed_docs = False
            st.session_state.vectorstore = None
            st.session_state.sessions = session_manager.load_sessions()
            st.rerun()
        
        st.markdown("---")
        
        # Display existing sessions
        sessions = session_manager.load_sessions()
        
        if sessions:
            for session_id, session_data in sorted(sessions.items(), key=lambda x: x[1].get('last_updated', ''), reverse=True):
                session_name = session_data.get('name', 'Unnamed Chat')
                last_updated = session_data.get('last_updated', '')
                
                # Format last updated
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
                    time_str = dt.strftime('%m/%d %H:%M')
                except:
                    time_str = ''
                
                # Session container
                is_current = session_id == st.session_state.current_session_id
                
                with st.container():
                    if is_current:
                        st.markdown(f'<div class="session-item current-session">', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="session-item">', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        if st.button(f"💬 {session_name}", key=f"load_{session_id}", help=f"Load session - {time_str}"):
                            save_current_session()
                            load_session(session_id)
                            st.rerun()
                    
                    with col2:
                        if st.button("✏️", key=f"edit_{session_id}", help="Rename session"):
                            st.session_state[f"edit_mode_{session_id}"] = True
                            st.rerun()
                    
                    with col3:
                        if len(sessions) > 1:
                            if st.button("🗑️", key=f"delete_{session_id}", help="Delete session"):
                                session_manager.delete_session(session_id)
                                if session_id == st.session_state.current_session_id:
                                    remaining_sessions = session_manager.load_sessions()
                                    if remaining_sessions:
                                        new_current = list(remaining_sessions.keys())[0]
                                        load_session(new_current)
                                st.session_state.sessions = session_manager.load_sessions()
                                st.rerun()
                        else:
                            st.button("🔒", key=f"delete_disabled_{session_id}", 
                                    help="Cannot delete the last session", disabled=True)
                    
                    # Edit mode
                    if st.session_state.get(f"edit_mode_{session_id}", False):
                        new_name = st.text_input("New name:", value=session_name, key=f"rename_{session_id}")
                        col_save, col_cancel = st.columns(2)
                        
                        with col_save:
                            if st.button("💾", key=f"save_{session_id}"):
                                session_manager.rename_session(session_id, new_name)
                                st.session_state[f"edit_mode_{session_id}"] = False
                                st.session_state.sessions = session_manager.load_sessions()
                                st.rerun()
                        
                        with col_cancel:
                            if st.button("❌", key=f"cancel_{session_id}"):
                                st.session_state[f"edit_mode_{session_id}"] = False
                                st.rerun()
                    
                    st.markdown(f'<div class="session-time">{time_str}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No chat sessions yet. Create your first chat!")


def create_fixed_input():
    """Create the fixed input bar at the bottom of the window"""
    st.markdown("""
    <div class="window-bottom-input">
        <div class="input-bar-container">
    """, unsafe_allow_html=True)
    
    # Create columns for the input elements
    col1, col2, col3 = st.columns([0.06, 0.88, 0.06])
    
    with col1:
        upload_clicked = st.button("📄", key="upload_toggle_window", help="Upload", 
                                 use_container_width=True)
        if upload_clicked:
            st.session_state.show_upload = not st.session_state.show_upload
            st.rerun()
    
    with col2:
        placeholder_text = "Message ChatGPT Assistant..." if st.session_state.chatgpt_mode else "Ask me anything..."
        user_input = st.chat_input(placeholder_text, key="window_chat_input")
    
    with col3:
        voice_clicked = st.button("🎤", key="voice_input_window", help="Voice", 
                                use_container_width=True)
        if voice_clicked:
            try:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    st.info("🎤 Listening...")
                    audio = r.listen(source, timeout=5)
                user_question = r.recognize_google(audio)
                st.success(f"✅ You said: '{user_question}'")
                handle_user_input(user_question)
                st.rerun()
            except:
                st.error("❌ Could not understand audio. Please try again.")
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    return user_input


def main():
    init_session_state()
    
    # Sidebar for chat sessions
    sidebar_chat_sessions()
    
    # Header
    header_title = "🤖 ChatGPT-like AI Assistant" if st.session_state.chatgpt_mode else "🤖 AI Chat Assistant"
    header_desc = "ChatGPT-like experience • Smart responses • Context aware" if st.session_state.chatgpt_mode else "Smart document chat • Voice enabled • Context memory"
    
    st.markdown(f"""
    <div class="main-header">
        <h1>{header_title}</h1>
        <p>{header_desc}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show current session info
    if st.session_state.current_session_id:
        session_name = st.session_state.sessions.get(st.session_state.current_session_id, {}).get('name', 'Current Chat')
        st.markdown(f'<div class="current-session-indicator">📝 {session_name}</div>', unsafe_allow_html=True)
    
    # Main layout
    col1, col2 = st.columns([2.8, 1.2])
    
    with col1:
        # Main content area with scrollable chat
        st.markdown('<div class="scrollable-content-area">', unsafe_allow_html=True)
        
        # Status (hidden in ChatGPT mode)
        if not st.session_state.chatgpt_mode:
            if st.session_state.processed_docs:
                st.markdown('<div class="status-indicator status-ready">✅ Documents ready</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-indicator status-waiting">🧠 General knowledge mode</div>', unsafe_allow_html=True)
        
        # Show upload modal
        show_upload_modal()
        
        # Display chat history in scrollable container
        st.markdown('<div class="scrollable-chat-container">', unsafe_allow_html=True)
        display_chat_history()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Handle input
        user_question = create_fixed_input()
        if user_question:
            handle_user_input(user_question)
            st.rerun()
        
        # Auto-scroll when new message is added
        if st.session_state.should_scroll or st.session_state.new_message:
            add_auto_scroll()
            st.session_state.should_scroll = False
            st.session_state.new_message = False
    
    with col2:
        # Compact right panel
        st.markdown('<div class="compact-right-panel">', unsafe_allow_html=True)
        
        # ChatGPT Mode Toggle
        st.markdown('<div class="compact-section">', unsafe_allow_html=True)
        st.markdown('<div class="compact-title">🎯 Mode</div>', unsafe_allow_html=True)
        
        mode_text = "ChatGPT Mode: ON" if st.session_state.chatgpt_mode else "ChatGPT Mode: OFF"
        mode_color = "success" if st.session_state.chatgpt_mode else "secondary"
        
        if st.button(f"🔄 {mode_text}", key="toggle_chatgpt_mode", 
                    help="Toggle ChatGPT-like conversational mode"):
            st.session_state.chatgpt_mode = not st.session_state.chatgpt_mode
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Response Length Section
        st.markdown('<div class="compact-section">', unsafe_allow_html=True)
        st.markdown('<div class="compact-title">📏 Length</div>', unsafe_allow_html=True)
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            btn_style = "primary" if st.session_state.length_preference == "short" else "secondary"
            if st.button("S", key="length_short", help="Short responses", type=btn_style):
                st.session_state.length_preference = "short"
                st.rerun()
        with col_b:
            btn_style = "primary" if st.session_state.length_preference == "medium" else "secondary"
            if st.button("M", key="length_medium", help="Medium responses", type=btn_style):
                st.session_state.length_preference = "medium"
                st.rerun()
        with col_c:
            btn_style = "primary" if st.session_state.length_preference == "long" else "secondary"
            if st.button("L", key="length_long", help="Long responses", type=btn_style):
                st.session_state.length_preference = "long"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Actions Section
        st.markdown('<div class="compact-section">', unsafe_allow_html=True)
        st.markdown('<div class="compact-title">⚡ Actions</div>', unsafe_allow_html=True)
        
        if not st.session_state.chatgpt_mode:
            if st.button("📋 Summary", key="quick_summary", help="Summarize documents"):
                if st.session_state.processed_docs:
                    handle_user_input("Please provide a comprehensive summary of all the uploaded documents")
                    st.rerun()
                else:
                    st.warning("⚠️ Upload documents first")
        
        if st.button("🗑️ Clear", key="clear_chat", help="Clear current chat"):
            st.session_state.chat_history = []
            if st.session_state.current_session_id in st.session_state.context_memory:
                st.session_state.context_memory[st.session_state.current_session_id] = []
            save_current_session()
            st.rerun()
        
        if st.button("🔊 Read", key="text_to_speech", help="Read last response"):
            if st.session_state.chat_history:
                last_bot = [msg for msg in st.session_state.chat_history if msg["type"] == "bot"]
                if last_bot:
                    try:
                        engine = pyttsx3.init()
                        engine.say(last_bot[-1]["content"])
                        engine.runAndWait()
                    except:
                        st.error("❌ TTS unavailable")
            else:
                st.warning("⚠️ No chat history")
        
        if not st.session_state.chatgpt_mode:
            if st.button("📊 Stats", key="toggle_stats", help="Toggle statistics"):
                st.session_state.show_stats = not st.session_state.show_stats
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Stats Section (hidden in ChatGPT mode)
        if st.session_state.show_stats and not st.session_state.chatgpt_mode:
            st.markdown('<div class="compact-section">', unsafe_allow_html=True)
            st.markdown('<div class="compact-title">📈 Stats</div>', unsafe_allow_html=True)
            show_stats()
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == '__main__':
    main()
