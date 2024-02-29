import streamlit as st
import streamlit_antd_components as sac
import tempfile
import configparser
import os
from langchain.memory import ConversationBufferWindowMemory
from langchain.document_loaders import UnstructuredFileLoader
from basecode.users_module import vectorstore_selection_interface

import openai
from openai import OpenAI
from basecode.authenticate import return_api_key
from basecode.main_bot import insert_into_data_table

from datetime import datetime
from Markdown2docx import Markdown2docx

from lcc.k_mapp import generate_mindmap, output_mermaid_diagram

config = configparser.ConfigParser()
config.read("config.ini")

LESSON_COLLAB = config["constants"]["LESSON_COLLAB"]

from settings import SUBJECTS_LIST, EDUCATION_LEVELS

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=return_api_key(),
)


def commentator_rating():
    rating_value = sac.rate(
        label="Lesson Commentator Ratings:",
        position="left",
        clear=True,
        value=2.5,
        align="left",
        size=15,
        color="#25C3B0",
        half=True,
        key=1,
    )
    return rating_value


def generator_rating():
    rating_value = sac.rate(
        label="Lesson Generator Ratings:",
        position="left",
        clear=True,
        value=2.5,
        align="left",
        size=15,
        color="#25C3B0",
        half=True,
        key=2,
    )
    return rating_value


def metacog_bot(prompt, prompt_template, bot_name):
    try:
        prompt_question = prompt["question"]
        prompt_text = prompt["text"]

        if prompt:
            # st.write("I am inside", st.session_state.lesson_col_prompt)
            if "memory" not in st.session_state:
                st.session_state.memory = ConversationBufferWindowMemory(k=5)

            st.session_state.msg.append(
                {"role": "user", "content": "Question: " + prompt_question}
            )
            st.session_state.msg.append(
                {"role": "user", "content": "Text: " + prompt_text}
            )

            message_placeholder = st.empty()

            # check if there is any knowledge base
            if st.session_state.vs:
                docs = st.session_state.vs.similarity_search(
                    prompt_question + " " + prompt_text
                )
                resources = docs[0].page_content
                reference_prompt = f"""You may refer to this resources to improve or design the lesson
										{resources}
									"""
            else:
                reference_prompt = ""

            full_response = ""
            input_prompt = "question: " + prompt_question + ", text: " + prompt_text

            for response in template_prompt(
                input_prompt, reference_prompt + prompt_template
            ):
                full_response += response.choices[0].delta.content or ""
                message_placeholder.markdown(full_response + "▌")
            if bot_name == LESSON_COLLAB:
                feedback_value = generator_rating()
            else:
                feedback_value = commentator_rating()
            message_placeholder.markdown(full_response)
            st.session_state.msg.append({"role": "assistant", "content": full_response})
            st.session_state["memory"].save_context(
                {"input": input_prompt}, {"output": full_response}
            )
            # This is to send the lesson_plan to the lesson design map
            st.session_state.lesson_plan = full_response
            # Insert data into the table
            now = datetime.now()  # Using ISO format for date
            num_tokens = len(full_response + prompt_question + prompt_text) * 1.3
            # st.write(num_tokens)
            insert_into_data_table(
                now.strftime("%d/%m/%Y %H:%M:%S"),
                full_response,
                input_prompt,
                num_tokens,
                bot_name,
                feedback_value,
            )
            st.session_state.data_doc = (
                st.session_state.data_doc + "\n\n" + full_response
            )
            md_filename = "lp" + st.session_state.user["username"] + ".md"
            md_filepath = os.path.join("lesson_plan", md_filename)
            if not os.path.exists("lesson_plan"):
                os.makedirs("lesson_plan")
            with open(md_filepath, "w", encoding="utf-8") as file:
                file.write(full_response)
            # Convert the markdown file to a docx
            base_filepath = os.path.join(
                "lesson_plan", "lp" + st.session_state.user["username"]
            )
            project = Markdown2docx(base_filepath)
            project.eat_soup()
            project.save()  # Assuming it saves the file with the same name but a .docx extension
            st.session_state.generated_flag = True

    except Exception as e:
        st.error(e)


