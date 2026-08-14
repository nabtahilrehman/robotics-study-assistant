import streamlit as st
import google.generativeai as genai

# --- Page Configuration ---
st.set_page_config(page_title="Robotics Study Assistant", page_icon="🤖", layout="centered")

# --- System Prompt (The Brain of the Assistant) ---
SYSTEM_PROMPT = """
You are an expert, highly encouraging study assistant specializing in Robotics, Artificial Intelligence, 
Machine Learning, Computer Vision, and ROS2. 

Your goal is to help university students understand complex concepts easily.
- Provide clear, step-by-step explanations.
- If a student asks for code (especially in ROS2, Python, or C++), always provide well-commented code blocks.
- Use analogies to explain difficult topics (e.g., compare neural networks to human brain cells).
- If a question is completely outside of Robotics, AI, ML, CV, or ROS2, politely decline and remind the user 
  that you are a specialized robotics tutor.
- Format your responses using Markdown (bullet points, bold text, code blocks) for readability.
"""

# --- API Key Handling ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("⚠️ API Key not found! Please add GEMINI_API_KEY to your .streamlit/secrets.toml file.")
    st.stop()

# --- Initialize the Model ---
model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    system_instruction=SYSTEM_PROMPT
)

# --- Initialize Chat Session ---
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- UI Design ---
st.title("🤖 Robotics Study Assistant")
st.markdown("Your AI tutor for **Robotics, AI, ML, Computer Vision, and ROS2**. Ask me anything!")

# Sidebar with quick suggestions
with st.sidebar:
    st.header("Quick Prompts")
    if st.button("Explain YOLOv8"):
        st.session_state.pending_prompt = "Can you explain how YOLOv8 works for object detection in simple terms?"
    if st.button("ROS2 Basics"):
        st.session_state.pending_prompt = "What is the difference between a Node and a Topic in ROS2?"
    if st.button("CNN vs ANN"):
        st.session_state.pending_prompt = "Why are Convolutional Neural Networks (CNNs) better for Computer Vision than standard ANNs?"
    if st.button("Reinforcement Learning"):
        st.session_state.pending_prompt = "Explain the concept of Q-learning in Reinforcement Learning."
    
    st.divider()
    st.write("Built by Nabtahil Rehman")

# Display Chat History
for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Handle Chat Input
prompt = st.chat_input("Ask your robotics or AI question...")

# Check if a quick prompt button was clicked
if "pending_prompt" in st.session_state:
    prompt = st.session_state.pending_prompt
    del st.session_state.pending_prompt # Clear it so it doesn't loop

if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
