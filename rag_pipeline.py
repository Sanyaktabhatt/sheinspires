from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_classic.chains import RetrievalQA

import os

from document_processor import load_documents, split_documents
from conflict_detector import detect_conflict


def create_rag():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    if not os.path.exists("vector_db"):

        docs = load_documents()

        chunks = split_documents(docs)

        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory="vector_db"
        )

        vector_db.persist()

    else:

        vector_db = Chroma(
            persist_directory="vector_db",
            embedding_function=embeddings
        )

    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    llm = ChatOllama(
        model="qwen3",
        temperature=0
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return qa