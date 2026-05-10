"""
Home page for the Adaptive RAG Streamlit application.
"""

import logging
import streamlit as st

# Configure page settings (must be the first Streamlit command)
st.set_page_config(
    page_title="Adaptive RAG",
    page_icon="🤖",
    layout="wide"
)

# Hide sidebar for cleaner look
hide_sidebar_style = """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ---- Main Page UI ----
st.title("🤖 Adaptive RAG Assistant")
st.markdown("##### Intelligent Question Answering with Dynamic Query Routing")

st.markdown("---")

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state["session_id"] = "active-session"

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# If already logged in, redirect to chat
if st.session_state["logged_in"]:
    st.switch_page("pages/chat.py")

# Login / Signup form
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### 🔐 Login to Continue")

    with st.form("auth_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        mode = st.radio("Choose action:", ["Login", "Create Account"], horizontal=True)
        submit = st.form_submit_button("Submit", use_container_width=True)

    if submit:
        if not username or not password:
            st.error("❌ Username and password are required.")
        else:
            # Set session and redirect to chat page
            st.session_state["username"] = username
            st.session_state["logged_in"] = True
            st.session_state["jwt_token"] = "local-token"

            if mode == "Create Account":
                st.success(f"✅ Account created for **{username}**! Redirecting...")
            else:
                st.success(f"✅ Welcome back, **{username}**! Redirecting...")

            st.switch_page("pages/chat.py")

st.markdown("---")

# Feature highlights
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("#### 📄 Upload Documents")
    st.markdown("Upload PDFs or text files and ask questions about them.")
with c2:
    st.markdown("#### 🔍 Smart Retrieval")
    st.markdown("Adaptive routing decides the best source for your query.")
with c3:
    st.markdown("#### 🌐 Web Search Fallback")
    st.markdown("If documents don't have the answer, it searches the web.")
