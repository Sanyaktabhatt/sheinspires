import streamlit as st
from rag_pipeline import create_rag
from conflict_detector import detect_conflict
import json


uploaded_files = st.file_uploader(
    "Upload company documents",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    for file in uploaded_files:

        save_path = f"uploads/{file.name}"

        with open(save_path, "wb") as f:
            f.write(file.getbuffer())

        st.success(f"{file.name} uploaded successfully")
st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="🤖",
    layout="centered"
)

def find_people_with_skill(skill):

    with open("employees.json") as f:
        employees = json.load(f)

    matches = []

    for emp in employees:

        if skill.lower() in [s.lower() for s in emp["skills"]]:
            matches.append(emp["name"])

    return matches

st.title("🤖 AI Enterprise Knowledge Assistant")

st.write("Ask questions about internal company policies.")

qa = create_rag()

question = st.text_input("Ask a question about company policies")

if st.button("Ask AI"):

    if not question:
        st.warning("Please enter a question.")
        st.stop()


    if "who knows" in question.lower():

        skill = question.lower().replace("who knows", "").strip()

        people = find_people_with_skill(skill)

        st.markdown("## 👨‍💻 Employees with this skill")

        if people:
            for p in people:
                st.write("•", p)
        else:
            st.write("No employees found with that skill.")

        st.stop()   


    with st.spinner("Searching company knowledge base..."):

        result = qa.invoke({"query": question})

    answer = result["result"]
    sources = result["source_documents"]

    st.markdown("## 📌 Answer")
    st.write(answer)

    st.markdown("## 📄 Source Documents")

    texts = []

    for doc in sources:

        texts.append(doc.page_content)

        with st.expander(f"Source: {doc.metadata['source']}"):
            st.write(doc.page_content)

    if detect_conflict(texts):
        st.warning("⚠ Conflicting information detected in documents")

        st.markdown("## Feedback")

        col1, col2 = st.columns(2)

        if col1.button("Helpful 👍"):
            st.success("Thanks for your feedback!")

        if col2.button("Incorrect 👎"):
            st.error("We'll review this response.")