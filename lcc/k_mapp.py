import streamlit as st
from streamlit.components.v1 import html
import re
import openai
from openai import OpenAI


# For AWS Secrets
import json
import boto3
from botocore.exceptions import ClientError


class SecretsManager:
    @staticmethod
    def get_secret(key):
        secret_name = "cotf/streamlit/test"
        region_name = "ap-southeast-1"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)

        except ClientError as e:
            raise e

        secrets = json.loads(get_secret_value_response["SecretString"])
        return secrets[key]


def mermaid(code: str) -> None:
    html(
        f"""
        <pre class="mermaid">
            {code}
        </pre>

        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
        """,
        height=st.session_state["svg_height"] + 50,
    )


def extract_mermaid_syntax(text):
    # st.text(text)
    pattern = r"```\s*mermaid\s*([\s\S]*?)\s*```"
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    else:
        pattern = r"\*\(&\s*([\s\S]*?)\s*&\)\*"
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
        else:
            return "Mermaid syntax not found in the provided text."


def output_mermaid_diagram(mermaid_code):
    """
    Outputs the mermaid diagram in a Streamlit app.

    Args:
        mermaid_code (str): Mermaid code to be rendered.
    """

    if mermaid_code:
        mermaid(mermaid_code)
    else:
        st.error("Please type in a new topic or change the words of your topic again")
        return False


def generate_mindmap(prompt):
    try:
        client = OpenAI(api_key=SecretsManager.get_secret("openai_key"))

        response = client.chat.completions.create(
            model=st.session_state.openai_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=st.session_state.temp,  # settings option
            presence_penalty=st.session_state.presence_penalty,  # settings option
            frequency_penalty=st.session_state.frequency_penalty,  # settings option
        )

        if response["choices"][0]["message"]["content"] != None:
            msg = response["choices"][0]["message"]["content"]
            st.text(msg)

            extracted_code = extract_mermaid_syntax(msg)
            st.write(extracted_code)
            return extracted_code

    except openai.APIError as e:
        st.error(e)
        st.error("Please type in a new topic or change the words of your topic again")
        return False

    except Exception as e:
        st.error(e)
        st.error("Please type in a new topic or change the words of your topic again")
        return False
