import streamlit as st

if "GEMINI_API_KEY" in st.secrets:
    st.success("✅ Secret detected")
else:
    st.error("❌ Secret not found")
