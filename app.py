
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

# 2. Automatically Find a Working Model
try:
    models = genai.list_models()
    valid_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
except Exception as e:
    st.error(f"Failed to connect to Google. Error: {e}")
    st.stop()

if not valid_models:
    st.error("Your API key has access to 0 models. You must go to Google AI Studio and create a NEW API key.")
    st.stop()

# Pick the best model available
chosen_model = valid_models[0]
for pref in ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-1.0-pro"]:
    if pref in valid_models:
        chosen_model = pref
        break

# 3. System Instructions
SYSTEM_PROMPT = """
You are an expert, highly encouraging study assistant specializing in Robotics, AI, ML, Computer Vision, and ROS2. 
- Provide clear, step-by-step explanations and well-commented code blocks.
- Use analogies to explain difficult topics.
- If a question is outside of these fields, politely decline.
- Format responses using Markdown.
"""

# 4. Initialize Model
try:
    model = genai.GenerativeModel(
        model_name=chosen_model,
        system_instruction=SYSTEM_PROMPT
    )
except Exception as e:
    st.error(f"Failed to initialize model. Error: {e}")
    st.stop()

# 5. Streamlit UI
st.title("🤖 Robotics Study Assistant")
st.caption(f"Currently using model: `{chosen_model}`") # This shows us which model it picked

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
