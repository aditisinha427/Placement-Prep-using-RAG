import streamlit as st
from rag import load_db, get_answer

# Load DB once
db = load_db()

st.set_page_config(page_title="Placement Prep Copilot", layout="centered")

st.title("🤖 Placement Prep Copilot")
st.write("Ask questions on OS, DBMS, CN")

# -------------------------------
# Initialize chat history
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# Display chat history
# -------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------
# Chat input (replaces text_input + button)
# -------------------------------
user_input = st.chat_input("Ask something...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response
    response = get_answer(user_input, db)

    # Show assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)