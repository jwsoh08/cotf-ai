import streamlit as st


def login_form():
    with st.form("Student login"):
        username = st.text_input("Username", max_chars=20)
        password = st.text_input("Password", type="password", max_chars=16)
        submit_button = st.form_submit_button("Login")
        if submit_button:
            if check_password(username, password):
                st.session_state.user = username
                return True
            else:
                st.error("Username and Password is incorrect")
                return False
    pass
