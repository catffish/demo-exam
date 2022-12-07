from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, CreateOfferForm, CreateCategoryForm
from app.models import User, Category, Offer
from datetime import datetime
from app import db, app

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    offers=Offer.query.all()
    return render_template("index.html", offers=offers)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('registration.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.username=="admin":
        form=CreateCategoryForm()
        if form.validate_on_submit():
            category=Category(name=form.name.data.lower())
            db.session.add(category)
            db.session.commit()
            flash('Категория создана')
            return redirect(url_for('profile'))
        offers=Offer.query.all()
    else:
        form=CreateOfferForm()
        if form.validate_on_submit():
            print("Возврат", form.submit.data)
            category=Category.query.filter_by(name=form.category.data.lower()).first()
            if category is None:
                return redirect(url_for('index'))
            else:
                pass
            offer=Offer(name=form.name.data, description=form.description.data, category=form.category.data.lower(), author=current_user, time=datetime.utcnow(), status="новая")
            db.session.add(offer)
            db.session.commit()
            flash('Заявка создана')
            return redirect(url_for('profile'))
        offers=Offer.query.filter_by(user=current_user.id)
    return render_template('profile.html', name='Профиль', form=form, offers=offers)