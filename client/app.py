import streamlit as st
from components.upload import render_uploader
from components.history_download import render_history_download
from components.chatUI import render_chat

# Page Configuration
st.set_page_config(
    page_title="AI Medical Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# Custom CSS Styling with Background and Glassmorphism
st.markdown("""
    <style>
    /* Background */
    [data-testid="stAppViewContainer"] > .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-attachment: fixed;
        min-height: 100vh;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: rgba(255, 255, 255, 0.05);
        background-attachment: fixed;
    }
    
    /* Main container styling */
    .main {
        padding-top: 0rem;
    }
    
    /* Header styling */
    .header-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .header-container:hover {
        background: rgba(255, 255, 255, 0.2);
        box-shadow: 0 12px 48px 0 rgba(102, 126, 234, 0.4);
    }
    
    .header-container h1 {
        margin: 0;
        font-size: 2.8rem;
        font-weight: 800;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    
    .header-container p {
        margin: 0.8rem 0 0 0;
        font-size: 1.15rem;
        opacity: 0.95;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    /* Chat container */
    .chat-container {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.25);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        transition: all 0.3s ease;
    }
    
    .chat-container:hover {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.35);
        box-shadow: 0 12px 48px 0 rgba(31, 38, 135, 0.3);
    }
    
    /* Heading styling */
    h3 {
        color: white !important;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        font-weight: 700;
    }
    
    /* Info boxes */
    .stInfo, [data-baseweb="notification"] {
        background: rgba(100, 200, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(100, 200, 255, 0.3) !important;
        border-radius: 15px !important;
        color: white !important;
    }
    
    .stError, [data-icon="error"] {
        background: rgba(255, 100, 100, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 100, 100, 0.3) !important;
        border-radius: 15px !important;
    }
    
    .stSuccess {
        background: rgba(100, 255, 150, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(100, 255, 150, 0.3) !important;
        border-radius: 15px !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.8), rgba(118, 75, 162, 0.8));
        backdrop-filter: blur(10px);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 12px;
        padding: 0.7rem 1.8rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        background: linear-gradient(135deg, rgba(102, 126, 234, 1), rgba(118, 75, 162, 1));
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, rgba(240, 147, 251, 0.8), rgba(245, 87, 108, 0.8));
        backdrop-filter: blur(10px);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 12px;
        padding: 0.7rem 1.8rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
        letter-spacing: 0.5px;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-3px);
        background: linear-gradient(135deg, rgba(240, 147, 251, 1), rgba(245, 87, 108, 1));
        box-shadow: 0 8px 25px rgba(245, 87, 108, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stChatInput > div > div > input {
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 500;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stChatInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    /* File uploader */
    .stFileUploader > div > div {
        background: rgba(255, 255, 255, 0.12) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px dashed rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.15) !important;
    }
    
    /* Typography */
    body {
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-container">
        <h1>🩺 Medical Assistant Chatbot</h1>
        <p>✨ Intelligent AI-powered medical document analysis and Q&A</p>
    </div>
""", unsafe_allow_html=True)

# Main layout with columns
col1, col2 = st.columns([3, 1])

with col1:
    render_chat()

with col2:
    st.markdown("### 📋 Actions")
    render_history_download()

# Sidebar content
with st.sidebar:
    st.markdown("### 📂 Document Management")
    st.markdown("---")
    render_uploader()
    st.markdown("---")
    
    # Info section
    with st.expander("ℹ️ How to use", expanded=False):
        st.markdown("""
        1. **Upload Documents**: Upload your medical PDFs using the file uploader
        2. **Ask Questions**: Type your medical questions in the chat
        3. **Get Answers**: The AI will analyze documents and provide responses
        4. **Download History**: Save your conversation as a text file
        """)