from datetime import datetime

from flask import render_template, Blueprint, request, flash, redirect, url_for, make_response
from sqlalchemy import or_
from sqlalchemy.orm import with_polymorphic

from app import db
from app.models import Course, Student, Teacher, User

bp_main = Blueprint('main', __name__)


@bp_main.route('/')
def index(name=""):
    if 'name' in request.cookies:
        name = request.cookies.get('name')
    return render_template('index.html', name=name)


@bp_main.route('/courses', methods=['GET'])
def courses():
    courses = Course.query.join(Teacher).with_entities(Course.course_code, Course.name,
                                                       Teacher.name.label('teacher_name')).all()
    return render_template("courses.html", courses=courses)


@bp_main.route('/schedule_a_lesson', methods=['GET'])
def schedule_a_lesson():

    return render_template("schedule_a_lesson.html", courses=courses)


@bp_main.route('/lessons', methods=['GET'])
def lessons():

    return render_template("lessons.html", courses=courses)


@bp_main.route('/wallet', methods=['GET'])
def wallet():

    return render_template("wallet.html", courses=courses)


@bp_main.route('/delete_cookie')
def delete_cookie():
    response = make_response(redirect(url_for('main.index')))
    response.set_cookie('name', '', expires=datetime.now())
    return response
