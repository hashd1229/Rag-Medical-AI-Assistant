import streamlit as st
from utils.api import ask_question


def render_chat():
    st.markdown("### 💬 Chat with your assistant")

    if "messages" not in st.session_state:
        st.session_state.messages=[]

    # render existing chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message(msg["role"], avatar="👤"):
                st.markdown(msg["content"])
        else:
            with st.chat_message(msg["role"], avatar="🤖"):
                st.markdown(msg["content"])

    # input and response
    user_input=st.chat_input("Type your medical question here...")
    if user_input:
        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        st.session_state.messages.append({"role":"user","content":user_input})

        # Get and display assistant response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🔍 Analyzing documents..."):
                response=ask_question(user_input)
                if response.status_code==200:
                    data=response.json()
                    answer=data["response"]
                    sources=data.get("sources",[])
                    st.markdown(answer)
                    
                    # Display sources if available (commented functionality)
                    # if sources:
                    #     st.markdown("---")
                    #     st.markdown("📚 **Sources:**")
                    #     for src in sources:
                    #         st.markdown(f"- `{src}`")
                    
                    st.session_state.messages.append({"role":"assistant","content":answer})
                else:
                    st.error(f"❌ Error: {response.text}")