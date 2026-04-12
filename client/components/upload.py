import streamlit as st
from utils.api import upload_pdfs_api


def render_uploader():
    st.markdown('<h3 style="color: white; text-shadow: 0 2px 8px rgba(0,0,0,0.2);">📄 Upload PDFs</h3>', unsafe_allow_html=True)
    uploaded_files=st.file_uploader(
        label="Select your medical PDF documents",
        type="pdf",
        accept_multiple_files=True,
        help="Upload one or more PDF files to build your knowledge base"
    )
    
    if uploaded_files:
        st.info(f"✅ {len(uploaded_files)} file(s) selected", icon="ℹ️")
        
        if st.button("📤 Upload to Database", use_container_width=True):
            with st.spinner("⏳ Uploading and processing documents..."):
                response=upload_pdfs_api(uploaded_files)
                if response.status_code==200:
                    st.success("✅ Documents uploaded successfully!", icon="✅")
                else:
                    st.error(f"❌ Error: {response.text}", icon="❌")
    else:
        st.info("No PDFs selected yet. Upload medical documents to get started.", icon="ℹ️")