import streamlit as st
import google.generativeai as genai

st.title("🤖 Robotics Study Assistant")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

try:
    model = genai.GenerativeModel("gemini-pro")

    question = st.text_input("Ask a question")

    if question:
        response = model.generate_content(question)
        st.write(response.text)

except Exception as e:
    st.error(str(e))
