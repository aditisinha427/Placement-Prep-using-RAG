from google import genai

from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("API_KEY"))

def generate_response(prompt):
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    return response.text



from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


def load_db():
    with open("data.txt", "r") as    f:
        text = f.read()

    splitter = CharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    docs = splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings()

    db = FAISS.from_texts(docs, embeddings)

    return db


def search(query, db):
    docs = db.similarity_search(query, k=2)
    return " ".join([doc.page_content for doc in docs])

chat_history=[]

def get_answer(query, db):
    context = search(query, db)

    history_text = "\n".join(
    [f"{msg['role']}: {msg['content']}" for msg in chat_history[-4:]]
) 

    prompt = f"""
You are a helpful and conversational AI assistant for placement preparation.

Instructions:
- Answer clearly and naturally
- Use the provided context if relevant
- Maintain conversation continuity
- Do not say "based on context"


Chat History:
{history_text}

Context:
{context}

User: {query}
Assistant:
"""

    answer = generate_response(prompt)

    # store conversation
    chat_history.append({"role": "user", "content": query})
    chat_history.append({"role": "assistant", "content": answer})

    return answer
