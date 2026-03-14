from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def load_documents(folder="docs"):

    documents = []

    for folder_name in ["docs", "uploads"]:

        if not os.path.exists(folder_name):
            continue

        for file in os.listdir(folder_name):

            if file.endswith(".pdf"):

                path = os.path.join(folder_name, file)

                loader = PyPDFLoader(path)

                docs = loader.load()

                for doc in docs:
                    doc.metadata["source"] = file

                documents.extend(docs)

    return documents

def load_documents(folder="docs"):

    documents = []

    for file in os.listdir(folder):

        if file.endswith(".pdf"):
            path = os.path.join(folder, file)

            loader = PyPDFLoader(path)

            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = file

            documents.extend(docs)

    return documents


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    return splitter.split_documents(documents)