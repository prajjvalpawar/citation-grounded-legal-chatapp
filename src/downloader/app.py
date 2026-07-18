import streamlit as st
import uuid
from datetime import datetime
from chatbot import chatbot

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Citation-Grounded Legal Information Chatbot",
    page_icon="⚖️",
    layout="centered"
)

# ----------------------------
# Professional Dark Theme CSS
# ----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #111827;
        color: #e5e7eb;
    }
    .header-box {
        background-color: #1f2937;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #374151;
        margin-bottom: 25px;
    }
    .title {
        font-size: 30px;
        font-weight: 700;
        color: #f9fafb;
    }
    .subtitle {
        font-size: 15px;
        color: #9ca3af;
        margin-top: 8px;
    }
    .disclaimer {
        font-size: 12px;
        color: #6b7280;
        margin-top: 10px;
        font-style: italic;
    }
    .stChatMessage {
        background-color: #1f2937;
        border-radius: 12px;
    }
    .stChatInput textarea {
        background-color: #1f2937;
        color: #f9fafb;
    }

    /* Sidebar chat history styling */
    section[data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px solid #1f2937;
    }
    div[data-testid="stSidebar"] button {
        text-align: left;
        border-radius: 8px;
    }
    .chat-item-active button {
        background-color: #1f2937 !important;
        border: 1px solid #374151 !important;
        color: #f9fafb !important;
    }
    .sidebar-section-label {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #6b7280;
        margin-top: 18px;
        margin-bottom: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Session State: multi-chat storage
# ----------------------------
def new_chat(select=True):
    chat_id = str(uuid.uuid4())
    st.session_state.chats[chat_id] = {
        "title": "New chat",
        "messages": [],
        "created_at": datetime.now().strftime("%b %d, %H:%M")
    }
    if select:
        st.session_state.current_chat_id = chat_id
    return chat_id


if "chats" not in st.session_state:
    st.session_state.chats = {}
    st.session_state.current_chat_id = None
    new_chat()

if not st.session_state.current_chat_id or st.session_state.current_chat_id not in st.session_state.chats:
    new_chat()

current_chat = st.session_state.chats[st.session_state.current_chat_id]

# ----------------------------
# Sidebar: New Chat + History + Clear History
# ----------------------------
with st.sidebar:
    st.markdown("### ⚖️ Legal Chatbot")

    if st.button("➕ New chat", use_container_width=True):
        new_chat()
        st.rerun()

    st.markdown('<div class="sidebar-section-label">Chat history</div>', unsafe_allow_html=True)

    # Sort chats by most recently created first
    sorted_chat_ids = sorted(
        st.session_state.chats.keys(),
        key=lambda cid: st.session_state.chats[cid]["created_at"],
        reverse=True
    )

    if not sorted_chat_ids:
        st.caption("No conversations yet.")

    for chat_id in sorted_chat_ids:
        chat = st.session_state.chats[chat_id]
        is_active = chat_id == st.session_state.current_chat_id

        col1, col2 = st.columns([5, 1])
        with col1:
            label = f"{'🟢 ' if is_active else ''}{chat['title']}"
            if st.button(label, key=f"select_{chat_id}", use_container_width=True):
                st.session_state.current_chat_id = chat_id
                st.rerun()
        with col2:
            if st.button("🗑️", key=f"delete_{chat_id}", help="Delete this chat"):
                del st.session_state.chats[chat_id]
                if st.session_state.current_chat_id == chat_id:
                    st.session_state.current_chat_id = None
                st.rerun()

    st.divider()

    if st.button("🧹 Clear all history", use_container_width=True):
        st.session_state.chats = {}
        st.session_state.current_chat_id = None
        new_chat()
        st.rerun()

    st.divider()
    st.caption("Knowledge base: UAE Data Protection Law")

# ----------------------------
# Header
# ----------------------------
st.markdown(
    """
    <div class="header-box">
    <div class="title">
    Citation-Grounded Legal Information Chatbot
    </div>
    <div class="subtitle">
    This chatbot provides legal information on UAE Data Protection Law.
    It does not constitute professional legal advice.
    </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Chat History (current conversation)
# ----------------------------
for message in current_chat["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ----------------------------
# User Question
# ----------------------------
question = st.chat_input("Ask your legal question...")

if question:
    current_chat["messages"].append({"role": "user", "content": question})

    # Auto-title the chat from the first user message
    if current_chat["title"] == "New chat":
        current_chat["title"] = (question[:40] + "…") if len(question) > 40 else question

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching legal documents..."):
            answer = chatbot(question, current_chat["messages"])
        st.write(answer)

    current_chat["messages"].append({"role": "assistant", "content": answer})
    st.rerun()