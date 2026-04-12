# import os
# import shutil
# from fastapi import UploadFile
# import tempfile

# UPLOAD_DIR="./uploaded_docs"

# def save_uploaded_files(files:list[UploadFile])-> list[str]:
#     os.makedirs(UPLOAD_DIR,exist_ok=True)
#     file_path=[]
#     for file in files:
#         temp_path=os.path.join(UPLOAD_DIR,file.filename)
#         with open(temp_path,"wb") as f:
#             shutil.copyfileobj(file.file,f)
#         file_path.append(temp_path)
#     return file_path

import os
from fastapi import UploadFile
from io import BytesIO
import pypdf

def process_uploaded_files(files: list[UploadFile]) -> list[str]:
    """
    Process PDF files in memory - NO DISK WRITING
    Returns list of extracted text from each PDF
    """
    all_texts = []
    
    for file in files:
        # Read file into memory
        contents = file.file.read()
        pdf_file = BytesIO(contents)
        
        # Extract text from PDF
        pdf_reader = pypdf.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        
        all_texts.append(text)
    
    return all_texts


# Optional: Keep this for backward compatibility but make it memory-only
def save_uploaded_files(files: list[UploadFile]) -> list[str]:
    """
    DEPRECATED: Now processes in memory instead of saving to disk
    Returns list of text content instead of file paths
    """
    return process_uploaded_files(files)