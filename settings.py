import os
import streamlit as st
from services.aws import SecretsManager

# constants

PRI_LEVELS = [
    "Primary 1",
    "Primary 2",
    "Primary 3",
    "Primary 4",
    "Primary 5",
    "Primary 6",
]

SEC_LEVELS = [
    "Secondary 1",
    "Secondary 2",
    "Secondary 3",
    "Secondary 4",
    "Secondary 5",
]

JC_LEVELS = [
    "Junior College 1",
    "Junior College 2",
    "Junior College 3",
]

EDUCATION_LEVELS = PRI_LEVELS + SEC_LEVELS + JC_LEVELS

SUBJECTS_LIST = [
    "English Language",
    "Chinese",
    "Malay",
    "Tamil",
    "Mathematics",
    "Science",
    "Social Studies",
    "Physical Education (PE)",
    "Art",
    "Music",
    "Character and Citizenship Education (CCE)",
    "Design and Technology",
    "Food and Consumer Education (FCE)",
    "Computer Studies",
    "Additional Mathematics (Secondary)",
    "Literature (Secondary)",
    "History (Secondary)",
    "Geography (Secondary)",
    "Physics (Secondary)",
    "Chemistry (Secondary)",
    "Biology (Secondary)",
    "Economics (JC)",
    "Accounting (JC)",
    "General Paper (JC)",
    "Mathematics (JC)",
    "Further Mathematics (JC)",
    "Physics (JC)",
    "Chemistry (JC)",
    "Biology (JC)",
    "History (JC)",
    "Geography (JC)",
    "Art (JC)",
    "Music (JC)",
    "Theatre Studies and Drama (JC)",
]

FUNC_DESCRIPTIONS = {
    "Personal Dashboard": "An interface tailored for individual users to view and manage their personal activities and settings.",
    "Metacognitive Feedback": "A utility for helping students learn about science concepts and processes.",
    "Reflective Peer": "Allows students to reflect on their learning and share their reflections with their peers.",
    "Thinking Facilitator": "A tool that helps students to think critically and creatively.",
    "Lesson Design Facilitator": "A tool that facilitates cooperative lesson planning and content sharing between educators.",
    "Lesson Collaborator": "A tool that facilitates cooperative lesson planning and content sharing between educators.",
    "Lesson Commentator": "A platform that allows educators to provide feedback and annotations on lesson plans or content.",
    "Lesson Designer Map": "A tool that helps educators to design and plan lessons.",
    "AI Chatbot": "A virtual assistant powered by AI to interact and answer queries in real-time.",
    "Agent Chatbot": "An advanced chatbot that uses AI to provide more dynamic responses.",
    "Chatbot Management": "Tools for managing chatbot prompts and behaviors.",
    "Files management": "A digital storage solution that helps users to store, categorize, and retrieve files.",
    "KB management": "A system to manage the knowledge base, including its content, structure, and access permissions.",
    "Organisation Management": "A platform to oversee and control various aspects of an organization including its structure, roles, and policies.",
    "School Users Management": "A system tailored for educational institutions to manage students, teachers, and staff profiles and access rights.",
}

# Names
DEFAULT_TITLE = "GenAI Workshop Framework V2"
DEFAULT_PROMPT = "You are a helpful assistant"
LESSON_BOT = "Lesson Collaborator (Chatbot)"

SA = 1
STU = 2
TCH = 3
AD = 4
COTF = 0
META = 1
PANDAI = 2
META_BOT = "Thinking Facilitator bot"
QA_BOT = "AI Assistant bot"
AI_BOT = "AI Chat bot"
LESSON_BOT = "Lesson Collaborator (Chatbot)"
LESSON_COLLAB = "Lesson Collaborator (Scaffolded)"
LESSON_COMMENT = "Lesson Commentator"
LESSON_MAP = "Lesson Designer Map"
REFLECTIVE = "Reflective Peer bot"
CONVERSATION = "Conversation Assistant bot"
MINDMAP = "Mindmap Generator bot"
METACOG = "Metacognitive Feedback bot"


# Others
ACK = """
        Notice on the Use of Generative AI: We employ advanced generative AI technology to enhance our services and user experience. 
        This AI analyzes data and generates responses based on learned information. While we strive for accuracy and relevance, 
        please be aware that AI-generated content may not always be perfect or reflect the latest real-world developments. We encourage users to use discretion and consider the AI's limitations.
        The AI-generated content is for educational purposes only and should not be used as a substitute for professional advice.
        The retrieval augmented generation (RAG) knowledge base and user accounts DOES NOT PERSIST when the application is rebooted, you will lose all your data unless it is backed up using the super admin account.
        I WILL NOT UPLOAD ANY PERSONAL DATA OR SENSITIVE or CONFIDENTIAL INFORMATION TO THIS PLATFORM.
      """

# Database

if os.environ["ENVIRONMENT"] == "GCC":
    DEFAULT_DB = SecretsManager.get_secret("default_db")
else:
    DEFAULT_DB = st.secrets["default_db"]