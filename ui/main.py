import sys
import os
import streamlit as st
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
load_dotenv()

admin_password = os.getenv("ADMIN_PASSWORD")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from graph.workflow import app
except ImportError:
    st.error("Workflow not found!")

st.set_page_config(page_title="QuickFix AI", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top left, #1e293b, #0f172a);
        color: #f8fafc;
    }
    .main .block-container {
        padding-top: 2rem;
        max-width: 700px;
    }
    .glass-header {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 30px;
    }
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 18px !important;
        margin-bottom: 15px !important;
        backdrop-filter: blur(5px);
    }
    [data-testid="stChatMessage"]:nth-child(even) {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
    }
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    .admin-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        border-left: 4px solid #3b82f6;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- ADMIN LOGIC WITH PASSWORD ---
is_admin = st.query_params.get("view") == "admin"

if is_admin:
    with st.sidebar:
        st.markdown("<h2 style='color:#3b82f6;'>💎 Admin Dashboard</h2>", unsafe_allow_html=True)
        
        # Password Input
        pwd = st.text_input("Enter Admin Password", type="password")
        
        if pwd == admin_password: 
            st.success("Access Granted")
            if os.path.exists('leads.csv'):
                with open('leads.csv', 'r') as f:
                    leads = f.readlines()[-10:]
                    for l in reversed(leads):
                        st.markdown(f"<div class='admin-card'>{l}</div>", unsafe_allow_html=True)
            else:
                st.write("No leads yet.")
        elif pwd:
            st.error("Incorrect Password")
else:
    st.markdown("<style>[data-testid='stSidebar'] {display: none;}</style>", unsafe_allow_html=True)


st.markdown("""
    <div class="glass-header">
        <h1 style='margin:0; font-size: 2rem; color: #3b82f6;'>QuickFix <span style='color:white;'>AI</span></h1>
        <p style='margin:0; opacity:0.6; font-size: 0.9rem;'>Premium Plumbing Support Agent</p>
    </div>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm your QuickFix expert. How can I help you today?"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("You can get information here or book an appointment....."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            inputs = {"messages": [HumanMessage(content=prompt)]}
            result = app.invoke(inputs)
            response = result["answer"]
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    if is_admin:
        st.rerun()