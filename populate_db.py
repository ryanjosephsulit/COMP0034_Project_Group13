from langbridge import db
from langbridge.models import Teacher, User, BankAccount, Wallet, Language, LanguageUser, Lesson, LessonReview


def populate_db():
    """Populates the cscourses.db database if it is empty. The Flask langbridge needs to be running before you execute this code.

    :return: None
    """

    if not User.query.first():
        u1 = User(email="cs1234567@ucl.co.uk", password="cs1234567", name="Ahmet Roth")
        u2 = User(email="cs1234568@ucl.co.uk", password="cs1234568", user_type="learner",
                  name="Elsie-Rose Kent")
        u3 = User(email="cs1234569@ucl.co.uk", password="cs1234569", user_type="learner",
                  name="Willem Bull")

        t1 = Teacher(email="ct0000123@ucl.co.uk", password="ct0000123", user_type="teacher",
                     title="Dr", name="Lewis Baird")
        t2 = Teacher(email="ct0000124@ucl.co.uk", password="ct0000124", user_type="teacher",
                     title="Prof", name="Elif Munro")
        t3 = Teacher(email="ct0000125@ucl.co.uk", password="ct0000125", user_type="teacher",
                     title="Ms", name="Aleyna Bonilla")

        lang1 = Language(name="Mandarin")
        lang2 = Language(name="English")
        lang3 = Language(name="Spanish")

        lu1 = LanguageUser()
        lu2 = LanguageUser()
        lu3 = LanguageUser()

        lu1.lang_id.append(lang1)
        lu1.user_id.append(u2)

        lu2.lang_id.append(lang2)
        lu2.user_id.append(u2)

        lu3.lang_id.append(lang3)
        lu3.user_id.append(u1)

        lu1.lang_id.append(lang1)
        lu1.user_id.append(u3)

        db.session.add_all([u1, u2, u3])
        db.session.add_all([t1, t2, t3])
        db.session.commit()
