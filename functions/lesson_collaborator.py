import streamlit as st
import streamlit_antd_components as sac

from basecode.users_module import vectorstore_selection_interface
from basecode.main_bot import (
    clear_session_states,
    complete_my_lesson,
    search_bot,
    basebot_qa,
    basebot_qa_memory,
    basebot,
    basebot_memory,
)

from settings import LESSON_BOT


def lesson_collaborator_chatbot():
    st.subheader(f":green[{st.session_state.option}]")
    choice = sac.buttons(
        [
            sac.ButtonsItem(
                label="Collaborator Mode", icon="person-hearts", color="green"
            ),
            sac.ButtonsItem(label="Default", icon="person-fill", color="blue"),
            sac.ButtonsItem(
                label="Commentator Mode", icon="person-plus-fill", color="red"
            ),
        ],
        index=st.session_state.chatbot_index,
        format_func="title",
        align="center",
        size="small",
        type="default",
    )
    sac.divider(
        label="Chabot Settings",
        icon="robot",
        align="center",
    )

    # st.session_state.chatbot are prompt designs that are configured in config.ini
    if choice == "Collaborator Mode":
        st.session_state.chatbot = st.session_state.collaborator_mode
    elif choice == "Default Chatbot":  # remove the chatbot template
        st.session_state.chatbot = st.session_state.lesson_default
    elif choice == "Commentator Mode":
        st.session_state.chatbot = st.session_state.commentator_mode

    # check if API key is entered
    with st.expander("Lesson Designer Settings"):
        vectorstore_selection_interface(st.session_state.user["id"])
        # new options --------------------------------------------------------
        if st.session_state.vs:
            vs_flag = False
        else:
            vs_flag = True

        options = sac.chip(
            items=[
                sac.ChipItem(label="Raw Search", icon="search", disabled=vs_flag),
                sac.ChipItem(label="Enable Memory", icon="memory"),
                sac.ChipItem(label="Capture Responses", icon="camera-fill"),
                sac.ChipItem(label="Download Responses", icon="download"),
            ],
            index=[1, 2],
            format_func="title",
            radius="sm",
            size="sm",
            align="left",
            variant="light",
            multiple=True,
        )
        # Update state based on new chip selections
        raw_search = "Raw Search" in options
        st.session_state.memoryless = "Enable Memory" not in options
        st.session_state.rating = "Rating Function" in options
        st.session_state.download_response_flag = "Capture Responses" in options
        preview_download_response = "Download Responses" in options

        clear = sac.switch(
            label="Clear Chat", value=False, align="start", position="left"
        )
        if clear == True:
            clear_session_states()
        if preview_download_response:
            complete_my_lesson()

    if st.session_state.vs:  # chatbot with knowledge base
        if raw_search == True:
            search_bot()
        else:
            if st.session_state.memoryless:
                # memoryless chatbot with knowledge base but no memory
                basebot_qa(LESSON_BOT)
            else:
                # chatbot with knowledge base and memory
                basebot_qa_memory(LESSON_BOT)
    else:  # chatbot with no knowledge base
        if st.session_state.memoryless:
            # memoryless chatbot with no knowledge base and no memory
            basebot(LESSON_BOT)
        else:
            # chatbot with no knowledge base but with memory
            basebot_memory(LESSON_BOT)


def lesson_collaborator_scaffolded():
    st.session_state.start = 4
    st.subheader(f":green[{st.session_state.option}]")

    # st.subheader("1. Basic Lesson Information for Generator")
    # subject = st.selectbox("Choose a Subject", SUBJECTS_LIST)
    # level = st.selectbox("Grade Level", EDUCATION_LEVELS)
    # duration = st.text_input(
    #     "Duration (in minutes)",
    #     help="Estimated duration of one lesson or over a few lessons",
    # )

    # st.subheader("2. Lesson Details for Generator")
    # topic = st.text_area(
    #     "Topic", help="Describe the specific topic or theme for the lesson"
    # )
    # skill_level = st.text_input(
    #     "Readiness Level", help="Beginner, Intermediate, Advanced ..."
    # )

    # st.subheader("3. Learners Information for Generator")
    # prior_knowledge = st.text_area("Prior Knowledge")
    # learners_info = st.text_input("Describe the learners for this lesson")

    # st.subheader("4. Skills Application")
    # kat_options = [
    #     "Support Assessment for Learning",
    #     "Foster Conceptual Change",
    #     "Provide Differentiation",
    #     "Facilitate Learning Together",
    #     "Develop Metacognition",
    #     "Enable Personalisation",
    #     "Scaffold the learning",
    # ]
    # kat = st.multiselect(
    #     "Which Key Application of Technology (KAT) is your lesson focused on?",
    #     kat_options,
    # )
    # cc_21 = ""
    # incorporate_elements = ""
    # if st.checkbox(
    #     "I would like to incorporate 21CC (including New Media Literacies) in my lesson"
    # ):
    #     cc_21 = st.text_input(
    #         "What are the 21CC (including New Media Literacies) that are important for my students to develop? "
    #     )
    # if st.checkbox(
    #     "I would like to incorporate certain lesson elements in my lesson plan"
    # ):

    #     st.subheader("5. Lesson Structure")
    #     incorporate_elements = st.text_area(
    #         "Incoporate lesson elements (e.g. lesson should be fun and include pair work)",
    #         help="Describe lesson elements that you would like to have",
    #     )

    # container = st.container()
    # with container:
    #     st.session_state.lesson_col_prompt = lesson_collaborator()
    #     # on = sac.buttons([sac.ButtonsItem(label=f"Continue Conversation at {LESSON_BOT}", color='#40826D')], format_func='title', index=None, size='small',type='primary')
    #     on = sac.switch(
    #         label=f"Continue Conversation at {LESSON_BOT}",
    #         value=False,
    #         align="start",
    #         position="left",
    #     )
    #     if on:
    #         st.session_state.start = 3
    #         st.session_state.option = LESSON_BOT
    #         st.session_state.chatbot = st.session_state.collaborator_mode
    #         st.session_state.chatbot_index = 0
    #         container.empty()
    #         st.rerun()

    #     if st.session_state.lesson_col_prompt:
    #         lesson_bot(
    #             st.session_state.lesson_col_prompt,
    #             st.session_state.lesson_collaborator,
    #             LESSON_COLLAB,
    #         )
    #         lesson_design_options()
