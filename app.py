import streamlit as st
import google.generativeai as genai

st.title("🤖 Robotics Study Assistant")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

question = st.text_input("Ask a Robotics or AI question")

if question:
    response = model.generate_content(
        f"You are a robotics tutor. Answer this question simply: {question}"
    )

    st.write(response.text)
