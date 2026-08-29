"""
Shipment Support Agent - Streamlit UI

Run with:
    streamlit run app.py
"""

import streamlit as st
from agent.core import run_agent


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Shipment Support Agent",
    page_icon="📦",
    layout="centered"
)


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("📦 Shipment Support Agent")
st.caption("Tell us about your shipment issue and our agent will help resolve it.")


# --------------------------------------------------
# Session state
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# Shipment details
# --------------------------------------------------

st.subheader("Shipment Details")

shipment_id = st.text_input(
    "Shipment ID",
    placeholder="Example: SHIP001"
)


issue = st.selectbox(
    "Issue Faced",
    [
        "Damaged Package",
        "Failed Delivery",
        "Missing Documentation",
        "Bad Address",
        "Delayed Shipment"
    ]
)


problem = st.text_area(
    "Describe the Problem",
    placeholder="Example: My package arrived completely smashed and I want a replacement.",
    height=120
)


# --------------------------------------------------
# Submit button
# --------------------------------------------------

if st.button("Submit Issue", type="primary"):

    if not shipment_id:
        st.warning("Please enter your Shipment ID.")

    elif not problem:
        st.warning("Please describe the problem.")

    else:

        # Create a complete message for the agent
        user_message = f"""
Shipment ID: {shipment_id}

Issue Type: {issue}

Customer Problem:
{problem}
"""

        # Show user's request
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_message
            }
        )

        with st.chat_message("user"):
            st.markdown(user_message)

        # Run agent
        with st.chat_message("assistant"):

            with st.spinner("Agent is analyzing your shipment..."):

                answer = run_agent(
                    user_message,
                    verbose=True
                )

            st.markdown(answer)

        # Save response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


# --------------------------------------------------
# Previous conversation
# --------------------------------------------------

if st.session_state.messages:

    st.divider()

    st.subheader("Conversation")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("🔧 Debug")

    st.write(
        "Tool calls and agent activity are printed "
        "to the terminal where Streamlit is running."
    )

    st.divider()

    st.subheader("Supported Issues")

    st.write("📦 Damaged Package")
    st.write("🚚 Failed Delivery")
    st.write("📄 Missing Documentation")
    st.write("📍 Bad Address")
    st.write("⏰ Delayed Shipment")

    st.divider()

    if st.button("Clear Conversation"):

        st.session_state.messages = []

        st.rerun()