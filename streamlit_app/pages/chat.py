"""
Chat page for the Adaptive RAG Streamlit application.
"""

import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="Adaptive RAG - Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Check authentication
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("⚠️ Please login first.")
    st.switch_page("home.py")
    st.stop()

# Initialize logout confirmation state
if "show_logout_confirm" not in st.session_state:
    st.session_state.show_logout_confirm = False

# Header with user info and logout button
col1, col2 = st.columns([10, 2])
with col1:
    st.title("💬 Adaptive RAG Chat")
with col2:
    st.write("")  # Spacer
    if st.button("🔒 Logout", use_container_width=True):
        st.session_state.show_logout_confirm = True

# Logout confirmation dialog
if st.session_state.show_logout_confirm:
    st.warning("Are you sure you want to logout?")
    col_confirm, col_cancel = st.columns(2)
    with col_confirm:
        if st.button("✅ Yes, logout"):
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            # Redirect to home page
            st.switch_page("home.py")
    with col_cancel:
        if st.button("❌ Cancel"):
            st.session_state.show_logout_confirm = False

# Document upload section
with st.sidebar:
    st.header("📂 Upload Documents")
    st.markdown(f"Logged in as: **{st.session_state.get('username', 'User')}**")
    st.markdown("---")

    uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

    if uploaded_file:
        file_description = st.text_input(
            "📄 Describe your document (required)",
            max_chars=300,
            placeholder="E.g. LangGraph tutorial with workflows and code examples"
        )

        if "uploaded_files" not in st.session_state:
            st.session_state.uploaded_files = {}

        file_key = f"{uploaded_file.name}_{file_description}"

        if file_description:
            if file_key not in st.session_state.uploaded_files:
                st.success(f"✅ Uploaded: {uploaded_file.name}")
                st.session_state.uploaded_files[file_key] = True
            else:
                st.info(f"Already uploaded: {uploaded_file.name}")
        else:
            st.warning("Please describe your document before uploading.")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for role, text in st.session_state.chat_history:
    st.chat_message(role).write(text)

# User input
user_input = st.chat_input("Ask a question...")

# Process user input and get response
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").write(user_input)

    # Show a placeholder response (backend not connected on Streamlit Cloud)
    response = f"🤖 Thank you for your question: *\"{user_input}\"*\n\nTo get real AI-powered answers, please run this app locally with the FastAPI backend. See the README for setup instructions."
    st.session_state.chat_history.append(("assistant", response))
    st.chat_message("assistant").write(response)
