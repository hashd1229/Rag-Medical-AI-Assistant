import streamlit as st
from datetime import datetime

def render_history_download():
    if st.session_state.get("messages") and len(st.session_state.messages) > 0:
        # Format chat history with better structure
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        chat_lines = [f"Medical AI Chat History - {timestamp}", "=" * 50, ""]
        
        for msg in st.session_state.messages:
            role = msg['role'].upper()
            content = msg['content']
            chat_lines.append(f"[{role}]:")
            chat_lines.append(content)
            chat_lines.append("-" * 30)
            chat_lines.append("")
        
        chat_text = "\n".join(chat_lines)
        
        st.download_button(
            label="📥 Download Chat History",
            data=chat_text,
            file_name=f"medical_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
            help="Download your conversation as a text file"
        )
    else:
        st.info("💬 Start a conversation to enable download", icon="ℹ️")