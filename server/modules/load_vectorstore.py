# import os
# import time
# from pathlib import Path
# from dotenv import load_dotenv
# from tqdm.auto import tqdm
# from pinecone import Pinecone, ServerlessSpec
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
# from langchain_google_genai import GoogleGenerativeAIEmbeddings


# load_dotenv()

# GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
# PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
# PINECONE_ENV="us-east-1"
# PINECONE_INDEX_NAME="medicalindex"

# os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY

# UPLOAD_DIR="./uploaded_docs"
# os.makedirs(UPLOAD_DIR,exist_ok=True)


# # initialize pinecone instance
# pc=Pinecone(api_key=PINECONE_API_KEY)
# spec=ServerlessSpec(cloud="aws",region=PINECONE_ENV)
# existing_indexes=[i["name"] for i in pc.list_indexes()]


# if PINECONE_INDEX_NAME not in existing_indexes:
#     pc.create_index(
#         name=PINECONE_INDEX_NAME,
#         dimension=768,
#         metric="dotproduct",
#         spec=spec
#     )
#     while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
#         time.sleep(1)


# index=pc.Index(PINECONE_INDEX_NAME)

# # load,split,embed and upsert pdf docs content

# def load_vectorstore(uploaded_files):
#     embed_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
#     file_paths = []

#     for file in uploaded_files:
#         save_path = Path(UPLOAD_DIR) / file.filename
#         with open(save_path, "wb") as f:
#             f.write(file.file.read())
#         file_paths.append(str(save_path))

#     for file_path in file_paths:
#         loader = PyPDFLoader(file_path)
#         documents = loader.load()

#         splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#         chunks = splitter.split_documents(documents)

#         texts = [chunk.page_content for chunk in chunks]
#         metadatas = [chunk.metadata for chunk in chunks]
#         ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]

#         print(f"🔍 Embedding {len(texts)} chunks...")
#         embeddings = embed_model.embed_documents(texts)

#         print("📤 Uploading to Pinecone...")
#         with tqdm(total=len(embeddings), desc="Upserting to Pinecone") as progress:
#             index.upsert(vectors=zip(ids, embeddings, metadatas))
#             progress.update(len(embeddings))

#         print(f"✅ Upload complete for {file_path}")

# server/modules/load_vectorstore.py
import os
import time
from io import BytesIO
from dotenv import load_dotenv
from tqdm.auto import tqdm
import pypdf
from pinecone import Pinecone, ServerlessSpec
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

# Get environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "medicalindex")

# Set Google API key
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Initialize Pinecone instance
pc = Pinecone(api_key=PINECONE_API_KEY)
spec = ServerlessSpec(cloud="aws", region=PINECONE_ENV)

# Check and create index if needed
existing_indexes = [i["name"] for i in pc.list_indexes()]

if PINECONE_INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=768,
        metric="dotproduct",
        spec=spec
    )
    while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
        time.sleep(1)

index = pc.Index(PINECONE_INDEX_NAME)

# Initialize embedding model once
embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


def load_vectorstore(uploaded_files):
    """
    Process PDFs in memory and upload to Pinecone - NO DISK WRITING!
    """
    all_texts = []
    all_metadatas = []
    all_ids = []
    
    for file in uploaded_files:
        # Read PDF into memory (no disk writing!)
        contents = file.file.read()
        pdf_file = BytesIO(contents)
        
        # Extract text using pypdf
        pdf_reader = pypdf.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        
        if not text.strip():
            print(f"⚠️ No text extracted from {file.filename}")
            continue
        
        # Split into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        
        # Create document-like chunks
        chunks = splitter.create_documents([text])
        
        # Prepare data for Pinecone
        file_texts = [chunk.page_content for chunk in chunks]
        file_metadatas = [{"source": file.filename, "chunk": i} for i in range(len(chunks))]
        file_ids = [f"{file.filename.replace('.pdf', '')}-{i}" for i in range(len(chunks))]
        
        all_texts.extend(file_texts)
        all_metadatas.extend(file_metadatas)
        all_ids.extend(file_ids)
    
    if not all_texts:
        raise Exception("No text could be extracted from the uploaded PDFs")
    
    print(f"🔍 Embedding {len(all_texts)} chunks...")
    embeddings = embed_model.embed_documents(all_texts)
    
    print("📤 Uploading to Pinecone...")
    vectors = list(zip(all_ids, embeddings, all_metadatas))
    
    with tqdm(total=len(vectors), desc="Upserting to Pinecone") as progress:
        # Upsert in batches of 100 for better performance
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            index.upsert(vectors=batch)
            progress.update(len(batch))
    
    print(f"✅ Upload complete! {len(all_texts)} chunks added to Pinecone")
    return len(all_texts)


# For backward compatibility with existing code
def process_pdfs_in_memory(uploaded_files):
    """Alias for load_vectorstore"""
    return load_vectorstore(uploaded_files)