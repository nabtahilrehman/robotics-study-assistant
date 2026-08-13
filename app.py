import streamlit as st
import google.generativeai as genai

st.title("🤖 Robotics Study Assistant")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash-001")

question = st.text_input("Ask a Robotics or AI question")

if question:
    try:
        response = model.generate_content(question)
        st.write(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