def lesson_bot(prompt, prompt_template, bot_name):
    try:
        # prompt_question = prompt['question']
        # prompt_text = prompt['text']

        if prompt:
            # st.write("I am inside", st.session_state.lesson_col_prompt)
            if "memory" not in st.session_state:
                st.session_state.memory = ConversationBufferWindowMemory(k=5)

            st.session_state.msg.append({"role": "user", "content": "input: " + prompt})

            message_placeholder = st.empty()

            # check if there is any knowledge base
            if st.session_state.vs:
                docs = st.session_state.vs.similarity_search(prompt)
                resources = docs[0].page_content
                reference_prompt = f"""You may refer to this resources to improve or design the lesson
										{resources}
									"""
            else:
                reference_prompt = ""

            full_response = ""

            for response in template_prompt(prompt, reference_prompt + prompt_template):
                full_response += response.choices[0].delta.content or ""
                message_placeholder.markdown(full_response + "▌")
            if bot_name == LESSON_COLLAB:
                feedback_value = generator_rating()
            else:
                feedback_value = commentator_rating()
            message_placeholder.markdown(full_response)
            st.session_state.msg.append({"role": "assistant", "content": full_response})
            st.session_state["memory"].save_context(
                {"input": prompt}, {"output": full_response}
            )
            # This is to send the lesson_plan to the lesson design map
            st.session_state.lesson_plan = full_response
            # Insert data into the table
            now = datetime.now()  # Using ISO format for date
            num_tokens = len(full_response + prompt) * 1.3
            # st.write(num_tokens)
            insert_into_data_table(
                now.strftime("%d/%m/%Y %H:%M:%S"),
                full_response,
                prompt,
                num_tokens,
                bot_name,
                feedback_value,
            )
            st.session_state.data_doc = (
                st.session_state.data_doc + "\n\n" + full_response
            )
            md_filename = "lp" + st.session_state.user["username"] + ".md"
            md_filepath = os.path.join("lesson_plan", md_filename)
            if not os.path.exists("lesson_plan"):
                os.makedirs("lesson_plan")
            with open(md_filepath, "w", encoding="utf-8") as file:
                file.write(full_response)
            # Convert the markdown file to a docx
            base_filepath = os.path.join(
                "lesson_plan", "lp" + st.session_state.user["username"]
            )
            project = Markdown2docx(base_filepath)
            project.eat_soup()
            project.save()  # Assuming it saves the file with the same name but a .docx extension
            st.session_state.generated_flag = True

    except Exception as e:
        st.error(e)


def template_prompt(prompt, prompt_template):
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key=return_api_key(),
    )
    openai.api_key = return_api_key()
    os.environ["OPENAI_API_KEY"] = return_api_key()

    response = client.chat.completions.create(
        model=st.session_state.openai_model,
        messages=[
            {"role": "system", "content": prompt_template},
            {"role": "user", "content": prompt},
        ],
        temperature=st.session_state.temp,  # settings option
        stream=True,  # settings option
    )

    return response


def lesson_collaborator():
    st.subheader("1. Basic Lesson Information for Generator")
    subject = st.selectbox("Choose a Subject", SUBJECTS_LIST)
    level = st.selectbox("Grade Level", EDUCATION_LEVELS)
    duration = st.text_input(
        "Duration (in minutes)",
        help="Estimated duration of one lesson or over a few lessons",
    )

    st.subheader("2. Lesson Details for Generator")
    topic = st.text_area(
        "Topic", help="Describe the specific topic or theme for the lesson"
    )
    skill_level = st.text_input(
        "Readiness Level", help="Beginner, Intermediate, Advanced ..."
    )

    st.subheader("3. Learners Information for Generator")
    prior_knowledge = st.text_area("Prior Knowledge")
    learners_info = st.text_input("Describe the learners for this lesson")

    st.subheader("4. Skills Application")
    kat_options = [
        "Support Assessment for Learning",
        "Foster Conceptual Change",
        "Provide Differentiation",
        "Facilitate Learning Together",
        "Develop Metacognition",
        "Enable Personalisation",
        "Scaffold the learning",
    ]
    kat = st.multiselect(
        "Which Key Application of Technology (KAT) is your lesson focused on?",
        kat_options,
    )
    cc_21 = ""
    incorporate_elements = ""
    if st.checkbox(
        "I would like to incorporate 21CC (including New Media Literacies) in my lesson"
    ):
        cc_21 = st.text_input(
            "What are the 21CC (including New Media Literacies) that are important for my students to develop? "
        )
    if st.checkbox(
        "I would like to incorporate certain lesson elements in my lesson plan"
    ):

        st.subheader("5. Lesson Structure")
        incorporate_elements = st.text_area(
            "Incoporate lesson elements (e.g. lesson should be fun and include pair work)",
            help="Describe lesson elements that you would like to have",
        )

    st.write(st.session_state.lesson_col_option)
    vectorstore_selection_interface(st.session_state.user["id"])

    st.session_state.lesson_col_option = sac.buttons(
        [
            sac.ButtonsItem(
                label="Generate",
                icon="check-circle-fill",
                color="green",
                disabled=st.session_state.generated_flag,
            ),
            sac.ButtonsItem(
                label=st.session_state.button_text, icon="x-circle-fill", color="red"
            ),
        ],
        label=None,
        index=1,
        format_func="title",
        align="center",
        position="top",
        size="default",
        direction="horizontal",
        shape="round",
        type="default",
        compact=False,
    )

    if st.session_state.lesson_col_option == "Generate":
        lesson_prompt = f"""Help me design a lesson on this information
							Subject: {subject}
							Topic: {topic}
							Grade Level: {level}
							Duration: {duration} minutes
							Readiness Level: {skill_level}
							Description of Learners: {learners_info}
							Student's prior knowledge: {prior_knowledge}
							Key Application of Technology (KAT): {kat}"""
        if cc_21 != "":
            lesson_prompt + f"""21CC (including New Media Literacies): {cc_21}"""
        if incorporate_elements != "":
            (
                lesson_prompt
                + f"""Incorporate the following lesson elements (if any): {incorporate_elements}"""
            )

        st.success("Your lesson generation information has been submitted!")

        return lesson_prompt
    elif (
        st.session_state.lesson_col_option == "Cancel"
        or st.session_state.lesson_col_option == "Reset"
    ):
        st.session_state.generated_flag = False
        st.session_state.button_text = "Cancel"
        return False


