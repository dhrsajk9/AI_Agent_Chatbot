import os
import requests
from dotenv import load_dotenv
load_dotenv()

# Set backend URL from env or use localhost fallback
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:9999")
API_URL = f"{BACKEND_URL}/chat"

# 🟡 Wake up the backend on app load (in case it's asleep)
try:
    requests.post(API_URL, json={
        "model_name": "gpt-4o-mini",
        "model_provider": "OpenAI",
        "prompt": "Ping",
        "messages": ["Hi"],
        "allow_search": False
    }, timeout=1)
except:
    pass  # Ignore if backend is still waking up

# ===== Streamlit UI Setup =====
import streamlit as st

st.set_page_config(page_title="langGraph AI Agent", layout="wide")
st.title("AI Chatbot Agents")
st.write("Create and interact with AI agents.")

prompt = st.text_area("Define your AI agent: ", height=70, placeholder="Define how you want your model to behave...")

MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

provider = st.radio("Select Provider:", ("Groq", "OpenAI"))

if provider == "Groq":
    selected_model = st.selectbox("Select Groq Model:", MODEL_NAMES_GROQ)
elif provider == "OpenAI":
    selected_model = st.selectbox("Select OpenAI Model:", MODEL_NAMES_OPENAI)

allow_web_search = st.checkbox("Allow web search")

user_query = st.text_area("Enter your query: ", height=70, placeholder="Ask anything...")

# ===== Submit Query to Backend =====
if st.button("Ask agent"):
    if user_query.strip():
        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "prompt": prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            response_data = response.json()
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                st.subheader("Agent Response")
                st.markdown(f"Response: {response_data}")

    
        
