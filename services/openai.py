import os
import streamlit as st
from openai import OpenAI
from basecode.services.aws import SecretsManager

class OpenAIBase:
    """
    The API key supplied to the model would depend on
    which team is using the application.
    For example, if LCC team is using the LCC feature on
    the platform which is meant to serve them, then the 
    LCC API key would be used. Likewise for the metacog 
    team.
    """
    def __init__(self):
        if os.environ['PROTOTYPE'] == "LCC":
            if os.environ['ENVIRONMENT'] == "GCC":
                self.api_key = SecretsManager.get_secret("openai_key_lcc")
            else:
                self.api_key = st.secrets["openai_key_lcc"]

        elif os.environ['PROTOTYPE'] == "METACOG":
            if os.environ['ENVIRONMENT'] == "GCC":
                self.api_key = SecretsManager.get_secret("openai_key_metacog")
            else:
                self.api_key = st.secrets["openai_key_metacog"]


class ChatGPT(OpenAIBase):
    def chat_completions(self, messages, stream=True):

        client = OpenAI(api_key=self.api_key)
        completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
            stream=True,
        )

        return completion