import streamlit as st


def science_feedback():
    placeholder6 = st.empty()
    with placeholder6:
        with st.form("Metacognitive Feedback"):
            txt = st.text_area("Science text for analysis")
            submitted = st.form_submit_button("Submit Science text for feedback")
            if submitted:
                return txt


def reflective_peer():
    placeholder5 = st.empty()
    with placeholder5:
        with st.form("Reflective Peer"):
            txt = st.text_area("Reflection Text")
            submitted = st.form_submit_button("Submit Reflection Text")
            if submitted:
                return txt
