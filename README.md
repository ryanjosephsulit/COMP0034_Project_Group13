# COMP0034 Web Development - Group 13 Project
Based on COMP0034's "Completed example of the comp0034_flask_login exercises"

error found:  File "/Users/leonxu/PycharmProjects/COMP0034_Project_Group13/langbridge/main/routes.py", line 23, in language
    language = Language.query.join(User).with_entities(Language.lang_id, Language.name,
