import streamlit as st
from rag import load_db, get_answer

# Load DB once
db = load_db()

st.set_page_config(page_title="Placement Prep Copilot", layout="centered")

st.title("🤖 Placement Prep Copilot")
st.write("Ask questions on OS, DBMS, CN")

# Input box
query = st.text_input("Enter your question:")

# Button
if st.button("Ask"):
    if query:
        answer = get_answer(query, db)
        st.subheader("Answer:")
        st.write(answer)
    else:
        st.warning("Please enter a question")