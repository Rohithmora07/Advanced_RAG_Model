import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from mistralai.client import Mistral

load_dotenv()

CHROMA_DIR = "chroma_db"
CHROMA_HOST = os.getenv("CHROMA_HOST")
CHROMA_API_KEY = os.getenv("CHROMA_API_KEY")
CHROMA_TENANT = os.getenv("CHROMA_TENANT")
CHROMA_DATABASE = os.getenv("CHROMA_DATABASE")
CHROMA_SSL = os.getenv("CHROMA_SSL", "true").lower() in ("1", "true", "yes")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "mistral-small-latest"


def load_embeddings():
    """Load the HuggingFace embedding model."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def load_vectorstore(embeddings=None):
    """Load the existing Chroma vector store using cloud or local settings."""
    if embeddings is None:
        embeddings = load_embeddings()

    if CHROMA_API_KEY and CHROMA_TENANT and CHROMA_DATABASE:
        return Chroma(
            embedding_function=embeddings,
            chroma_cloud_api_key=CHROMA_API_KEY,
            tenant=CHROMA_TENANT,
            database=CHROMA_DATABASE,
        )

    if CHROMA_HOST:
        headers = None
        if CHROMA_API_KEY:
            headers = {"Authorization": f"Bearer {CHROMA_API_KEY}"}

        return Chroma(
            host=CHROMA_HOST,
            ssl=CHROMA_SSL,
            headers=headers,
            embedding_function=embeddings,
        )

    if not os.path.isdir(CHROMA_DIR):
        raise FileNotFoundError(f"ChromaDB directory not found: {CHROMA_DIR}")

    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
    )


def load_llm():
    """Load the Mistral client using the configured API key."""
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise EnvironmentError("Missing MISTRAL_API_KEY environment variable.")

    return Mistral(api_key=api_key)


def retrieve_context(query, vectorstore, k=3, with_scores=False):
    """Retrieve the top-k similar documents from ChromaDB.

    If with_scores=True, return a tuple (documents, scores). Otherwise return documents.
    """
    if with_scores and hasattr(vectorstore, "similarity_search_with_score"):
        results = vectorstore.similarity_search_with_score(query, k=k)
        documents = [doc for doc, _ in results]
        scores = [score for _, score in results]
        return documents, scores

    documents = vectorstore.similarity_search(query, k=k)
    if with_scores:
        return documents, [None] * len(documents)
    return documents


def build_prompt(query, documents):
    """Build a RAG prompt from retrieved documents and the user query."""
    context = "\n\n".join(doc.page_content for doc in documents)
    return f"""Answer the question using only the provided context.

Context:
{context}

Question:
{query}
"""


def generate_answer(query, llm, documents):
    """Generate a final answer from Mistral."""
    prompt = build_prompt(query, documents)
    response = llm.chat.complete(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content.strip()


def main():
    """Legacy CLI entrypoint preserved for console use."""
    print("Loading RAG system...")

    vectorstore = load_vectorstore()
    client = load_llm()

    print("RAG system ready!")

    while True:
        query = input("\nEnter your query (or type 'exit'): ").strip()

        if query.lower() == "exit":
            break

        results = retrieve_context(query, vectorstore, k=3)
        answer = generate_answer(query, client, results)

        print("\nAnswer:\n")
        print(answer)


if __name__ == "__main__":
    main()
