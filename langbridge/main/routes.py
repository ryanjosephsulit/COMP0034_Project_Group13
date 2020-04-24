import random
from datetime import datetime

from flask import render_template, Blueprint, request, flash, redirect, url_for, make_response
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import with_polymorphic
from langbridge.auth.forms import SignupForm, LoginForm
from langbridge import db
from langbridge.models import Teacher, User, BankAccount, Wallet, Language, Lesson, LessonReview

bp_main = Blueprint('main', __name__)


@bp_main.route('/', methods=['POST', 'GET'])
def index(name=""):
    if 'name' in request.cookies:
        name = request.cookies.get('name')
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.role.data == "learner":
            user = User(name=form.name.data, email=form.email.data, lang_id=form.language.data)
        else:
            user = Teacher(name=form.name.data, title=form.title.data, email=form.email.data,
                           lang_id=form.language.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            user = User.query.filter_by(email=form.email.data).first()
            wallet = Wallet()
            wallet.balance = 0
            # Generate random number for wallet
            wallet.wallet_id = random.randint(78624, 8123981242)
            wallet.id = user.id
            db.session.add(wallet)
            db.session.commit()
            response = make_response(redirect(url_for('main.index')))
            response.set_cookie("name", form.name.data)
            return response
        except IntegrityError:
            db.session.rollback()
            flash('ERROR! Unable to register {}. Please check your details are correct and resubmit'.format(
                form.email.data), 'error')

    return render_template('index.html', name=name, form=form)


@bp_main.route('/languages', methods=['GET'])
def language():
    languages = Language.query.join(Teacher).with_entities(Language.lang_id, Language.name,
                                                           Teacher.name.label('user_name'), Teacher.email).order_by(
        Language.lang_id).all()
    print("HERE")
    # Simple test to see if languages is populated
    print(languages)

    return render_template("languages.html", language=languages)


@bp_main.route('/delete_cookie')
def delete_cookie():
    response = make_response(redirect(url_for('main.index')))
    response.set_cookie('name', '', expires=datetime.now())
    return response
