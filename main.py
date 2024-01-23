# No need SQLite
import nltk
import streamlit as st

from streamlit_antd_components import menu, MenuItem
import streamlit_antd_components as sac
from metacog.metacog import science_feedback, reflective_peer
from lcc.lesson_plan import lesson_bot
from basecode.main_bot import (
    basebot_memory,
    basebot_qa_memory,
    clear_session_states,
    search_bot,
    basebot,
    basebot_qa,
    complete_my_lesson,
)
from basecode.files_module import display_files, docs_uploader, delete_files
from basecode.kb_module import (
    display_vectorstores,
    create_vectorstore,
    delete_vectorstores,
)
from basecode.authenticate import login_function, check_password
from basecode.class_dash import download_data_table_csv

# New schema move function fom settings
from basecode.database_schema import create_dbs
from basecode.agent import (
    agent_management,
    agent_bot,
    wiki_search,
    DuckDuckGoSearchRun,
    YouTubeSearchTool,
)

from basecode.database_module import (
    manage_tables,
    delete_tables,
    download_database,
    upload_database,
    upload_s3_database,
    download_from_s3_and_unzip,
    check_aws_secrets_exist,
    backup_s3_database,
    db_was_modified,
)
from basecode.org_module import (
    has_at_least_two_rows,
    initialise_admin_account,
    load_user_profile,
    display_accounts,
    create_org_structure,
    check_multiple_schools,
    process_user_profile,
    remove_or_reassign_teacher_ui,
    reassign_student_ui,
    change_teacher_profile_ui,
    add_user,
    streamlit_delete_interface,
    add_class,
    add_level,
)

from basecode.pwd_module import reset_passwords, password_settings
from basecode.users_module import (
    link_users_to_app_function_ui,
    set_function_access_for_user,
    create_prompt_template,
    update_prompt_template,
    vectorstore_selection_interface,
    pre_load_variables,
    load_and_fetch_vectorstore_for_user,
    link_profiles_to_vectorstore_interface,
)

from basecode.bot_settings import bot_settings_interface, load_bot_settings
from lcc.lesson_plan import (
    lesson_collaborator,
    lesson_bot,
    lesson_design_options,
    lesson_commentator,
    lesson_map_generator,
)

from PIL import Image
import configparser
import ast

from basecode.services.aws import SecretsManager


def download_nltk_data_if_absent(package_name):
    try:
        # Try loading the package to see if it exists
        nltk.data.find("tokenizers/" + package_name)
    except LookupError:
        # If the package doesn't exist, download it
        nltk.download(package_name)


download_nltk_data_if_absent("punkt")


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

# Setting Streamlit configurations
st.set_page_config(layout="wide")

# Fetching secrets from Streamlit
DEFAULT_TITLE = SecretsManager.get_secret("default_title")
SUPER_PWD = SecretsManager.get_secret("super_admin_password")
SUPER = SecretsManager.get_secret("super_admin")
DEFAULT_DB = SecretsManager.get_secret("default_db")

# Fetching values from config.ini
DEFAULT_TEXT = config_handler.get_value("constants", "DEFAULT_TEXT")
TCH = config_handler.get_value("constants", "TCH")
STU = config_handler.get_value("constants", "STU")
SA = config_handler.get_value("constants", "SA")
AD = config_handler.get_value("constants", "AD")
COTF = config_handler.get_value("constants", "COTF")
META = config_handler.get_value("constants", "META")
PANDAI = config_handler.get_value("constants", "PANDAI")
MENU_FUNCS = config_handler.get_value("menu_lists", "MENU_FUNCS")
META_BOT = config_handler.get_value("constants", "META_BOT")
QA_BOT = config_handler.get_value("constants", "QA_BOT")
LESSON_BOT = config_handler.get_value("constants", "LESSON_BOT")
LESSON_COLLAB = config_handler.get_value("constants", "LESSON_COLLAB")
LESSON_COMMENT = config_handler.get_value("constants", "LESSON_COMMENT")
LESSON_MAP = config_handler.get_value("constants", "LESSON_MAP")
REFLECTIVE = config_handler.get_value("constants", "REFLECTIVE")
CONVERSATION = config_handler.get_value("constants", "CONVERSATION")
MINDMAP = config_handler.get_value("constants", "MINDMAP")
METACOG = config_handler.get_value("constants", "METACOG")
ACK = config_handler.get_value("application_agreement", "ACK")
PROTOTYPE = config_handler.get_value("constants", "PROTOTYPE")


