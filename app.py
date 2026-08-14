import streamlit as st
import google.generativeai as genai

st.title("🤖 Robotics Study Assistant")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- Initialize the Model ---
model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    system_instruction=SYSTEM_PROMPT
)

question = st.text_input("Ask a Robotics or AI question")

if question:
    try:
        response = model.generate_content(question)
        st.write(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
