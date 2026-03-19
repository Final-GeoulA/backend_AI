from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader,PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

documents = []
documents.extend(TextLoader("data/acne.txt", encoding="utf-8").load())
documents.extend(TextLoader("data/skin_faq.txt", encoding="utf-8").load())
documents.extend(TextLoader("data/atopic.txt", encoding="utf-8").load())

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=50
)
split_docs = splitter.split_documents(documents)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vectorstore = FAISS.from_documents(split_docs, embeddings)
os.makedirs("db", exist_ok=True)
vectorstore.save_local("db/acne_index")
vectorstore.save_local("db/atopic_index")
print("인덱스 저장 완료")
print(f"문서 수 : {len(documents)}")
print(f"청크 수 : {len(split_docs)}")