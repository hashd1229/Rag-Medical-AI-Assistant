# from fastapi import APIRouter, UploadFile, File
# from typing import List
# from modules.load_vectorstore import load_vectorstore
# from fastapi.responses import JSONResponse
# from logger import logger


# router=APIRouter()

# @router.post("/upload_pdfs/")
# async def upload_pdfs(files:List[UploadFile] = File(...)):
#     try:
#         logger.info("Recieved uploaded files")
#         load_vectorstore(files)
#         logger.info("Document added to vectorstore")
#         return {"messages":"Files processed and vectorstore updated"}
#     except Exception as e:
#         logger.exception("Error during PDF upload")
#         return JSONResponse(status_code=500,content={"error":str(e)})
    

from fastapi import APIRouter, UploadFile, File, HTTPException
from io import BytesIO
import pypdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
import pinecone
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Initialize Pinecone (v5 style)
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "medical-assistant")

# Check if API key exists
if not PINECONE_API_KEY:
    raise Exception("PINECONE_API_KEY environment variable not set")

# Initialize Pinecone client
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)

# Initialize embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv("GOOGLE_API_KEY"))

@router.post("/upload")
async def upload_pdfs(files: list[UploadFile] = File(...)):
    """
    Upload PDFs and add to vector store - NO DISK WRITING
    Processes entirely in memory for Leapcell compatibility
    """
    try:
        all_texts = []
        all_metadatas = []
        
        for file in files:
            # Read PDF into memory (no disk writing!)
            contents = await file.read()
            pdf_file = BytesIO(contents)
            
            # Extract text from PDF using pypdf
            pdf_reader = pypdf.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            
            if not text.strip():
                continue
            
            # Split into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
            )
            chunks = text_splitter.split_text(text)
            
            # Add to collections with metadata
            for i, chunk in enumerate(chunks):
                all_texts.append(chunk)
                all_metadatas.append({
                    "source": file.filename,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                })
        
        if not all_texts:
            raise HTTPException(
                status_code=400, 
                detail="No text could be extracted from the uploaded PDFs"
            )
        
        # Create index if it doesn't exist
        existing_indexes = [index.name for index in pc.list_indexes()]
        
        if PINECONE_INDEX_NAME not in existing_indexes:
            pc.create_index(
                name=PINECONE_INDEX_NAME,
                dimension=1536,  # OpenAI embeddings dimension
                metric="cosine",
                spec=pinecone.ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
        
        # Add to Pinecone vector store
        vector_store = PineconeVectorStore.from_texts(
            texts=all_texts,
            embedding=embeddings,
            index_name=PINECONE_INDEX_NAME,
            metadatas=all_metadatas
        )
        
        return {
            "message": f"Successfully processed {len(files)} file(s)",
            "chunks_created": len(all_texts),
            "files_processed": len(files)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))