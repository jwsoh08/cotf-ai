import streamlit as st

from basecode.users_module import vectorstore_selection_interface
from lcc.lesson_plan import upload_lesson_plan

from services.openai import ChatGPT

from settings import EDUCATION_LEVELS, SUBJECTS_LIST

def lesson_commentator():
    st.session_state.start = 5
    st.subheader(f":green[{st.session_state.option}]")

    # Form start
    st.subheader("1. Basic Lesson Information for Feedback")
    subject = st.selectbox("Choose a Subject", SUBJECTS_LIST)
    level = st.selectbox("Choose a level", EDUCATION_LEVELS)
    duration = st.text_input(
        "Duration (in minutes)",
        help="Estimated duration of one lesson or over a few lessons",
    )

    st.subheader("2. Lesson Details for Feedback")
    topic = st.text_area(
        "Topic",
        help="Describe the specific topic or theme for the lesson",
    )
    skill_level = st.text_input(
        "Readiness Level",
        help="Beginner, Intermediate, Advanced ...",
    )

    st.subheader("3. Lesson Plan upload or key in manually")
    lesson_plan_content = upload_lesson_plan()
    if lesson_plan_content is not None and lesson_plan_content != "":
        if len(lesson_plan_content) > 6000:
            st.error(
                "Your lesson plan is too long. Please shorten it to 6000 chars or less."
            )
            return

    lesson_plan = st.text_area(
        "Please provide your lesson plan either upload or type into this text box (Max 6000 characters), including details such as learning objectives, activities, assessment tasks, and any use of educational technology tools.",
        height=500,
        max_chars=6000,
        value=lesson_plan_content,
    )

    st.subheader("4. Specific questions that I would like feedback on")
    feedback = st.text_area(
        "Include specific information from your lesson plan that you want feedback on."
    )

    st.subheader("5. Learners Profile")
    learners_info = st.text_input("Describe the learners for this lesson ")
    # Form end

    vectorstore_selection_interface(st.session_state.user["id"])

    if submitted := st.button(label="Provide Feedback", type="secondary"):
        # collect inputs in form
        prompt = f"""
        Imagine you are an experienced teacher. I'd like feedback on the lesson I've uploaded:  
    
        Subject: {subject}  
        Topic: {topic}  
        Level: {level}  
        Duration: {duration} minutes  
        Skill Level: {skill_level}  
        Lesson Plan Content: {lesson_plan}  
        Specific Feedback Areas: {feedback}  
        Description of Learners: {learners_info}  
        Please provide feedback to enhance this lesson plan."""


        # check if a knowledge base is selected
        kb_prompt = ""
        if st.session_state.vs:
            docs = st.session_state.vs.similarity_search(prompt)
            resources = docs[0].page_content

            kb_prompt = f"""
                        You may refer to this resources for the feedback of the lesson plan.
                        {resources}
                        """

        # make api call to chatgpt
        chatgpt = ChatGPT()
        
        prompt_template = st.session_state.lesson_commentator

        messages = [
            {"role": "system", "content": prompt_template},
            {"role": "user", "content": prompt + kb_prompt},
        ]

        response = ""

        with st.container():
            response = st.write_stream(chatgpt.chat_completions(messages, True))

        # save history in conversation
        st.session_state.msg.append(
            {
                "role": "user",
                "content": prompt,
            }
        )
        st.session_state.msg.append(
            {
                "role": "assistant",
                "content": response,
            }
        )
