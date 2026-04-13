import os
import time
import tempfile
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = "us-east-1"
PINECONE_INDEX_NAME = "medicalindex"

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

#  Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
spec = ServerlessSpec(cloud="aws", region=PINECONE_ENV)

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

async def load_vectorstore(uploaded_files):
    embed_model = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    file_paths = []


    for file in uploaded_files:
        contents = await file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        file_paths.append(tmp_path)

    #  Process PDFs
    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(documents)

        texts = [chunk.page_content for chunk in chunks]
        metadatas = [
            {**chunk.metadata, "text": chunk.page_content}  # Add text content to metadata
            for chunk in chunks
        ]
        ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]

        print(f"🔍 Embedding {len(texts)} chunks...")
        embeddings = embed_model.embed_documents(texts)

        print("📤 Uploading to Pinecone...")
        # Format vectors for Pinecone: [(id, embedding, metadata), ...]
        vectors_to_upsert = [
            (id_, emb, meta) 
            for id_, emb, meta in zip(ids, embeddings, metadatas)
        ]
        
        with tqdm(total=len(embeddings), desc="Upserting to Pinecone") as progress:
            index.upsert(vectors=vectors_to_upsert)
            progress.update(len(embeddings))

        print(f"✅ Upload complete for {file_path}")

        # 🧹 Cleanup temp file
        os.remove(file_path)

