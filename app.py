import os
import streamlit as st
from dotenv import load_dotenv

from query import (
    EMBEDDING_MODEL,
    generate_answer,
    load_embeddings,
    load_llm,
    load_vectorstore,
    retrieve_context,
)

load_dotenv()

st.set_page_config(
    page_title="CS INTERVIEW COACH",
    layout="wide",
    initial_sidebar_state="expanded",
)

TOPICS = [
    {"label": "DSA", "dot": "🟣"},
    {"label": "System Design", "dot": "🟢"},
    {"label": "OS / DBMS", "dot": "🔵"},
    {"label": "OOP / CN", "dot": "🟡"},
    {"label": "HR / Behavioral", "dot": "🟠"},
    {"label": "Coding Patterns", "dot": "🔴"},
]

WELCOME_MESSAGE = (
    "Hi! I'm your CS Interview Coach powered by Advanced RAG. "
    "Ask me anything about DSA, System Design, OS, DBMS, OOP, CN, or Behavioral Interviews."
)


@st.cache_resource(show_spinner=False)
def get_embeddings():
    return load_embeddings()


@st.cache_resource(show_spinner=False)
def get_vectorstore():
    return load_vectorstore(get_embeddings())


@st.cache_resource(show_spinner=False)
def get_llm():
    return load_llm()


