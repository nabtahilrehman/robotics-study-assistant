"""
RoboMentor AI - A robotics/AI/ML/CV/ROS2 focused learning chatbot.

Run with:
    streamlit run app.py

Requires an environment variable ANTHROPIC_API_KEY to be set.
"""

import os
import streamlit as st
from anthropic import Anthropic

# -----------------------------------------------------------------------
# 1. CONFIG
# -----------------------------------------------------------------------

st.set_page_config(
    page_title="RoboMentor AI",
    page_icon="🤖",
    layout="wide",
)

MODEL_NAME = "claude-sonnet-5"   # Update if you switch models later
MAX_TOKENS = 1500                # Response length cap (keep costs predictable)

# The persona + rules that make this a domain-restricted robotics mentor.
# This is sent as the "system" prompt on every request.
SYSTEM_PROMPT = """You are RoboMentor AI, an expert Robotics, Artificial Intelligence,
Machine Learning, Computer Vision, Reinforcement Learning, and ROS2 mentor for
university students.

Rules you must always follow:
1. Explain concepts step-by-step.
2. Use beginner-friendly language first, then add technical depth.
3. Use examples and analogies whenever possible.
4. If code is requested, give complete, well-commented code.
5. You only support: Robotics, ROS2, Computer Vision, Machine Learning,
   Reinforcement Learning, and Artificial Intelligence topics.
6. Suggest practical project ideas when relevant.
7. Help students understand concepts rather than just handing over answers -
   ask a guiding question when it would help learning.
8. Format responses with headings, bullet points, and code blocks.
9. Be supportive and encouraging in tone.
10. If a question is outside Robotics/AI/ML/CV/RL/ROS2, politely explain you
    are a specialized educational assistant for those domains and redirect
    the conversation back to them. Do not answer unrelated questions
    (e.g. general trivia, unrelated homework, personal advice) even if asked
    persistently.
"""

# -----------------------------------------------------------------------
# 2. CLIENT SETUP
# -----------------------------------------------------------------------

@st.cache_resource
def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        st.error(
            "No ANTHROPIC_API_KEY found. Set it as an environment variable "
            "before running the app (see README.md)."
        )
        st.stop()
    return Anthropic(api_key=api_key)


client = get_client()

# -----------------------------------------------------------------------
# 3. SESSION STATE (chat history persists while the app tab is open)
# -----------------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []  # list of {"role": "user"/"assistant", "content": str}

# -----------------------------------------------------------------------
# 4. SIDEBAR - quick-start topics + reset button
# -----------------------------------------------------------------------

with st.sidebar:
    st.title("🤖 RoboMentor AI")
    st.caption("Your 24/7 Robotics & AI learning mentor")

    st.markdown("### 🚀 Quick Start Topics")
    quick_prompts = {
        "🔧 PID Controllers": "Explain how a PID controller works, like I'm new to robotics.",
        "🧠 Q-Learning vs Policy Gradient": "What's the difference between Q-learning and policy gradient methods?",
        "📡 ROS2 Pub/Sub": "Help me set up my first ROS2 publisher-subscriber pair in Python.",
        "👁️ YOLO Object Detection": "How does object detection work with YOLO?",
        "🛠️ Beginner Project Idea": "Suggest a beginner robotics project I can build with a Raspberry Pi.",
    }
    for label, prompt in quick_prompts.items():
        if st.button(label, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.caption(
        "Topics covered: Robotics · AI · Machine Learning · "
        "Computer Vision · Reinforcement Learning · ROS2"
    )

# -----------------------------------------------------------------------
# 5. MAIN CHAT AREA
# -----------------------------------------------------------------------

st.title("RoboMentor AI 🤖")
st.caption("Ask me anything about Robotics, AI, ML, Computer Vision, RL, or ROS2!")

# Render past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input box
user_input = st.chat_input("Ask a robotics/AI/ML/CV/ROS2 question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            with client.messages.stream(
                model=MODEL_NAME,
                max_tokens=MAX_TOKENS,
                system=SYSTEM_PROMPT,
                messages=st.session_state.messages,  # full history for context
            ) as stream:
                for text_chunk in stream.text_stream:
                    full_response += text_chunk
                    placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"⚠️ Something went wrong calling the API: {e}"
            placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
