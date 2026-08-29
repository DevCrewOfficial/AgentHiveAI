"""
Minimal Streamlit demo shell. Run with:  streamlit run app.py

This gives you a working chat UI immediately so on hackathon day you only
need to focus on the agent logic, not the frontend.
"""

import streamlit as st
from agent.core import run_agent

st.set_page_config(page_title="Hackathon Agent", page_icon="🤖", layout="centered")

st.title("🤖 Hackathon Agent")
st.caption("Swap in your problem statement in agent/core.py -> SYSTEM_PROMPT")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask the agent something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = run_agent(user_input, verbose=True)
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

with st.sidebar:
    st.header("Debug")
    st.write("Tool calls and reasoning print to your terminal (where you ran `streamlit run app.py`).")
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()