def inject_styles():
    st.markdown(
        """
        <style>
        .css-18ni7ap.e8zbici2 {
            background-color: #0b1220 !important;
        }
        .stApp {
            background-color: #0b1220;
            color: #e6f1ff;
        }
        .main .block-container {
            padding-top: 1.2rem;
            padding-left: 1.2rem;
            padding-right: 1.2rem;
            background-color: #0b1220;
        }
        .css-1d391kg {
            background-color: #0b1220;
        }
        div[data-testid="stSidebar"] {
            background-color: #F5C518;
            color: #1a1a1a;
            min-width: 250px;
        }
        div[data-testid="stSidebar"] * {
            color: #1a1a1a !important;
        }
        div[data-testid="stSidebar"] label {
            color: #1a1a1a !important;
        }
        div[data-testid="stSidebar"] .stRadio label p {
            color: #1a1a1a !important;
        }
        div[data-testid="stSidebar"] p,
        div[data-testid="stSidebar"] span,
        div[data-testid="stSidebar"] div,
        div[data-testid="stSidebar"] a {
            color: #1a1a1a !important;
        }
        div[data-testid="stSidebarContent"] {
            background-color: #F5C518 !important;
        }
        div[data-testid="stSidebar"] input,
        div[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stSidebar"] h3,
        div[data-testid="stSidebar"] strong {
            color: #1a1a1a !important;
        }
        div[data-testid="stSidebar"] div[data-baseweb="radio"] {
            border: 1px solid #1a1a1a !important;
            border-radius: 8px !important;
            background: rgba(0,0,0,0.06) !important;
            padding: 4px 8px !important;
            margin-bottom: 4px !important;
        }
        div[data-testid="stSidebar"] [data-testid="stProgressBar"] > div {
            background-color: #1a1a1a !important;
        }
        .sidebar-content {
            padding: 1rem 1rem 1rem 1rem;
        }
        .topic-button {
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            padding: 0.9rem 1rem;
            margin-bottom: 0.5rem;
            border-radius: 16px;
            border: 1px solid #F5C518;
            background-color: #111b33;
            color: #e6f1ff;
            font-weight: 500;
        }
        .topic-button.selected {
            border-color: #F5C518;
            background: linear-gradient(135deg, rgba(245,197,24,0.22), rgba(17,28,51,0.95));
        }
        .status-card {
            border-radius: 18px;
            padding: 1rem;
            margin-bottom: 1rem;
            background: #0f172a;
            border: 1px solid #F5C518 !important;
        }
        .response-card {
            border-radius: 22px;
            padding: 1.4rem;
            background: #0f172a;
            border: 1px solid #F5C518 !important;
            box-shadow: 0 20px 50px rgba(245,197,24,0.08);
            margin-bottom: 1rem;
        }
        .topic-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.4rem 0.8rem;
            border-radius: 999px;
            background: rgba(245,197,24,0.18);
            color: #F5C518;
            font-size: 0.9rem;
            font-weight: 600;
        }
        .assistant-message {
            background: #0f172a;
            border: 1px solid #F5C518 !important;
            border-radius: 22px;
            padding: 1rem;
            color: #e6f1ff;
        }
        .user-message {
            background: #111827;
            border: 1px solid #F5C518 !important;
            border-radius: 22px;
            padding: 1rem;
            color: #e6f1ff;
        }
        .sidebar-footer {
            margin-top: 1.5rem;
            padding: 1rem;
            border-radius: 18px;
            background: rgba(0,0,0,0.08);
            border: 1px solid #1a1a1a !important;
        }
        .sidebar-footer,
        .sidebar-footer * {
            color: #1a1a1a !important;
        }

        .sidebar-footer p {
            margin: 0.45rem 0;
        }
        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.9rem;
            color: #cbd5e1;
        }
        .status-pill span {
            width: 8px;
            height: 8px;
            border-radius: 999px;
            background: #22c55e;
            display: inline-block;
        }
        .sidebar-title {
            color: #1a1a1a;
            font-size: 1.05rem;
            margin-bottom: 0.75rem;
            font-weight: 700;
        }
        .welcome-card {
            border-radius: 22px;
            padding: 1.4rem;
            background: #0f172a;
            border: 1px solid #F5C518 !important;
            margin-bottom: 1.5rem;
        }
        .welcome-title {
            font-size: 1.5rem;
            margin-bottom: 0.6rem;
            color: #e2e8f0;
        }
        div[data-testid="stExpander"] {
            border: 1px solid #F5C518 !important;
            border-radius: 12px !important;
        }
        div[data-testid="stChatMessage"] {
            border: 1px solid #F5C518 !important;
            border-radius: 16px !important;
        }
        div[data-testid="stChatInput"] {
            border: 1px solid #F5C518 !important;
            border-radius: 16px !important;
        }
        div[data-testid="stSidebar"],
        div[data-testid="stSidebar"] * {
            color: #1a1a1a !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def initialize_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "message": WELCOME_MESSAGE,
                "topic": "Welcome",
                "sources": [],
            }
        ]
    if "selected_topic" not in st.session_state:
        st.session_state.selected_topic = TOPICS[0]["label"]
    if "retrieved_contexts" not in st.session_state:
        st.session_state.retrieved_contexts = []
    if "last_relevance_score" not in st.session_state:
        st.session_state.last_relevance_score = None
    if "last_confidence_level" not in st.session_state:
        st.session_state.last_confidence_level = None
    if "last_retrieved_chunks" not in st.session_state:
        st.session_state.last_retrieved_chunks = 0
    if "last_top_source" not in st.session_state:
        st.session_state.last_top_source = None
    if "last_hallucination_risk" not in st.session_state:
        st.session_state.last_hallucination_risk = None


def get_topic_cards(selected_topic):
    labels = [f"{topic['dot']} {topic['label']}" for topic in TOPICS]
    try:
        index = next(
            i for i, topic in enumerate(TOPICS) if topic["label"] == selected_topic
        )
    except StopIteration:
        index = 0

    selected_label = st.sidebar.radio(
        "",
        labels,
        index=index,
        label_visibility="collapsed",
    )

    selected = next(
        topic["label"] for topic in TOPICS if f"{topic['dot']} {topic['label']}" == selected_label
    )
    st.session_state.selected_topic = selected


def get_index_stats(vectorstore):
    try:
        count = vectorstore._collection.count()
        return count
    except Exception:
        try:
            result = vectorstore._collection.get(include=["documents"])
            return len(result.get("documents", []))
        except Exception:
            return None


def render_sidebar(kb_ready, index_count, llm_ready):
    st.sidebar.markdown("<div class='sidebar-title'>Topics</div>", unsafe_allow_html=True)
    get_topic_cards(st.session_state.selected_topic)
    st.sidebar.markdown(
        f"""

            **Indexed chunks:** {index_count if index_count is not None else 'Unknown'}

            **ChromaDB status:** {'Active' if kb_ready else 'Unavailable'}

            **Mistral status:** {'Connected' if llm_ready else 'Unavailable'}

        """,
        unsafe_allow_html=True,
    )

    relevance_label = (
        f"{st.session_state.last_relevance_score}%" if st.session_state.last_relevance_score is not None else "N/A"
    )
    confidence_label = (
        st.session_state.last_confidence_level if st.session_state.last_confidence_level else "N/A"
    )
    source_label = st.session_state.last_top_source or "N/A"
    chunks_label = st.session_state.last_retrieved_chunks
    hallucination_label = st.session_state.last_hallucination_risk or "N/A"

    st.sidebar.markdown(
        f"""

            Response Analytics
            **Relevance Score:** {relevance_label}

            **Confidence Level:** {confidence_label}

            **Retrieved chunks:** {chunks_label}

            **Top source document:** {source_label}

            **Hallucination risk:** {hallucination_label}

        """,
        unsafe_allow_html=True,
    )
    if st.session_state.last_relevance_score is not None:
        st.sidebar.progress(st.session_state.last_relevance_score / 100)


def render_header():
    st.markdown(
        "<div class='welcome-card'><div class='welcome-title'>CS Interview Coach</div>"
        "<div class='status-pill'><span></span> RAG Active · ChromaDB + Mistral</div></div>",
        unsafe_allow_html=True,
    )


def render_chat_history():
    for turn in st.session_state.chat_history:
        if turn["role"] == "user":
            with st.chat_message("user"):
                st.markdown(
                    f"<div class='user-message'>{turn['message']}</div>",
                    unsafe_allow_html=True,
                )
        else:
            with st.chat_message("assistant"):
                topic = turn.get("topic", st.session_state.selected_topic)
                st.markdown(
                    "<div class='response-card'>"
                    f"<div class='topic-badge'>{topic} · Medium</div>"
                    f"<div style='margin-top:1rem;'>{turn['message']}</div>"
                    "</div>",
                    unsafe_allow_html=True,
                )
                if turn.get("sources"):
                    with st.expander("Retrieved Context"):
                        for idx, source in enumerate(turn["sources"], start=1):
                            source_label = source.get("source", "Unknown source")
                            chunk_label = source.get("chunk_id")
                            st.markdown(
                                f"**Chunk {idx} — {source_label} {f'(chunk {chunk_label})' if chunk_label else ''}**"
                            )
                            st.write(source.get("content", ""))


def add_chat_entry(role, message, sources=None, topic=None):
    st.session_state.chat_history.append(
        {
            "role": role,
            "message": message,
            "sources": sources or [],
            "topic": topic if topic else st.session_state.selected_topic,
        }
    )


def create_prompt(query, documents):
    context = "\n\n".join(doc.page_content for doc in documents)
    return f"""Answer the question using only the provided context.

Context:
{context}

Question:
{query}
"""


def format_sources(results):
    formatted = []
    for idx, doc in enumerate(results, start=1):
        metadata = getattr(doc, "metadata", {}) or {}
        formatted.append(
            {
                "content": doc.page_content,
                "source": metadata.get("source", metadata.get("source_document", "unknown")),
                "chunk_id": metadata.get("chunk", idx),
            }
        )
    return formatted


def compute_relevance_metrics(scores):
    if not scores:
        return None, None

    valid_scores = [s for s in scores if s is not None]
    if not valid_scores:
        return None, None

    avg_distance = sum(valid_scores) / len(valid_scores)
    similarity = max(0.0, 1.0 - (avg_distance / 2.0))
    relevance = int(similarity * 100)

    if relevance >= 80:
        confidence = "High"
    elif relevance >= 60:
        confidence = "Medium"
    else:
        confidence = "Low"

    return relevance, confidence


def main():
    inject_styles()
    initialize_session_state()

    kb_ready = False
    llm_ready = False
    index_count = None
    vectorstore = None
    llm_client = None
    error_message = None

    try:
        vectorstore = get_vectorstore()
        kb_ready = True
        index_count = get_index_stats(vectorstore)
    except FileNotFoundError:
        error_message = "ChromaDB folder not found. Please run the existing pipeline and keep chroma_db in the project root."
    except Exception as err:
        error_message = f"Unable to load the knowledge base: {err}"

    try:
        llm_client = get_llm()
        llm_ready = True
    except EnvironmentError:
        error_message = "Missing MISTRAL_API_KEY in environment variables."
    except Exception as err:
        error_message = f"Unable to connect to Mistral: {err}"

    render_sidebar(kb_ready, index_count, llm_ready)
    render_header()
    render_chat_history()

    if error_message:
        st.error(error_message)
        return

    user_query = st.chat_input("Send your interview question...")
    if user_query is not None:
        cleaned = user_query.strip()
        if not cleaned:
            st.warning("Please enter a valid question before submitting.")
        else:
            add_chat_entry("user", cleaned)
            try:
                with st.spinner("Searching knowledge base..."):
                    results, similarity_scores = retrieve_context(cleaned, vectorstore, k=5, with_scores=True)

                if not results:
                    st.error("No relevant documents were found. Try a different phrasing.")
                else:
                    sources = format_sources(results)
                    with st.spinner("Generating answer with Mistral..."):
                        answer = generate_answer(cleaned, llm_client, results)

                    relevance, confidence = compute_relevance_metrics(similarity_scores)
                    st.session_state.last_relevance_score = relevance
                    st.session_state.last_confidence_level = confidence
                    st.session_state.last_retrieved_chunks = len(results)
                    st.session_state.last_top_source = sources[0]["source"] if sources else None
                    if relevance is None:
                        hallucination_risk = "Unknown"
                    elif relevance >= 80:
                        hallucination_risk = "Low"
                    elif relevance >= 60:
                        hallucination_risk = "Medium"
                    else:
                        hallucination_risk = "High"
                    st.session_state.last_hallucination_risk = hallucination_risk

                    add_chat_entry(
                        "assistant",
                        answer,
                        sources=sources,
                        topic=st.session_state.selected_topic,
                    )
                    st.session_state.retrieved_contexts.append(sources)
                    st.rerun()
            except Exception as err:
                st.error(f"There was a problem generating your answer: {err}")


if __name__ == "__main__":
    main()
