from datetime import timedelta
from urllib.parse import urlparse, urljoin
import random
from flask import render_template, Blueprint, request, flash, redirect, url_for, make_response, abort
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf import form
from sqlalchemy.exc import IntegrityError

from langbridge import login_manager
from langbridge.auth.forms import SignupForm, LoginForm, SearchForm
from langbridge.models import Teacher, User, BankAccount, Wallet, Language, Lesson, LessonReview

from sqlalchemy import or_
from sqlalchemy.orm import with_polymorphic

from langbridge import db

bp_auth = Blueprint('auth', __name__)


def is_safe_url(target):
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return redirect_url.scheme in ('http', 'https') and host_url.netloc == redirect_url.netloc


def get_safe_redirect():
    url = request.args.get('next')
    if url and is_safe_url(url):
        return url

    url = request.referrer
    if url and is_safe_url(url):
        return url
    return '/'


@login_manager.user_loader
def load_user(id):
    """Check if user is logged-in on every page load."""
    if id is not None:
        return User.query.get(id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.login'))


@bp_auth.route('/signup/', methods=['POST', 'GET'])
def signup():
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
    return render_template('signup.html', form=form)

@bp_auth.route('/advanced_search/', methods=['GET'])
@login_required
def advanced_search():
    return render_template("advanced_search.html")

@bp_auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        print(form.email.data, form.password.data)
        user = User.query.filter_by(email=form.email.data).first()
        print(user.email, user.password)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data, duration=timedelta(minutes=1))
        flash('Logged in successfully. {}'.format(user.name))
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)
        return redirect(next or url_for('main.index'))
    return render_template('login.html', form=form)


@bp_auth.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    if request.method == 'POST':
        term = request.form['search_term']
        if term == "":
            flash("Enter a name to search for")
            return redirect('/')
        users = with_polymorphic(User, [Teacher])
        results = db.session.query(Teacher).filter(Teacher.name.contains(term)).all()
        # results = Student.query.filter(Student.email.contains(term)).all()
        if not results:
            flash("No teachers found with that name.")
            return redirect('/')
        return render_template('search_results.html', results=results)
    else:
        return redirect(url_for('main.index'))


@bp_auth.route('/advanced_search/results', methods=['POST','GET'])
@login_required
def results():
    if request.method == 'POST':
        print("Works!")
        language = request.form['language_choice']
        if language == "":
            flash("Choose a language to search for")
            return redirect('/')
        users = with_polymorphic(User, [Teacher])
        #results = db.session.query(Teacher, Language).filter(Language.lang_id==Teacher.lang_id).filter(Language.name.contains(language)).all()
        results = Language.query.join(Teacher).with_entities(Language.lang_id, Language.name,
                                                   Teacher.name.label('user_name'), Teacher.email,
                                                   Teacher.rating).order_by(
            Language.lang_id).filter(Language.name.contains(language)).all()
        print("Works2!")
        print(results)
        if not results:
            flash("No teachers found for that language.")
            return redirect('/')
        return render_template("searchresults_language.html", results=results)
    else:
        return redirect(url_for('main.index'))

@bp_auth.route('/schedule_a_lesson', methods=['GET'])
@login_required
def schedule_a_lesson():
    return render_template("schedule_a_lesson.html")

@bp_auth.route('/lessons', methods=['GET'])
@login_required
def lessons():
    return render_template("lessons.html")

@bp_auth.route('/payment_details', methods=['GET', 'POST'])
@login_required
def payment_details():
    if request.method == "GET":
        return render_template("payment_details.html")
    elif request.method == "POST":
        form = request.form
        print(form)
        user = User.query.filter_by(email=current_user.email).first()
        cardnum = len(str(form.get('card_number')))
        cardtype = str(form.get('card_type'))
        expyr = int(form.get('expiry_year'))
        expmnth = int(form.get('expiry_month'))
        cvvlength = len(str(form.get('CVV')))
        if ((expyr == 20 and expmnth > 4) or (20 < expyr < 41)) \
                and ((cardnum == 19 and cvvlength == 3 and (
                cardtype == 'visa' or cardtype == 'master-card' or cardtype == 'discover' or cardtype == 'jcb')) or (cardnum == 17 and (cvvlength == 4 and cardtype == 'american-express')) or (cvvlength == 3 and cardtype == 'diners')):
            bankaccount = BankAccount(payment_type=form.get('card_type'), credit_card_num=form.get('card_number'))
            bankaccount.id = user.id
            bankaccount.card_id = random.randint(45678, 9876543456)
            db.session.add(bankaccount)
            db.session.commit()
            return redirect("/wallet")
        elif expyr > 40 or expyr < 20:
            flash('Please submit a valid expiry year (between 2020 and 2040).')
            return redirect("/payment_details")
        else:
            flash('Please submit a valid card number, CVV and expiry date.')
            return redirect("/payment_details")


@bp_auth.route('/wallet', methods=['GET', 'POST'])
@login_required
def wallet():
    user = User.query.filter_by(email=current_user.email).first()
    wallet = Wallet.query.join(User).filter(User.email == user.email).first()
    bankaccounts = BankAccount.query.join(User).filter(User.email == user.email).all()
    print(user, wallet.balance, bankaccounts)
    if request.method == "GET":
        return render_template("wallet.html", wallet_balance=wallet.balance, bankaccounts=bankaccounts)
    elif request.method == "POST":
        form = request.form

        if "buyamount" in form:
            amount = float(form.get('buyamount'))
            wallet.balance = round(amount + wallet.balance, 2)
        # wallet.balance = float("{0:.2f}".format(wallet.balance1) change

        else:
            amount = float(form.get('sellamount'))
            if wallet.balance - amount >= 0:
                wallet.balance = round(wallet.balance - amount, 2)
            else:
                flash('Error: You cannot sell more LangCoins than what is in your balance.')
        db.session.add(wallet)
        db.session.commit()
        return render_template("wallet.html", wallet_balance=wallet.balance, bankaccounts=bankaccounts)


@bp_auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
