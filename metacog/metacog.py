import streamlit as st


def science_feedback():
    placeholder6 = st.empty()

    with placeholder6:
        inputs = {}

        with st.form("Metacognitive Feedback"):
            question = st.text_input("Question")
            text = st.text_area("Text for analysis")

            submitted = st.form_submit_button("Submit text for feedback")

            if submitted:
                inputs["question"] = question
                inputs["text"] = text
                return inputs


def reflective_peer():
    placeholder5 = st.empty()

    with placeholder5:
        inputs = {}

        with st.form("Reflective Peer"):
            question = st.text_input("Reflective question")
            text = st.text_area("Reflection Text")
            
            submitted = st.form_submit_button("Submit Reflection Text")
            if submitted:
                inputs["question"] = question
                inputs["text"] = text
                return inputs
