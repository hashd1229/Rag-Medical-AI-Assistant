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

from fastapi import UploadFile
from io import BytesIO
import pypdf

def process_uploaded_files(files: list[UploadFile]) -> list[str]:
    """
    Process PDF files in memory - NO DISK WRITING
    Returns list of extracted text from each PDF
    
    Args:
        files: List of uploaded PDF files
        
    Returns:
        List of extracted text strings for each PDF
    """
    all_texts = []
    
    for file in files:
        try:
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
            
        except Exception as e:
            print(f"Error processing {file.filename}: {str(e)}")
            all_texts.append("")  # Add empty string for failed PDFs
    
    return all_texts


def save_uploaded_files(files: list[UploadFile]) -> list[str]:
    """
    DEPRECATED: Now processes in memory instead of saving to disk
    Kept for backward compatibility - returns text content instead of file paths
    
    Args:
        files: List of uploaded PDF files
        
    Returns:
        List of extracted text strings (maintained for API compatibility)
    """
    return process_uploaded_files(files)


def extract_pdf_text(file_content: bytes) -> str:
    """
    Extract text from PDF bytes - pure memory operation
    
    Args:
        file_content: PDF file as bytes
        
    Returns:
        Extracted text as string
    """
    try:
        pdf_file = BytesIO(file_content)
        pdf_reader = pypdf.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        raise Exception(f"PDF extraction failed: {str(e)}")