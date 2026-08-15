import streamlit as st
import google.generativeai as genai

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

    st.success("API Key Loaded")

    for m in genai.list_models():
        st.write(m.name)

except Exception as e:
    st.error(e)
