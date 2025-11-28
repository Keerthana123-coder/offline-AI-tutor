import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import warnings
import requests
import json

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="AI Tutor  Chatbot",
    page_icon="🤖", 
    layout="centered", 
    initial_sidebar_state="collapsed")
    

SYSTEM_PROMPT = """
You are an AI tutor specializing in Mathematics and Science.

RULES:
1. For math expressions such as:
   - 2+3
   - 10*(5-2)
   - (4^2) + 6 / 3
   ALWAYS answer ONLY with the final numeric answer. No words.

2. Do NOT explain math unless the user asks:
   - explain
   - why
   - show steps

3. For science questions (physics, chemistry, biology, astronomy):
   - Provide short, clear, accurate answers.
   - No long paragraphs.
   - No philosophical or random text.

4. If user asks "explain deeply", then give a longer explanation.

5. If the question is unclear, ask for clarification.
"""

st.markdown("""
<style>
/* Full page dark background */
[data-testid="stAppViewContainer"] {
    background: #E6F0FA;
    color: #1A1A1A;
}
/* Full page background including margins */
[data-testid="stAppContent"] {
    background-color: #E6F0FA;
}
            
            /* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #D9E6F6;  /* Slightly different shade for contrast */
}
            
/* Chat container wider and centered */
.css-1lcbmhc {
    max-width: 900px;
    margin: auto;
    padding: 20px;
}
  .chatbot-title {
    position: sticky;
    top: 0;
    background-color: #E6F0FA;
    padding: 15px 20px;
    font-size: 28px;
    font-weight: bold;
    border-bottom: 1px solid #cbd5e1;
    z-index: 100;
}          

/* Chat bubbles */
.stChatMessage {
    border-radius: 20px;
    padding: 20px 25px;
    margin: 10px 0;
    font-size: 25px;
    line-height: 1.6;
}

/* User messages */
.stChatMessage .user {
    background-color: #3b82f6;
    color: white;
}

/* AI messages */
.stChatMessage .assistant {
    background-color: #374151;
    color: #f3f4f6;
}

/* Chat input box */
.css-1kyxreq {
    background-color: #1f2937;   /* Dark input background */
    border-radius: 30px;
    padding: 12px 20px;          /* Padding inside input */
    font-size: 18px;
    color: #f3f4f6;              /* Light text */
    border: none;                /* Remove default border */
}

/* Placeholder text color */
.css-1kyxreq::placeholder {
    color: #9ca3af;              /* Light gray placeholder */
}
</style>
""", unsafe_allow_html=True)



st.markdown(
    """
    <h1 style="text-align:center; color:#3b82f6; font-size:60px; position:sticky">
        🤖 Offline AI Tutor📘
    </h1>
    <p style="text-align:center; font-size:28px; color:gray;">
        Math + Science • 100% Offline 
    </p>
    <hr style="margin-top:10px; margin-bottom:20px;">
    """,
    unsafe_allow_html=True
)

# -------------------------
#     INSTRUCTIONS BOX
# -------------------------
with st.expander("ℹ️ Instructions", expanded=False):
    st.markdown(
        """
        **You can ask:**
        - Math calculations → `2+3`, `10*(5-2)`
        - Math steps → `explain 25*4`
        - Physics → `why sky is blue?`
        - Chemistry → `what is pH?`
        - Biology → `function of mitochondria`
        - Astronomy → `what is a black hole?`

        **Math rule:**  
        → If you enter only numbers/equations, bot gives only the final answer.

        **Offline:**  
        → Works without internet using Ollama.
        ** General Rules **
            - Works 100% offline using Ollama.
            - Ask only one question at a time for best results.
            - For long, complex answers, mention:
       - **"I want a long explanation"**
       - **"Explain step-by-step"**
        """
    )

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"   # Or use "llama3.2:1b" for low-end PCs




def ask_ollama(question):
    """Send prompt to Ollama locally"""
    payload = {
        "model": MODEL_NAME,
        "prompt": SYSTEM_PROMPT + "\nUser: " + question+ "\nAI:",
        "stream": False
    }
    try:
        result = requests.post(OLLAMA_URL, json=payload, timeout=60)
        
        data = result.json()
       
            
        if "result" in data:
            return data["result"].strip()
        elif "done" in data and "response" in data:
            return data["response"].strip()

        # Print full JSON if unexpected
        else:
            return f"❌ Unexpected Ollama format:\n{data}"

    except Exception as e:
        return f"❌ Error: {e}"


if "chat" not in st.session_state:
    st.session_state.chat = []

# Display past messages
for role, content in st.session_state.chat:
    with st.chat_message(role):
        st.write(content)

# User input box
user_input = st.chat_input("Ask a math or science question...")

if user_input:
    # Save user message
    st.session_state.chat.append(("user", user_input))
    with st.chat_message("user"):
        st.write(user_input)

    # Generate answer
    with st.chat_message("assistant"):
        reply = ask_ollama(user_input)
        st.session_state.chat.append(("assistant", reply))
        st.write(reply)
        with st.expander("ℹ️ Instructions", expanded=False):
            st.markdown(
        """
        **You can ask:**
        - Math calculations → `2+3`, `10*(5-2)`
        - Math steps → `explain 25*4`
        - Physics → `why sky is blue?`
        - Chemistry → `what is pH?`
        - Biology → `function of mitochondria`
        - Astronomy → `what is a black hole?`

        **Math rule:**  
        → If you enter only numbers/equations, bot gives only the final answer.

        **Offline:**  
        → Works without internet using Ollama.
        ** General Rules **
            - Works 100% offline using Ollama.
            - Ask only one question at a time for best results.
            - For long, complex answers, mention:
       - **"I want a long explanation"**
       - **"Explain step-by-step"**
        """
    )
    st.markdown(
    """
    <div style="
        text-align:center; 
        margin-top:40px; 
        padding-top:10px;
        color:#3b82f6;
        font-size:16px;
        font-weight:600;
    ">
        Made with ❤️ • Offline AI Tutor
    </div>
    <div style="
        text-align:center; 
        color:gray;
        font-size:13px;
    ">
        Powered locally by <b>Ollama</b> + <b>Llama 3</b>
    </div>
    """,
    unsafe_allow_html=True
)

    st.rerun()

