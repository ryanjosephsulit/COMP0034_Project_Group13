from flask_bcrypt import generate_password_hash, check_password_hash

from langbridge import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    user_type = db.Column(db.String(10), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": user_type
    }

    def __repr__(self):
        return "User email %s" % self.email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Teacher(User):
    __tablename__ = 'teacher'
    teacher_id = db.Column(None, db.ForeignKey('user.user_id'), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    reviews = db.Column(db.String)

    __mapper_args__ = {"polymorphic_identity": "learner"}

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class BankAccount(db.Model):
    __tablename__ = 'bank_account'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    payment_type = db.Column(db.String(250), nullable=False)
    payment_details = db.Column(db.String(250), nullable=False)


    def __repr__(self):
        return f"Forecast('{self.forecast}', '{self.comment}')"


class Wallet(db.Model):
    __tablename__ = 'wallet'
    wallet_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    balance = db.Column(db.Integer)


class Lesson(db.Model):
    __tablename__ = 'lesson'
    lesson_id = db.Column(db.Integer, primary_key=True)
    learner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'))
    aim = db.Column(db.String)
    format = db.Column(db.String)
    time = db.Column(db.String)


class LessonReview(db.Model):
    __tablename__ = 'lesson_review'
    review_id = db.Column(db.Integer, primary_key=True)
    learner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.String)
    reviewed_on = db.Column(db.String)


class Language(db.Model):
    __tablename__ = 'language'
    lang_id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String)


class LanguageUser(db.Model):
    __tablename__ = 'language_user'
    lang_id = db.Column(db.Integer, db.ForeignKey('language.lang_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)