import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Robotics Study Assistant", page_icon="🤖", layout="centered")

# 1. Connect to Google API
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("⚠️ API Key not found in Streamlit Secrets!")
    st.stop()

# 2. Hardcode the most stable free-tier model
MODEL_ID = "gemini-1.5-flash-latest"

SYSTEM_PROMPT = """
You are an expert, highly encouraging study assistant specializing in Robotics, AI, ML, Computer Vision, and ROS2. 
- Provide clear, step-by-step explanations and well-commented code blocks.
- Use analogies to explain difficult topics.
- If a question is outside of these fields, politely decline.
- Format responses using Markdown.
"""

try:
    model = genai.GenerativeModel(
        model_name=MODEL_ID,
        system_instruction=SYSTEM_PROMPT
    )
except Exception as e:
    st.error(f"Failed to initialize model. Error: {e}")
    st.stop()

# 3. Streamlit UI
st.title("🤖 Robotics Study Assistant")
st.caption(f"Powered by Google Gemini")

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Display Chat History
for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Handle Chat Input
prompt = st.chat_input("Ask a robotics or AI question...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
