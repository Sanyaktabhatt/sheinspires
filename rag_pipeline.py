from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_classic.chains import RetrievalQA

from document_processor import load_documents, split_documents


def create_rag():

    docs = load_documents()
    chunks = split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="vector_db"
    )

    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever
    )

    return qa
