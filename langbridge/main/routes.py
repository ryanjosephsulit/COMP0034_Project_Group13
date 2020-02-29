from datetime import datetime

from flask import render_template, Blueprint, request, flash, redirect, url_for, make_response
from sqlalchemy import or_
from sqlalchemy.orm import with_polymorphic

from langbridge import db
from langbridge.models import Teacher, User, BankAccount, Wallet, Language, LanguageUser, Lesson, LessonReview


bp_main = Blueprint('main', __name__)


@bp_main.route('/')
def index(name=""):
    if 'name' in request.cookies:
        name = request.cookies.get('name')
    return render_template('index.html', name=name)


@bp_main.route('/courses', methods=['GET'])
def courses():
    courses = Language.query.join(Teacher).with_entities(Language.lang_id, Language.name,
                                                       Teacher.name.label('teacher_name')).all()
    return render_template("courses.html", courses=courses)



@bp_main.route('/delete_cookie')
def delete_cookie():
    response = make_response(redirect(url_for('main.index')))
    response.set_cookie('name', '', expires=datetime.now())
    return response
