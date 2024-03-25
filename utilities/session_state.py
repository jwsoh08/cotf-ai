import os
import streamlit as st

from services.aws import SecretsManager
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

ENV = config["constants"]["prototype_env"]


from settings import FUNC_DESCRIPTIONS


def initialise_session_state():
    if "title_page" not in st.session_state:
        st.session_state.title_page = "GenAI Workshop Framework V2"

    if "option" not in st.session_state:
        st.session_state.option = False

    if "api_key" not in st.session_state:
        st.session_state.api_key = ""

    if "login" not in st.session_state:
        st.session_state.login = False

    if "user" not in st.session_state:
        st.session_state.user = None

    if "start" not in st.session_state:
        st.session_state.start = 0

    if "openai_model" not in st.session_state:
        if ENV == "GCC":
            st.session_state.openai_model = SecretsManager.get_secret("default_model")
        else:
            st.session_state.openai_model = st.secrets["default_model"]

    if "msg" not in st.session_state:
        st.session_state.msg = []

    if "rating" not in st.session_state:
        st.session_state.rating = False

    if "lesson_plan" not in st.session_state:
        st.session_state.lesson_plan = ""

    if "temp" not in st.session_state:
        if ENV == "GCC":
            st.session_state.temp = int(SecretsManager.get_secret("default_temp"))
        else:
            st.session_state.temp = st.secrets["default_temp"]

    if "acknowledgement" not in st.session_state:
        st.session_state.acknowledgement = False

    if "frequency_penalty" not in st.session_state:
        if ENV == "GCC":
            st.session_state.frequency_penalty = int(
                SecretsManager.get_secret("default_frequency_penalty")
            )
        else:
            st.session_state.frequency_penalty = st.secrets["default_frequency_penalty"]

    if "presence_penalty" not in st.session_state:
        if ENV == "GCC":
            st.session_state.presence_penalty = int(
                SecretsManager.get_secret("default_presence_penalty")
            )
        else:
            st.session_state.presence_penalty = st.secrets["default_presence_penalty"]

    if "k_memory" not in st.session_state:
        if ENV == "GCC":
            st.session_state.k_memory = int(
                SecretsManager.get_secret("default_k_memory")
            )
        else:
            st.session_state.k_memory = st.secrets["default_k_memory"]

    if "memoryless" not in st.session_state:
        st.session_state.memoryless = False

    if "vs" not in st.session_state:
        st.session_state.vs = False

    if "visuals" not in st.session_state:
        st.session_state.visuals = False

    if "svg_height" not in st.session_state:
        st.session_state["svg_height"] = 1000

    if "current_model" not in st.session_state:
        st.session_state.current_model = "No KB loaded"

    if "func_options" not in st.session_state:
        st.session_state.func_options = {key: True for key in FUNC_DESCRIPTIONS.keys()}

    if "tools" not in st.session_state:
        st.session_state.tools = []

    if "lesson_col_prompt" not in st.session_state:
        st.session_state.lesson_col_prompt = False

    if "lesson_col_option" not in st.session_state:
        st.session_state.lesson_col_option = "Cancel"

    if "generated_flag" not in st.session_state:
        st.session_state.generated_flag = False

    if "button_text" not in st.session_state:
        st.session_state.button_text = "Cancel"

    if "data_doc" not in st.session_state:
        st.session_state.data_doc = ""

    if "download_response_flag" not in st.session_state:
        st.session_state.download_response_flag = False

    if "chatbot_index" not in st.session_state:
        st.session_state.chatbot_index = 1

    if "chat_response" not in st.session_state:
        st.session_state.chat_response = ""
