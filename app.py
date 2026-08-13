import streamlit as st

st.title("🤖 Robotics Study Assistant")

question = st.text_input("Ask a question")

if question:
    st.write("You asked:", question)
