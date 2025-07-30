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
from htmltemplates import css

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Page configuration
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS
st.markdown(css, unsafe_allow_html=True)

# Add auto-scroll JavaScript function
def add_auto_scroll():
    """Inject JavaScript to auto-scroll to bottom"""
    st.markdown("""
    <script>
    function scrollToBottom() {
        // Scroll to the bottom of the page
        window.scrollTo({
            top: document.body.scrollHeight,
            behavior: 'smooth'
        });
        
        // Alternative method for better compatibility
        document.documentElement.scrollTop = document.documentElement.scrollHeight;
    }
    
    // Execute scroll after content loads
    setTimeout(function() {
        scrollToBottom();
    }, 100);
    </script>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    defaults = {
        "conversation": None,
        "chat_history": [],
        "processed_docs": False,
        "is_processing": False,
        "vectorstore": None,
        "llm": None,
        "show_upload": False,
        "length_preference": "medium",
        "show_stats": False,
        "should_scroll": False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

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

def get_general_knowledge_answer(question, llm, length_pref="medium"):
    """Get general knowledge answer from LLM"""
    # Determine format based on length preference
    if length_pref == "short":
        format_instruction = "Provide a concise, helpful answer in 100-200 words with clear bullet points"
    elif length_pref == "long":
        format_instruction = "Provide a detailed, comprehensive answer in 400-600 words with examples, explanations, and thorough coverage"
    else:
        format_instruction = "Provide a well-structured, informative answer in 250-400 words with good detail and examples"
    
    prompt = f"""You are a helpful AI assistant. Answer the following question using your general knowledge.

Question: {question}

Instructions: {format_instruction}

Please provide a helpful, accurate, and well-formatted response:"""
    
    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        return f"I apologize, but I encountered an error while processing your question: {str(e)}"

def get_document_based_answer(question, vectorstore, llm, length_pref="medium"):
    """Get document-based answer using vectorstore"""
    # Determine format based on length preference
    if length_pref == "short":
        format_instruction = "Based on the documents, provide a concise answer in 100-200 words"
    elif length_pref == "long":
        format_instruction = "Based on the documents, provide a detailed answer in 400-600 words with specific examples from the content"
    else:
        format_instruction = "Based on the documents, provide a well-structured answer in 250-400 words"
    
    try:
        if isinstance(vectorstore, list):
            # Simple text matching fallback
            relevant_text = " ".join(vectorstore[:3])
            prompt = f"""Based on the following document content, answer the question.

Document Content: {relevant_text}

Question: {question}

Instructions: {format_instruction}

Answer based on the document content:"""
        else:
            # Use vectorstore retrieval
            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
            relevant_docs = retriever.get_relevant_documents(question)
            
            if relevant_docs:
                context = "\n".join([doc.page_content for doc in relevant_docs])
                prompt = f"""Based on the following document content, answer the question.

Document Content: {context}

Question: {question}

Instructions: {format_instruction}

Answer based on the document content:"""
            else:
                # No relevant documents found, fall back to general knowledge
                return get_general_knowledge_answer(question, llm, length_pref)
        
        response = llm.invoke(prompt)
        return response.content.strip()
    
    except Exception as e:
        # Fall back to general knowledge on any error
        return get_general_knowledge_answer(question, llm, length_pref)

def get_hybrid_answer(question, vectorstore, llm, length_pref="medium"):
    """Smart hybrid approach - determines whether to use documents or general knowledge"""
    
    # Keywords that suggest document-related queries
    document_keywords = [
        'document', 'documents', 'uploaded', 'file', 'files', 'pdf', 'content',
        'text', 'summary', 'summarize', 'tell me about the', 'what is in',
        'according to', 'based on', 'from the document', 'in the file'
    ]
    
    # Check if question is document-related and we have documents
    is_document_query = any(keyword in question.lower() for keyword in document_keywords)
    
    if vectorstore and st.session_state.processed_docs and is_document_query:
        # Try document-based answer first
        answer = get_document_based_answer(question, vectorstore, llm, length_pref)
        return {"answer": answer, "source": "documents"}
    else:
        # Use general knowledge
        answer = get_general_knowledge_answer(question, llm, length_pref)
        return {"answer": answer, "source": "general_knowledge"}

def handle_user_input(user_question):
    # Show typing indicator
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
        
        # Use hybrid approach for better answers
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
        
        # Set scroll flag to trigger auto-scroll
        st.session_state.should_scroll = True
        
        typing_placeholder.empty()
        
    except Exception as e:
        typing_placeholder.empty()
        st.error(f"Error generating response: {str(e)}")

def display_chat_history():
    for message in st.session_state.chat_history:
        if message["type"] == "user":
            st.markdown(f'<div class="chat-message user">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            # Show source indicator
            source = message.get("source", "unknown")
            source_emoji = "📄" if source == "documents" else "🧠"
            source_text = "From Documents" if source == "documents" else "General Knowledge"
            
            st.markdown(f'<div class="chat-message bot">{message["content"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align: left; margin-left: 0; font-size: 0.8rem; color: #667eea; margin-top: -0.5rem; margin-bottom: 1rem;">{source_emoji} {source_text}</div>', unsafe_allow_html=True)
    
    # Add scroll anchor at the bottom
    st.markdown('<div id="bottom-anchor"></div>', unsafe_allow_html=True)

def show_upload_modal():
    if st.session_state.show_upload:
        # Fixed: Using a proper container without overlay issues
        with st.container():
            st.markdown('<div class="upload-modal-container">', unsafe_allow_html=True)
            st.markdown('<div class="upload-modal">', unsafe_allow_html=True)
            
            st.markdown("### 📁 Upload Documents")
            
            # Create two columns for file uploads
            col1, col2 = st.columns(2)
            
            with col1:
                pdf_docs = st.file_uploader("📄 PDF Files", accept_multiple_files=True, type="pdf", key="pdf_upload")
                docx_docs = st.file_uploader("📝 Word Files", accept_multiple_files=True, type="docx", key="docx_upload")
            
            with col2:
                eml_docs = st.file_uploader("📧 Email Files", accept_multiple_files=True, type="eml", key="eml_upload")
                web_input = st.text_area("🌐 Web URLs (one per line)", placeholder="https://example.com", height=60, key="web_upload")
                web_urls = [url.strip() for url in web_input.split('\n') if url.strip()] if web_input else []
            
            # Action buttons
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
                                st.success(f"✅ Successfully processed {len(text_chunks)} text chunks!")
                                st.rerun()
                            else:
                                st.error("❌ No content could be extracted from the documents.")
                    else:
                        st.warning("⚠️ Please upload at least one document or enter a URL.")
            
            with col_btn2:
                if st.button("🔄 Reset", key="reset_upload"):
                    # Clear all file uploaders by rerunning
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

def main():
    init_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Chat Assistant</h1>
        <p>Beautiful interface • Smart document chat • Voice enabled • General knowledge</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main layout
    col1, col2 = st.columns([2.5, 1])
    
    with col1:
        # Search container with small plus button
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        
        col_plus, col_input, col_voice = st.columns([0.4, 8, 1])
        
        with col_plus:
            if st.button("➕", key="upload_toggle", help="Upload Documents"):
                st.session_state.show_upload = not st.session_state.show_upload
                st.rerun()
        
        with col_input:
            user_question = st.chat_input("Ask me anything - documents or general questions...")
        
        with col_voice:
            if st.button("🎤", key="voice_input", help="Voice Input"):
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
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show upload modal right after search container
        show_upload_modal()
        
        # Status
        if st.session_state.processed_docs:
            st.markdown('<div class="status-indicator status-ready">✅ Documents ready! Can answer both document and general questions</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-indicator status-waiting">🧠 General knowledge mode active - Ready to answer any questions!</div>', unsafe_allow_html=True)
        
        # Handle input
        if user_question:
            handle_user_input(user_question)
            st.rerun()
        
        # Display chat
        display_chat_history()
        
        # Auto-scroll to bottom when new message is added
        if st.session_state.should_scroll:
            add_auto_scroll()
            st.session_state.should_scroll = False
    
    with col2:
        # Right panel with all controls
        st.markdown('<div class="right-panel">', unsafe_allow_html=True)
        
        # Response Length Section
        st.markdown('<div class="panel-section">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">📏 Response Length</div>', unsafe_allow_html=True)
        
        length_options = ["short", "medium", "long"]
        for length in length_options:
            if st.button(length.title(), key=f"length_{length}", help=f"Set {length} responses"):
                st.session_state.length_preference = length
                st.success(f"✅ Set to {length} responses")
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Actions Section
        st.markdown('<div class="panel-section">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">⚡ Quick Actions</div>', unsafe_allow_html=True)
        
        if st.button("🌍 General Question", key="quick_general"):
            st.info("💡 Ask me anything! Science, history, technology, current events, etc.")
        
        if st.button("📋 Summarize Documents", key="quick_summary"):
            if st.session_state.processed_docs:
                handle_user_input("Please provide a comprehensive summary of all the uploaded documents")
                st.rerun()
            else:
                st.warning("⚠️ Please upload documents first using the ➕ button")
        
        if st.button("🔍 Explain Topic", key="quick_explain"):
            st.info("💡 Try asking: 'Explain artificial intelligence' or 'What is quantum computing?'")
        
        if st.button("📍 Scroll to Bottom", key="manual_scroll"):
            # Manual scroll trigger
            st.session_state.should_scroll = True
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat Controls Section
        st.markdown('<div class="panel-section">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">🎛️ Chat Controls</div>', unsafe_allow_html=True)
        
        if st.button("🗑️ Clear Chat History", key="clear_chat"):
            st.session_state.chat_history = []
            st.success("✅ Chat history cleared!")
            st.rerun()
        
        if st.button("🔊 Read Last Response", key="text_to_speech"):
            if st.session_state.chat_history:
                last_bot = [msg for msg in st.session_state.chat_history if msg["type"] == "bot"]
                if last_bot:
                    try:
                        engine = pyttsx3.init()
                        engine.say(last_bot[-1]["content"])
                        engine.runAndWait()
                    except:
                        st.error("❌ Text-to-speech not available")
                else:
                    st.warning("⚠️ No bot responses to read")
            else:
                st.warning("⚠️ No chat history available")
        
        if st.button("📊 Toggle Statistics", key="toggle_stats"):
            st.session_state.show_stats = not st.session_state.show_stats
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Stats Section
        if st.session_state.show_stats:
            st.markdown('<div class="panel-section">', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">📈 Chat Statistics</div>', unsafe_allow_html=True)
            show_stats()
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
