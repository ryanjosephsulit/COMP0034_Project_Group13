from langbridge import db
from langbridge.models import Teacher, User, BankAccount, Wallet, Language, LanguageUser, Lesson, LessonReview


def populate_db():
    """Populates the language.db database if it is empty. The Flask langbridge needs to be running before you execute this code.

    :return: None
    """

    if not User.query.first():
        u1 = User(email="cs1234567@ucl.co.uk", password="cs1234567", name="Ahmet Roth")
        u2 = User(email="cs1234568@ucl.co.uk", password="cs1234568", user_type="user", name="Elsie-Rose Kent")
        u3 = User(email="cs1234569@ucl.co.uk", password="cs1234569", user_type="user", name="Willem Bull")

        t1 = Teacher(email="ct0000123@ucl.co.uk", password="ct0000123", user_type="teacher", title="Dr", name="Lewis Baird", rating="5", reviews="initial")
        t2 = Teacher(email="ct0000124@ucl.co.uk", password="ct0000124", user_type="teacher", title="Prof", name="Elif Munro", rating="5", reviews="initial")
        t3 = Teacher(email="ct0000125@ucl.co.uk", password="ct0000125", user_type="teacher", title="Ms", name="Aleyna Bonilla", rating="5", reviews="initial")

        lang1 = Language(name="Mandarin")
        lang2 = Language(name="English")
        lang3 = Language(name="Spanish")


        db.session.add_all([u1, u2, u3])
        db.session.add_all([t1, t2, t3])
        db.session.add_all([lang1, lang2, lang3])
        db.session.commit()
