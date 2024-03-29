import streamlit as st
import hashlib

# from st_files_connection import FilesConnection
import sqlite3
import os
import configparser
import os
import ast


from services.aws import SecretsManager


class ConfigHandler:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

    def get_value(self, section, key):
        value = self.config.get(section, key)
        try:
            # Convert string value to a Python data structure
            return ast.literal_eval(value)
        except (SyntaxError, ValueError):
            # If not a data structure, return the plain string
            return value


# Initialization
config_handler = ConfigHandler()
COTF = config_handler.get_value("constants", "COTF")
META = config_handler.get_value("constants", "META")
PANDAI = config_handler.get_value("constants", "PANDAI")

# Create or check for the 'database' directory in the current working directory
cwd = os.getcwd()
WORKING_DIRECTORY = os.path.join(cwd, "database")

if not os.path.exists(WORKING_DIRECTORY):
    os.makedirs(WORKING_DIRECTORY)


# Check application environment => GCC or Streamlit
ENV = config_handler.get_value("constants", "prototype_env")

if ENV == "GCC":
    if SecretsManager.get_secret("sql_ext_path") == "None":
        WORKING_DATABASE = os.path.join(
            WORKING_DIRECTORY, SecretsManager.get_secret("default_db")
        )
    else:
        WORKING_DATABASE = SecretsManager.get_secret("sql_ext_path")
else:
    if st.secrets["sql_ext_path"] == "None":
        WORKING_DATABASE = os.path.join(WORKING_DIRECTORY, st.secrets["default_db"])
    else:
        WORKING_DATABASE = st.secrets["sql_ext_path"]


def login_function():
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


# can consider bycrypt if need to upgrade higher security


def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(username, password):
    """Checks if the password matches the stored password."""
    hashed_password = hash_password(password)
    conn = sqlite3.connect(WORKING_DATABASE)
    # conn = st.experimental_connection('s3', type=FilesConnection)
    cursor = conn.cursor()

    # Fetch only the password for the given username
    cursor.execute("SELECT password FROM Users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    # Check if the result exists and the hashed password matches the stored password
    if result and hashed_password == result[0]:
        return True
    else:
        return False


def return_api_key():

    if ENV == "GCC":
        # initial value of API KEY
        if "option" not in st.session_state:
            return SecretsManager.get_secret("openai_key_lcc")

        if (
            st.session_state.option == "Lesson Collaborator (Chatbot)"
            or st.session_state.option == "Lesson Collaborator (Scaffolded)"
            or st.session_state.option == "Lesson Commentator"
            or st.session_state.option == "Lesson Designer Map"
        ):
            return SecretsManager.get_secret("openai_key_lcc")
        elif (
            st.session_state.option == "Metacognitive Feedback"
            or st.session_state.option == "Reflective Peer"
            or st.session_state.option == "Thinking Facilitator (Chatbot)"
        ):
            return SecretsManager.get_secret("openai_key_metacog")
        else:
            return SecretsManager.get_secret("openai_key_lcc")
    else:
        # initial value of API KEY
        if "option" not in st.session_state:
            return st.secrets["openai_key_lcc"]

        if (
            st.session_state.option == "Lesson Collaborator (Chatbot)"
            or st.session_state.option == "Lesson Collaborator (Scaffolded)"
            or st.session_state.option == "Lesson Commentator"
            or st.session_state.option == "Lesson Designer Map"
        ):
            return st.secrets["openai_key_lcc"]
        elif (
            st.session_state.option == "Metacognitive Feedback"
            or st.session_state.option == "Reflective Peer"
            or st.session_state.option == "Thinking Facilitator (Chatbot)"
        ):
            return st.secrets["openai_key_metacog"]
        else:
            return st.secrets["openai_key_lcc"]