def lesson_design_options():
    docx_name = "lp" + st.session_state.user["username"] + ".docx"
    docx_path = os.path.join("lesson_plan", docx_name)

    if os.path.exists(docx_path):
        # Provide the docx for download via Streamlit
        with open(docx_path, "rb") as docx_file:
            docx_bytes = docx_file.read()
            st.success("File is ready for downloading")
            st.download_button(
                label="Download document as DOCX",
                data=docx_bytes,
                file_name=docx_name,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        os.remove(docx_path)
        st.session_state.button_text = "Reset"
    else:
        st.warning("There is no lesson plan available for download.")


# direct load into form
def upload_lesson_plan():
    def get_file_extension(file_name):
        return os.path.splitext(file_name)[1]

    # Streamlit file uploader to accept file input
    uploaded_file = st.file_uploader(
        "Upload a lesson plan file", type=["docx", "txt", "pdf"]
    )

    if uploaded_file:
        # Reading file content
        file_content = uploaded_file.read()

        # Determine the suffix based on uploaded file's name
        file_suffix = get_file_extension(uploaded_file.name)

        # Saving the uploaded file temporarily to process it
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as temp_file:
            temp_file.write(file_content)
            temp_file.flush()  # Ensure the data is written to the file
            temp_file_path = temp_file.name

        # Process the temporary file using UnstructuredFileLoader (or any other method you need)
        # st.write(temp_file_path)
        loader = UnstructuredFileLoader(temp_file_path)
        docs = loader.load()

        st.success("File processed and added to form")

        # Removing the temporary file after processing
        os.remove(temp_file_path)
        return docs


def count_words(text):
    return len(text)


def lesson_design_map(lesson_plan):
    """
    Generates a prompt based on a response from a chatbot for Mermaid diagram.

    Args:
            bot_response (str): Response from a chatbot over a topic.
    Returns:
            str: Generated prompt
    """

    prompt = f"""Given the lesson plan that is provided below: '{lesson_plan}', 
				 You must generate a git diagram using the Mermaid JS syntax with reference to the lesson plan above.
				 You will need to have one main branch and create 4 branches
				 Each new branch is called individual, group, class or community.
				 For each of the activities in the lesson plan, you must determine how the activity is focused on the individual, group, class or community.
				 You must create a path that maps the activities to the branches in a linear order such that each activity is mapped to one of the 4 branches.
				 The main branch is the start lesson branch
				 For each activity, you must create three commmit id for each activity.The first commit id is the activity name.
				 The second commit is the lesson brief details in 3 words and the last commit is the tool used for the activity.
				 Here is an example on how a lesson plan is mapped to a git diagram.
				 %%{{init: {{ 'logLevel': 'debug', 'theme': 'base', 'gitGraph': {{'showBranches': true, 'showCommitLabel':true,'mainBranchName': "Class Start"}}}} }}%%
					gitGraph
						commit id: "Objective 1"
						commit id: "Objective 2"
						commit id: "Objective 3"
						branch Class
						commit id: "1.Activity"
						commit id: "1.Lesson Detail"
						commit id: "1.Tools"
						branch Group
						commit id: "2.Activity"
						commit id: "2.Lesson Detail"
						commit id: "2.Tools"
						branch Individual
						checkout Individual
						commit id: "3.Activity"
						commit id: "3.Lesson Detail"
						commit id: "3.Tools"
						checkout Class
						merge Individual
						commit id: "4.Activity"
						commit id: "4.Lesson Detail"
						commit id: "4.Tools"
						branch Community
						checkout Community
						commit id: "5.Activity"
						commit id: "5.Lesson Detail"
						commit id: "5.Tools"
						checkout Individual
						merge Community
						commit id: "6.Activity"
						commit id: "6.Lesson Detail"
						commit id: "6.Tools"
				You must use the init setting of the syntax to set the gitgraph
				You must remove the extra "{" and "}" in the syntax below.
				You must create a new flow mermaid syntax based on the given syntax example to suit the lesson plan.
				You must output the mermaid syntax between these special brackets with * and &: *(& MERMAID SYNTAX &)*"""

    return prompt


def lesson_map_generator():
    try:
        with st.form("Lesson Map"):
            st.subheader("Lesson Map Generator")
            st.write(
                "Please input or edit the lesson plan below from the lesson generator"
            )
            lesson_plan = st.text_area(
                "Lesson Plan", height=500, value=st.session_state.lesson_plan
            )
            submit = st.form_submit_button("Generate Lesson Map")
            if submit:
                with st.status("Generating Lesson Map"):
                    diagram_prompt = lesson_design_map(lesson_plan)
                    syntax = generate_mindmap(diagram_prompt)
                if syntax:
                    output_mermaid_diagram(syntax)
                    st.success("Lesson Map Generated!")

    except Exception as e:
        st.error(e)
