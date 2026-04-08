from google import genai

client = genai.Client(api_key="AIzaSyDdOJ13QJg2a8WyphCrnxu2YQW2o1peJaE")

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

    history_text = "\n".join(chat_history[-6:])  

    prompt = f"""
You are a helpful, conversational AI assistant for placement preparation.
- Answer clearly and naturally
- Use context if relevant
- Remember previous conversation
-Do not say "based on context"

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
