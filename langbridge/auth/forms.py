from flask_wtf import FlaskForm
from sqlalchemy import or_
from sqlalchemy.orm import with_polymorphic
from wtforms import SelectField, StringField, PasswordField, ValidationError, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

from langbridge import db
from langbridge.models import Teacher, User, BankAccount, Wallet, Language, Lesson, LessonReview


class SignupForm(FlaskForm):
    title = SelectField('Title', choices=[('mr', 'Mr'), ('mrs', 'Mrs'), ('dr', 'Dr'), ('prof', 'Prof')])
    name = StringField('Name', validators=[DataRequired()])
    role = SelectField('Role', choices=[('learner', 'Learner'), ('teacher', 'Teacher')])
    language = SelectField('Of Which Language?', choices=[('1', 'Mandarin'), ('2', 'English'), ('3', 'Spanish')])
    email = StringField('Email Address', validators=[DataRequired(), Email(message='Valid email address required')])
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

    def validate_email(self, email):
        users = with_polymorphic(User, [Teacher])
        results = db.session.query(users).filter(
            or_((users.email == email.data))).first()
        # student = Student.query.filter_by(student_ref=id_value.data).first()
        if results is not None:
            raise ValidationError('An account is already registered for that email address')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')


class SearchForm(FlaskForm):
    language = SelectField('Language', choices=[('1', 'Mandarin'), ('2', 'English'), ('3', 'Spanish')])


class EditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    language = SelectField('Language', choices=[('1', 'Mandarin'), ('2', 'English'), ('3', 'Spanish')])
    review = StringField('Review', validators=[DataRequired()])
