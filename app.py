import streamlit as st
from rag_pipeline import create_rag

st.title("AI Enterprise Knowledge Assistant")
st.write("App started successfully")

qa = create_rag()

question = st.text_input("Ask a question about company policies")

if question:
    result = qa.run(question)

    st.write("### Answer")
    st.write(result)

    st.write("### Source")
    st.write("Information retrieved from internal company documents.")
