# Introduction
This codebase serves the needs of different teams, whom utilises different features that it offers. Currently, at this point in time, two features are being used.

- Lesson Collaborator Chatbot (LCC)
- Metacogition (Metacog)

## Production URLs
- https://cotf-lcc-prototype.com
- https://cotf-metacog-prototype.com

## Secrets
> [!IMPORTANT]  
> The following env variables are required for setup. You can add this to the `secrets.toml` file in your streamlit deployment

```

openai_key = "YOUR_OPEN_API_KEY"
default_db = "chergpt.db"
default_temp = 0.0
default_frequency_penalty = 0.0
default_presence_penalty = 0.0
default_k_memory = 4
default_model = "gpt-4-1106-preview"
default_password = "default_password"
student_password = "studentp@sswrd"
teacher_password = "teacherp@sswrd"
super_admin_password = "pass1234"
super_admin = "super_admin"
default_title = "GenAI Workshop Framework V2"
sql_ext_path = "None"
```

## Deployment and Continuous Integration
Do follow the process below to update the EC2 instance on GCC AWS. Any updates shall only be done on a weekly basis.

1. Push all updates to github repository
2. Change visibility of project in settings to public
3. Pull changes from EC2 instance using `git pull origin main`
4. Change visibility of project in settings to private