def is_function_disabled(function_name):
    # st.write("Function name: ", function_name)
    # st.write("Function options: ", st.session_state.func_options.get(function_name, True))
    return st.session_state.func_options.get(function_name, True)


def return_function_name(function_name, default_name=""):
    if st.session_state.func_options.get(function_name, True):
        return "-"
    else:
        if default_name == "":
            return function_name
        else:
            return default_name


def initialize_session_state(menu_funcs, default_value):
    st.session_state.func_options = {key: default_value for key in menu_funcs.keys()}


def main():
    try:
        if "title_page" not in st.session_state:
            st.session_state.title_page = DEFAULT_TITLE

        st.title(st.session_state.title_page)
        sac.divider(label="Classroom of the Future", icon="house", align="center")

        if "api_key" not in st.session_state:
            st.session_state.api_key = ""

        if "option" not in st.session_state:
            st.session_state.option = False

        if "login" not in st.session_state:
            st.session_state.login = False

        if "user" not in st.session_state:
            st.session_state.user = None

        if "start" not in st.session_state:
            st.session_state.start = 0

        if "openai_model" not in st.session_state:
            st.session_state.openai_model = SecretsManager.get_secret("default_model")

        if "msg" not in st.session_state:
            st.session_state.msg = []

        if "rating" not in st.session_state:
            st.session_state.rating = False

        if "lesson_plan" not in st.session_state:
            st.session_state.lesson_plan = ""

        if "temp" not in st.session_state:
            st.session_state.temp = int(SecretsManager.get_secret("default_temp"))

        if "acknowledgement" not in st.session_state:
            st.session_state.acknowledgement = False

        if "frequency_penalty" not in st.session_state:
            st.session_state.frequency_penalty = int(
                SecretsManager.get_secret("default_frequency_penalty")
            )

        if "presence_penalty" not in st.session_state:
            st.session_state.presence_penalty = int(
                SecretsManager.get_secret("default_presence_penalty")
            )

        if "k_memory" not in st.session_state:
            st.session_state.k_memory = int(
                SecretsManager.get_secret("default_k_memory")
            )

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
            st.session_state.func_options = {}
            initialize_session_state(MENU_FUNCS, True)

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

        # useful session state variables for testing and debugging
        # not in use for production
        if "test1" not in st.session_state:
            st.session_state.test1 = ""

        if "test2" not in st.session_state:
            st.session_state.test2 = ""

        # These functions below will create the initial database and administator account
        create_dbs()
        initialise_admin_account()

        # PLEASE REMOVE THIS or COMMENT IT
        # st.write("User Profile: ", st.session_state.user)

        # PLEASE REMOVE ABOVE
        with st.sidebar:  # options for sidebar
            if st.session_state.login == False:
                st.image("app_logo/cotf_logo.png")
                st.session_state.option = menu([MenuItem("Users login", icon="people")])
            else:
                # can do a test if user is school is something show a different logo and set a different API key
                # super admin login feature
                if st.session_state.user["profile_id"] == SA:
                    # Initialize the session state for function options
                    initialize_session_state(MENU_FUNCS, False)
                else:
                    if st.session_state.acknowledgement == False:
                        initialize_session_state(MENU_FUNCS, True)
                    else:
                        set_function_access_for_user(st.session_state.user["id"])
                        # st.write("Function options: ", st.session_state.func_options)
                    # Using the is_function_disabled function for setting the `disabled` attribute
                st.session_state.option = sac.menu(
                    [
                        sac.MenuItem(
                            "Home",
                            icon="house",
                            children=[
                                sac.MenuItem(
                                    return_function_name("Personal Dashboard"),
                                    icon="person-circle",
                                    disabled=is_function_disabled("Personal Dashboard"),
                                ),
                                # sac.MenuItem('Class Dashboard', icon='clipboard-data', disabled=is_function_disabled('Class Dashboard')),
                            ],
                        ),
                        sac.MenuItem(
                            "Lesson Assistant",
                            icon="person-fill-gear",
                            children=[
                                sac.MenuItem(
                                    return_function_name(
                                        "Lesson Design Facilitator",
                                        "Lesson Collaborator (Chatbot)",
                                    ),
                                    icon="chat-text",
                                    disabled=is_function_disabled(
                                        "Lesson Design Facilitator"
                                    ),
                                ),
                                sac.MenuItem(
                                    return_function_name(
                                        "Lesson Collaborator",
                                        "Lesson Collaborator (Scaffolded)",
                                    ),
                                    icon="pencil-square",
                                    disabled=is_function_disabled(
                                        "Lesson Collaborator"
                                    ),
                                ),
                                sac.MenuItem(
                                    return_function_name(
                                        "Lesson Commentator", "Lesson Commentator"
                                    ),
                                    icon="chat-left-dots",
                                    disabled=is_function_disabled("Lesson Commentator"),
                                ),
                                # Jun Wen: Hiding this menu item as advised by Joe.
                                # sac.MenuItem(
                                #     return_function_name(
                                #         "Lesson Designer Map", "Lesson Designer Map"
                                #     ),
                                #     icon="diagram-2",
                                #     disabled=is_function_disabled(
                                #         "Lesson Designer Map"
                                #     ),
                                # ),
                            ],
                        ),
                        sac.MenuItem(
                            "Learning Tools",
                            icon="tools",
                            children=[
                                sac.MenuItem(
                                    return_function_name("Metacognitive Feedback"),
                                    icon="bug-fill",
                                    disabled=is_function_disabled(
                                        "Metacognitive Feedback"
                                    ),
                                ),
                                sac.MenuItem(
                                    return_function_name("Reflective Peer"),
                                    icon="people",
                                    disabled=is_function_disabled("Reflective Peer"),
                                ),
                                sac.MenuItem(
                                    return_function_name(
                                        "Thinking Facilitator",
                                        "Thinking Facilitator (Chatbot)",
                                    ),
                                    icon="chat-dots",
                                    disabled=is_function_disabled(
                                        "Thinking Facilitator"
                                    ),
                                ),
                            ],
                        ),
                        sac.MenuItem(
                            "Types of ChatBots",
                            icon="person-fill-gear",
                            children=[
                                sac.MenuItem(
                                    return_function_name("AI Chatbot"),
                                    icon="chat-dots",
                                    disabled=is_function_disabled("AI Chatbot"),
                                ),
                                sac.MenuItem(
                                    return_function_name("Agent Chatbot"),
                                    icon="chat-dots",
                                    disabled=is_function_disabled("Agent Chatbot"),
                                ),
                                sac.MenuItem(
                                    return_function_name("Chatbot Management"),
                                    icon="wrench",
                                    disabled=is_function_disabled("Chatbot Management"),
                                ),
                            ],
                        ),
                        sac.MenuItem(
                            "Knowledge Base Tools",
                            icon="book",
                            children=[
                                sac.MenuItem(
                                    return_function_name(
                                        "Files management", "Files Management"
                                    ),
                                    icon="file-arrow-up",
                                    disabled=is_function_disabled("Files management"),
                                ),
                                sac.MenuItem(
                                    return_function_name(
                                        "KB management", "Knowledge Base Editor"
                                    ),
                                    icon="database-fill-up",
                                    disabled=is_function_disabled("KB management"),
                                ),
                            ],
                        ),
                        sac.MenuItem(
                            "Organisation Tools",
                            icon="buildings",
                            children=[
                                sac.MenuItem(
                                    return_function_name(
                                        "Organisation Management", "Org Management"
                                    ),
                                    icon="building-gear",
                                    disabled=is_function_disabled(
                                        "Organisation Management"
                                    ),
                                ),
                                sac.MenuItem(
                                    return_function_name(
                                        "School Users Management", "Users Management"
                                    ),
                                    icon="house-gear",
                                    disabled=is_function_disabled(
                                        "School Users Management"
                                    ),
                                ),
                            ],
                        ),
                        sac.MenuItem(type="divider"),
                        sac.MenuItem("Profile Settings", icon="gear"),
                        sac.MenuItem("Application Info", icon="info-circle"),
                        sac.MenuItem("Logout", icon="box-arrow-right"),
                    ],
                    index=st.session_state.start,
                    format_func="title",
                    open_all=True,
                )

        if st.session_state.option == "Users login":
            col1, col2 = st.columns([3, 4])
            placeholder = st.empty()
            with placeholder:
                with col1:
                    if login_function() == True:
                        st.session_state.user = load_user_profile(st.session_state.user)
                        pre_load_variables(st.session_state.user["id"])
                        load_and_fetch_vectorstore_for_user(st.session_state.user["id"])
                        load_bot_settings(st.session_state.user["id"])
                        st.session_state.login = True
                        placeholder.empty()
                        st.rerun()
                with col2:
                    pass
        elif st.session_state.option == "Home":
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(
                    "Acknowledgement on the use of Generative AI with Large Language Models"
                )
                initialize_session_state(MENU_FUNCS, True)
                st.write(ACK)
                ack = st.checkbox("I acknowledge the above information")
                if ack:
                    st.session_state.acknowledgement = True
                    set_function_access_for_user(st.session_state.user["id"])
                    st.session_state.start = 1
                    st.rerun()
                else:
                    st.warning(
                        "Please acknowledge the above information before you proceed"
                    )
                    initialize_session_state(MENU_FUNCS, True)
                    st.stop()
                pass
            with col2:
                pass

        # Personal Dashboard
        elif st.session_state.option == "Personal Dashboard":
            st.subheader(f":green[{st.session_state.option}]")
            if st.session_state.user["profile_id"] == SA:
                sch_id, msg = process_user_profile(st.session_state.user["profile_id"])
                st.write(msg)
                download_data_table_csv(
                    st.session_state.user["id"],
                    sch_id,
                    st.session_state.user["profile_id"],
                )
            else:
                download_data_table_csv(
                    st.session_state.user["id"],
                    st.session_state.user["school_id"],
                    st.session_state.user["profile_id"],
                )
            display_vectorstores()
            vectorstore_selection_interface(st.session_state.user["id"])

        elif st.session_state.option == "Lesson Collaborator (Chatbot)":
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
                        sac.ChipItem(
                            label="Raw Search", icon="search", disabled=vs_flag
                        ),
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

        elif st.session_state.option == "Lesson Collaborator (Scaffolded)":
            st.session_state.start = 4
            st.subheader(f":green[{st.session_state.option}]")
            container = st.container()
            with container:
                st.session_state.lesson_col_prompt = lesson_collaborator()
                # on = sac.buttons([sac.ButtonsItem(label=f"Continue Conversation at {LESSON_BOT}", color='#40826D')], format_func='title', index=None, size='small',type='primary')
                on = sac.switch(
                    label=f"Continue Conversation at {LESSON_BOT}",
                    value=False,
                    align="start",
                    position="left",
                )
                if on:
                    st.session_state.start = 3
                    st.session_state.option = LESSON_BOT
                    st.session_state.chatbot = st.session_state.collaborator_mode
                    st.session_state.chatbot_index = 0
                    container.empty()
                    st.rerun()
                if st.session_state.lesson_col_prompt:
                    # st.write("I am here", st.session_state.lesson_col_prompt)
                    lesson_bot(
                        st.session_state.lesson_col_prompt,
                        st.session_state.lesson_collaborator,
                        LESSON_COLLAB,
                    )
                    lesson_design_options()

        elif st.session_state.option == "Lesson Commentator":
            st.session_state.start = 5
            st.subheader(f":green[{st.session_state.option}]")
            container1 = st.container()

            with container1:
                # on = sac.buttons([sac.ButtonsItem(label=f"Continue Conversation at {LESSON_BOT}", color='#40826D')], format_func='title', index=None, size='small',type='primary')
                st.session_state.lesson_col_prompt = lesson_commentator()
                on = sac.switch(
                    label=f"Continue Conversation at {LESSON_BOT}",
                    value=False,
                    align="start",
                    position="left",
                )
        elif st.session_state.option == "Lesson Designer Map":
            st.subheader(f":green[{st.session_state.option}]")
            lesson_map_generator()

        # Metacog Feedback
        elif st.session_state.option == "Metacognitive Feedback":
            st.subheader(f":green[{st.session_state.option}]")
            prompt = science_feedback()

            if st.session_state.vs == False:
                st.warning("Metacognitive Feedback is not linked to any knowledge base")

            if prompt is not None:
                if prompt["text"] != "" and prompt["question"] != "":
                    prompt_template = st.session_state.metacognitive_feedback
                    lesson_bot(prompt, prompt_template, METACOG)
                else:
                    st.warning("You will need to enter both question and text.")

        # Reflective Peer
        elif st.session_state.option == "Reflective Peer":
            st.subheader(f":green[{st.session_state.option}]")
            prompt = reflective_peer()

            if st.session_state.vs == False:
                st.warning("Reflective Peer is not linked to any knowledge base")

            if prompt is not None:
                if prompt["text"] != "" and prompt["question"] != "":
                    prompt_template = st.session_state.reflective_peer
                    lesson_bot(prompt, prompt_template, REFLECTIVE)
                else:
                    st.warning("You will need to enter both question and text.")

        # Thinking Facilitator
        elif st.session_state.option == "Thinking Facilitator (Chatbot)":
            st.subheader(f":green[{st.session_state.option}]")

            # Jun Wen: Options (Conversation, Default and Paragraph) were asked to
            # be removed by Joe.

            # Metacog settings
            with st.expander("Thinking Facilitator Settings"):
                vectorstore_selection_interface(st.session_state.user["id"])

                if st.session_state.vs:
                    vs_flag = False
                else:
                    vs_flag = True

                options = sac.chip(
                    items=[
                        sac.ChipItem(
                            label="Raw Search", icon="search", disabled=vs_flag
                        ),
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

            # chatbot with knowledge base
            if st.session_state.vs:
                if raw_search == True:
                    search_bot()
                else:
                    if st.session_state.memoryless:
                        # memoryless chatbot with knowledge base but no memory
                        basebot_qa(META_BOT)
                    else:
                        # chatbot with knowledge base and memory
                        basebot_qa_memory(META_BOT)

            # chatbot with no knowledge base
            else:
                # memoryless chatbot with no knowledge base and no memory
                if st.session_state.memoryless:
                    basebot(META_BOT)
                else:
                    # chatbot with no knowledge base but with memory
                    basebot_memory(META_BOT)

        elif st.session_state.option == "AI Chatbot":
            # Code for AI Chatbot - ZeroCode
            st.write("Current Chatbot Template: ", st.session_state.chatbot)
            # check if API key is entered
            with st.expander("Chatbot Settings"):
                vectorstore_selection_interface(st.session_state.user["id"])
                # new options --------------------------------------------------------
                if st.session_state.vs:
                    vs_flag = False
                else:
                    vs_flag = True
                options = sac.chip(
                    items=[
                        sac.ChipItem(
                            label="Raw Search", icon="search", disabled=vs_flag
                        ),
                        sac.ChipItem(label="Enable Memory", icon="memory"),
                        sac.ChipItem(label="Rating Function", icon="star-fill"),
                        sac.ChipItem(label="Capture Responses", icon="camera-fill"),
                        sac.ChipItem(label="Download Responses", icon="download"),
                    ],
                    index=[1, 2, 3],
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
                    if (
                        st.session_state.memoryless
                    ):  # memoryless chatbot with knowledge base but no memory
                        basebot_qa(LESSON_BOT)
                    else:
                        # chatbot with knowledge base and memory
                        basebot_qa_memory(LESSON_BOT)
            else:  # chatbot with no knowledge base
                if (
                    st.session_state.memoryless
                ):  # memoryless chatbot with no knowledge base and no memory
                    basebot(LESSON_BOT)
                else:
                    # chatbot with no knowledge base but with memory
                    basebot_memory(LESSON_BOT)

        elif st.session_state.option == "Agent Chatbot":
            if st.session_state.tools == []:
                st.warning(
                    "Loading Wikipedia Search, Internet Search and YouTube Search, you may select your tools in Bot & Prompt management"
                )
                st.session_state.tools = [
                    wiki_search,
                    DuckDuckGoSearchRun(name="Internet Search"),
                    YouTubeSearchTool(),
                ]
                agent_bot()
            else:
                agent_bot()

        # ensure that it is for administrator or super_admin
        elif st.session_state.option == "Chatbot Management":
            if (
                st.session_state.user["profile_id"] == SA
                or st.session_state.user["profile_id"] == AD
            ):
                st.subheader(f":green[{st.session_state.option}]")
                templates = create_prompt_template(st.session_state.user["id"])
                st.divider()
                # st.write("Templates created: ", templates)
                update_prompt_template(st.session_state.user["profile_id"], templates)
                st.subheader("Agent Management")
                agent_management()
                if st.session_state.user["profile_id"] == SA:
                    st.subheader("OpenAI Chatbot Parameters Settings")
                    bot_settings_interface(
                        st.session_state.user["profile_id"],
                        st.session_state.user["school_id"],
                    )
            else:
                st.subheader(
                    f":red[This option is accessible only to administrators only]"
                )

        # Knowledge Base Tools
        elif st.session_state.option == "Files Management":
            st.subheader(f":green[{st.session_state.option}]")
            display_files()
            docs_uploader()
            delete_files()

        elif st.session_state.option == "Knowledge Base Editor":
            st.subheader(f":green[{st.session_state.option}]")
            options = sac.steps(
                items=[
                    sac.StepsItem(
                        title="Step 1", description="Create a new knowledge base"
                    ),
                    sac.StepsItem(
                        title="Step 2", description="Assign a knowledge base to a user"
                    ),
                    sac.StepsItem(
                        title="Step 3", description="Delete a knowledge base (Optional)"
                    ),
                ],
                format_func="title",
                placement="vertical",
                size="small",
            )
            if options == "Step 1":
                st.subheader("KB created in the repository")
                display_vectorstores()
                st.subheader("Files available in the repository")
                display_files()
                create_vectorstore()
            elif options == "Step 2":
                st.subheader("KB created in the repository")
                display_vectorstores()
                vectorstore_selection_interface(st.session_state.user["id"])
                link_profiles_to_vectorstore_interface(st.session_state.user["id"])

            elif options == "Step 3":
                st.subheader("KB created in the repository")
                display_vectorstores()
                delete_vectorstores()

        # Organisation Tools
        elif st.session_state.option == "Users Management":
            if (
                st.session_state.user["profile_id"] == SA
                or st.session_state.user["profile_id"] == AD
            ):
                st.subheader(f":green[{st.session_state.option}]")
                sch_id, msg = process_user_profile(st.session_state.user["profile_id"])
                rows = has_at_least_two_rows()
                if rows >= 2:
                    # Password Reset
                    st.subheader("User accounts information")
                    df = display_accounts(sch_id)
                    st.warning("Password Management")
                    st.subheader("Reset passwords of users")
                    reset_passwords(df)
                    add_user(sch_id)
            else:
                st.subheader(
                    f":red[This option is accessible only to administrators only]"
                )

        elif st.session_state.option == "Org Management":
            if st.session_state.user["profile_id"] == SA:
                st.subheader(f":green[{st.session_state.option}]")
                # direct_vectorstore_function()

                if check_password(st.session_state.user["username"], SUPER_PWD):
                    st.write(
                        "To start creating your teachers account, please change the default password of your administrator account under profile settings"
                    )
                else:
                    sch_id, msg = process_user_profile(
                        st.session_state.user["profile_id"]
                    )
                    create_flag = False
                    rows = has_at_least_two_rows()
                    if rows >= 2:
                        create_flag = check_multiple_schools()
                    st.markdown("###")
                    st.write(msg)
                    st.markdown("###")
                    steps_options = sac.steps(
                        items=[
                            sac.StepsItem(
                                title="step 1",
                                description="Create Students and Teachers account of a new school",
                                disabled=create_flag,
                            ),
                            sac.StepsItem(
                                title="step 2",
                                description="Remove/Assign Teachers to Classes",
                            ),
                            sac.StepsItem(
                                title="step 3", description="Change Teachers Profile"
                            ),
                            sac.StepsItem(
                                title="step 4",
                                description="Setting function access for profiles",
                            ),
                            sac.StepsItem(
                                title="step 5",
                                description="Reassign Students to Classes(Optional)",
                            ),
                            sac.StepsItem(
                                title="step 6",
                                description="Add/Delete Classes and Levels",
                            ),
                            sac.StepsItem(
                                title="step 7",
                                description="Managing SQL Schema Tables",
                                icon="radioactive",
                            ),
                        ],
                        format_func="title",
                        placement="vertical",
                        size="small",
                    )
                    if steps_options == "step 1":
                        if create_flag:
                            st.write("School created, click on Step 2")
                        else:
                            create_org_structure()
                    elif steps_options == "step 2":
                        remove_or_reassign_teacher_ui(sch_id)
                    elif steps_options == "step 3":
                        change_teacher_profile_ui(sch_id)
                    elif steps_options == "step 4":
                        link_users_to_app_function_ui(sch_id)
                    elif steps_options == "step 5":
                        reassign_student_ui(sch_id)
                    elif steps_options == "step 6":
                        add_level(sch_id)
                        st.divider()
                        add_class(sch_id)
                        st.divider()
                        streamlit_delete_interface()
                    elif steps_options == "step 7":
                        st.subheader(":red[Managing SQL Schema Tables]")
                        st.warning(
                            "Please do not use this function unless you know what you are doing"
                        )
                        if st.checkbox("I know how to manage SQL Tables"):
                            st.subheader(
                                ":red[Zip Database - Download and upload a copy of the database]"
                            )
                            download_database()
                            upload_database()
                            if check_aws_secrets_exist():
                                st.subheader(
                                    ":red[Upload Database to S3 - Upload a copy of the database to S3]"
                                )
                                upload_s3_database()
                                download_from_s3_and_unzip()
                            st.subheader(
                                ":red[Display and Edit Tables - please do so if you have knowledge of the current schema]"
                            )
                            manage_tables()
                            st.subheader(
                                ":red[Delete Table - Warning please use this function with extreme caution]"
                            )
                            delete_tables()
            else:
                st.subheader(
                    f":red[This option is accessible only to super administrators only]"
                )

        elif st.session_state.option == "Profile Settings":
            st.subheader(f":green[{st.session_state.option}]")
            # direct_vectorstore_function()
            password_settings(st.session_state.user["username"])

        elif st.session_state.option == "Application Info":
            st.subheader(f":green[{st.session_state.option}]")
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(
                    "Acknowledgement on the use of Generative AI with Large Language Models"
                )
                initialize_session_state(MENU_FUNCS, True)
                st.write(ACK)
                if st.session_state.acknowledgement == True:
                    st.success("You have acknowledged the above information")
                else:
                    ack = st.checkbox("I acknowledge the above information")
                    if ack:
                        st.session_state.acknowledgement = True
                        set_function_access_for_user(st.session_state.user["id"])
                        st.session_state.start = 1
                        st.rerun()
                    else:
                        st.warning(
                            "Please acknowledge the above information before you proceed"
                        )
                        initialize_session_state(MENU_FUNCS, True)
                        st.stop()
                    pass
            with col2:
                pass

        elif st.session_state.option == "Logout":
            if db_was_modified(DEFAULT_DB):
                if check_aws_secrets_exist():
                    backup_s3_database()
                    for key in st.session_state.keys():
                        del st.session_state[key]
                    st.rerun()
                elif st.session_state.user["profile_id"] == SA:
                    on = st.toggle("I do not want to download a copy of the database")
                    if on:
                        for key in st.session_state.keys():
                            del st.session_state[key]
                        st.rerun()
                    else:
                        download_database()
                        for key in st.session_state.keys():
                            del st.session_state[key]
                        st.rerun()
                else:
                    for key in st.session_state.keys():
                        del st.session_state[key]
                    st.rerun()
            else:
                for key in st.session_state.keys():
                    del st.session_state[key]
                st.rerun()

    except Exception as e:
        st.exception(e)


if __name__ == "__main__":
    main()
