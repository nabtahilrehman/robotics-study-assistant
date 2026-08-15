import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Robotics Study Assistant",
    page_icon="🤖",
)

st.title("🤖 Robotics Study Assistant")

st.markdown(
    """
Ask me about:

- Robotics
- AI
- Machine Learning
- Computer Vision
- ROS2
- Reinforcement Learning
"""
)

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

question = st.text_input(
    "Ask a Robotics or AI Question"
)

if question:

    prompt = f"""
    You are an expert Robotics and AI tutor.

    Explain concepts clearly and simply.

    Question:
    {question}
    """

    try:
        response = model.generate_content(prompt)

        st.markdown("### Answer")
        st.write(response.text)

    except Exception as e:
        st.error(f"Error: {e}")
