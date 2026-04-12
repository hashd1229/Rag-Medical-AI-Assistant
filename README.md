# 🩺 Medical AI Assistant - RAG Chatbot

A sophisticated **Retrieval Augmented Generation (RAG)** chatbot powered by AI that specializes in medical document analysis and intelligent Q&A. This application combines modern NLP with vector databases to provide accurate medical information retrieval.

## ✨ Features

- 📄 **PDF Document Upload**: Upload and process medical PDFs with ease
- 💬 **Intelligent Chat Interface**: Ask questions about your medical documents
- 🧠 **RAG Technology**: Retrieval Augmented Generation for accurate answers
- 📊 **Semantic Search**: Find relevant information using vector embeddings
- 💾 **Chat History**: Download conversation history as text files
- ⚡ **Fast Processing**: Optimized document indexing and retrieval

## 🏗️ Architecture

```
┌─────────────────┐
│   Streamlit UI  │ (Frontend - Client)
│  - ChatUI       │
│  - Upload       │
│  - History      │
└────────┬────────┘
         │ HTTP
         ▼
┌──────────────────────────────┐
│  FastAPI Server              │ (Backend)
│  - Groq (Llama 3.3 70B)      │
│  - Google Embeddings         │
│  - Pinecone Vector DB        │
│  - PDF Processing            │
│  - Query Handlers            │
└──────────────────────────────┘
         │
         ▼
┌──────────────────────┐
│  Pinecone Vector DB  │
│  (medicalindex)      │
└──────────────────────┘
```

## 📁 Project Structure

```
RAG Medical AI Assistant/
├── client/                      # Streamlit Frontend
│   ├── app.py                   # Main application entry
│   ├── config.py                # Client configuration
│   ├── requirements.txt          # Client dependencies
│   ├── components/
│   │   ├── chatUI.py            # Chat interface
│   │   ├── upload.py            # PDF upload component
│   │   └── history_download.py  # Chat history download
│   └── utils/
│       └── api.py               # API client functions
│
├── server/                      # FastAPI Backend
│   ├── main.py                  # Server entry point
│   ├── logger.py                # Logging configuration
│   ├── requirements.txt          # Server dependencies
│   ├── test.py                  # Tests
│   ├── middlewares/
│   │   └── exception_handlers.py # Error handling
│   ├── modules/
│   │   ├── llm.py               # LLM integration
│   │   ├── load_vectorstore.py  # Vector DB management
│   │   ├── pdf_handlers.py      # PDF processing
│   │   └── query_handlers.py    # Query processing
│   ├── routes/
│   │   ├── ask_question.py      # Q&A endpoint
│   │   └── upload_pdfs.py       # Upload endpoint
│   └── uploaded_docs/           # Uploaded PDF storage
│
├── .gitignore                   # Git ignore rules
├── .env.example                 # Environment variables template
├── pyproject.toml               # Project metadata
├── main.py                      # Root entry point
└── README.md                    # This file
```

## 🎯 Usage Guide

### 1. Upload Medical Documents

1. Open the Streamlit application
2. Click on **📄 Upload PDFs** in the sidebar
3. Select one or more medical PDF files
4. Click **📤 Upload to Database** button
5. Wait for processing confirmation

### 2. Ask Questions

1. Type your medical question in the chat input
2. The AI will search relevant documents and provide an answer
3. View the response with source information

### 3. Download Chat History

1. Have an active conversation
2. Click **📥 Download Chat History** button
3. A text file with your conversation will be downloaded

## 📦 Dependencies

### Client
- **streamlit** - Web UI framework
- **requests** - HTTP client
- **python-dotenv** - Environment variables

### Server
- **fastapi** - Web framework
- **uvicorn[standard]** - ASGI server with standard extras
- **langchain** - LLM orchestration
- **langchain-community** - Community integrations
- **langchain-core** - Core LangChain utilities
- **langchain-groq** - Groq LLM integration
- **langchain-google-genai** - Google Generative AI embeddings
- **pinecone** - Pinecone vector database client
- **pypdf** - PDF document parsing
- **python-dotenv** - Environment variable management
- **python-multipart** - File upload support
- **pydantic** - Data validation
- **tqdm** - Progress bars
- **loguru** - Advanced logging

## 🔐 Security Considerations

- ✅ API keys stored in `.env` (never commit to git)
- ✅ PDF documents stored locally with proper cleanup
- ✅ Input validation on all endpoints
- ✅ Error handling without exposing sensitive info
- ✅ CORS configured for frontend communication


**Last Updated**: April 2026  
**Status**: Active Development 🚀
