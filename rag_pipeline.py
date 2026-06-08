import os
import shutil

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

# Config
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
CHROMA_DIR = os.path.join(ROOT_DIR, "chroma_db")
CHROMA_HOST = os.getenv("CHROMA_HOST")
CHROMA_API_KEY = os.getenv("CHROMA_API_KEY")
CHROMA_TENANT = os.getenv("CHROMA_TENANT")
CHROMA_DATABASE = os.getenv("CHROMA_DATABASE")
CHROMA_SSL = os.getenv("CHROMA_SSL", "true").lower() in ("1", "true", "yes")

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def main():

    # Clear old local database only when using local persistence.
    if not CHROMA_HOST and not (CHROMA_API_KEY and CHROMA_TENANT and CHROMA_DATABASE):
        if os.path.exists(CHROMA_DIR):
            shutil.rmtree(CHROMA_DIR)
            print(f"Cleared old ChromaDB: {CHROMA_DIR}")

    # Load documents
    print("Loading documents...")

    loader = DirectoryLoader(
        DOCS_DIR,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )

    documents = loader.load()

    print(f"Loaded {len(documents)} documents")

    # Split documents
    print("Splitting documents...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    # Embeddings
    print("Loading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    # Create Chroma vector store
    print("Building ChromaDB index...")

    if CHROMA_API_KEY and CHROMA_TENANT and CHROMA_DATABASE:
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            chroma_cloud_api_key=CHROMA_API_KEY,
            tenant=CHROMA_TENANT,
            database=CHROMA_DATABASE,
        )
    elif CHROMA_HOST:
        headers = None
        if CHROMA_API_KEY:
            headers = {"Authorization": f"Bearer {CHROMA_API_KEY}"}

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            host=CHROMA_HOST,
            ssl=CHROMA_SSL,
            headers=headers,
        )
    else:
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_DIR,
        )

    print("ChromaDB successfully created!")
    print(f"Indexed chunks: {len(chunks)}")
    print(f"ChromaDB collection count after indexing: {vectorstore._collection.count()}")


if __name__ == "__main__":
    main()
