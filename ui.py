import streamlit as st
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

from confluence_rag.pipeline import ask

st.set_page_config(
    page_title="Confluence RAG",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Confluence RAG - Query your documentation with AI."
    }
)

# Modern CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .stExpander {
        border: 1px solid #ddd;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">📚 Confluence RAG</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Intelligent Q&A over your Confluence documentation</div>', unsafe_allow_html=True)

# Initialize session state
if "chats" not in st.session_state:
    st.session_state.chats = [[]]  # List of chats, each chat is a list of messages
if "current_chat" not in st.session_state:
    st.session_state.current_chat = 0

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Chat management
    chat_options = [f"Chat {i+1}" for i in range(len(st.session_state.chats))]
    selected_chat = st.selectbox("Select Chat", chat_options, index=st.session_state.current_chat)
    st.session_state.current_chat = chat_options.index(selected_chat)
    
    if st.button("➕ New Chat"):
        st.session_state.chats.append([])
        st.session_state.current_chat = len(st.session_state.chats) - 1
        st.rerun()
    
    if st.button("🗑️ Delete Current Chat") and len(st.session_state.chats) > 1:
        del st.session_state.chats[st.session_state.current_chat]
        if st.session_state.current_chat >= len(st.session_state.chats):
            st.session_state.current_chat = len(st.session_state.chats) - 1
        st.rerun()
    
    st.divider()
    
    if st.button("🔄 Sync Knowledge Base"):
        with st.spinner("Syncing data..."):
            try:
                subprocess.Popen(["python", "run_ingest.py"], cwd=os.getcwd())
                st.success("Sync initiated successfully!")
            except Exception as e:
                st.error(f"Sync failed: {e}")
    
    if st.button("🗑️ Clear Current Chat"):
        st.session_state.chats[st.session_state.current_chat] = []
        st.rerun()

# Get current messages
messages = st.session_state.chats[st.session_state.current_chat]

# Display chat messages
for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📄 Sources"):
                for src in message["sources"]:
                    title = src.get('title', 'Untitled')
                    text_snippet = src.get('text', '')[:150] + '...' if len(src.get('text', '')) > 150 else src.get('text', '')
                    if text_snippet.strip():  # Only show if there's content
                        st.markdown(f"**{title}**\n{text_snippet}")
                    else:
                        st.markdown(f"**{title}** (No content available)")

# Chat input
if prompt := st.chat_input("Ask a question about your docs..."):
    # Add user message
    messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Generating answer..."):
            answer, sources = ask(prompt)
        st.markdown(answer)
        if sources:
            with st.expander("📄 Sources"):
                for src in sources:
                    title = src.get('title', 'Untitled')
                    text_snippet = src.get('text', '')[:150] + '...' if len(src.get('text', '')) > 150 else src.get('text', '')
                    if text_snippet.strip():  # Only show if there's content
                        st.markdown(f"**{title}**\n{text_snippet}")
                    else:
                        st.markdown(f"**{title}** (No content available)")
    messages.append({"role": "assistant", "content": answer, "sources": sources})