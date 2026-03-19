import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from .prompts import RAG_PROMPT

load_dotenv()
# 1. 생성한 벡터의 인덱스 가져오기
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, "db", "acne_index")

# 2. 한번 더 임베딩 로딩
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 3. FAISS 인덱스 로딩
vectorstore = FAISS.load_local(
    INDEX_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)
# 검색할 때 가장 유사한 결과를 2개 반환
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# 모델
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2,
    max_tokens=200
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def ask_acne_chatbot(question: str):
    docs = retriever.invoke(question)
    context = format_docs(docs)

    prompt_value = RAG_PROMPT.invoke({
        "context": context,
        "question": question
    })

    response = llm.invoke(prompt_value)

    sources = []
    for doc in docs:
        sources.append({
            "source": doc.metadata.get("source", ""),
            "preview": doc.page_content[:120]
        })

    return {
        "question": question,
        "answer": response.content,
        "sources": sources
    }