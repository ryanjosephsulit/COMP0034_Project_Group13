from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from langbridge import db
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    user_type = db.Column(db.String(10), nullable=False)
    lang_id = db.Column(db.Integer, db.ForeignKey('language.lang_id'), nullable=False)
    languages = db.relationship('Language', backref='Users')

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
    teacher_id = db.Column(None, db.ForeignKey('user.id'), primary_key=True)
    title = db.Column(db.Text)
    rating = db.Column(db.Integer, nullable=False)
    reviews = db.Column(db.String)
    users = db.relationship('User', backref='teachers')


    __mapper_args__ = {"polymorphic_identity": "teacher"}

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class BankAccount(db.Model):
    __tablename__ = 'bank_account'
    card_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('user.id'))
    payment_type = db.Column(db.String(250), nullable=False)
    credit_card_num = db.Column(db.Integer)
    users = db.relationship('User', backref='bankAccounts')

    def __repr__(self):
        return f"Forecast('{self.payment_type}', '{self.credit_card_num}')"


class Wallet(db.Model):
    __tablename__ = 'wallet'
    wallet_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('user.id'))
    balance = db.Column(db.Integer)
    users = db.relationship('User', backref='wallets')


class Lesson(db.Model):
    __tablename__ = 'lesson'
    lesson_id = db.Column(db.Integer, primary_key=True)
    learner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'))
    aim = db.Column(db.String)
    format = db.Column(db.String)
    time = db.Column(db.String)
    users = db.relationship('User', backref='lessons')

class LessonReview(db.Model):
    __tablename__ = 'lesson_review'
    review_id = db.Column(db.Integer, primary_key=True)
    learner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.String)
    reviewed_on = db.Column(db.String)
    users = db.relationship('User', backref='lessonReviews')


class Language(db.Model):
    __tablename__ = 'language'
    lang_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

#class LanguageUser(db.Model):
#    _tablename_ = 'language_user'
#    lang_id = db.Column(db.Integer, db.ForeignKey('language.lang_id'), primary_key=True)
#    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
#    languages = db.relationship('Language', backref='languageusers')
#    users = db.relationship('User', backref='languageusers')