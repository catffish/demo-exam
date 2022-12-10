from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app.forms import LoginForm, RegistrationForm, CreateOfferForm, CreateCategoryForm
from app.models import User, Category, Offer
from datetime import datetime
from app import db, app
import os

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
            category=Category.query.filter_by(name=form.category.data.lower()).first()
            if category is None:
                return redirect(url_for('index'))
            else:
                pass
            offer=Offer(name=form.name.data, description=form.description.data, category=form.category.data.lower(), photo='', author=current_user, time=datetime.utcnow(), status="новая")
            db.session.add(offer)
            db.session.commit()
            f = request.files['photo']
            f.filename = "offerID"+str(offer.id)+'.png'
            path=os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
            f.save(path)
            offer.photo=f.filename
            db.session.commit()
            flash('Заявка создана')
            return redirect(url_for('profile'))
        offers=Offer.query.filter_by(user=current_user.id)
    return render_template('profile.html', name='Профиль', form=form, offers=offers)

@app.route('/delete_offer/<id>', methods=['GET', 'POST'])
@login_required
def delete_offer(id):
    offer=Offer.query.filter_by(id=id).first()
    if current_user.id==offer.user and offer.status=="новая":
        Offer.query.filter_by(id=id).delete()
        f=os.path.join(app.config['UPLOAD_FOLDER'], offer.photo)
        os.remove(f)
        db.session.commit()
        return redirect(url_for('profile'))
    elif current_user.id!=offer.user:
        flash('У вас нет прав удалить эту заявку')
        return (redirect(url_for('profile')))
    else:
        flash('Нельзя удалить отклонённую или решённую заявку')
        return (redirect(url_for('profile')))

@app.route('/accept_offer/<id>', methods=["GET", "POST"])
@login_required
def accept_offer(id):
    offer = Offer.query.filter_by(id=id).first()
    if current_user.username=="admin" and offer.status=="новая":
        offer.status = 'решена'
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        flash("у вас нет прав изменить статус этой заявки")
        return redirect(url_for('profile'))

@app.route('/reject_offer/', methods=["GET", "POST"])
@login_required
def reject_offer():
    offer = Offer.query.filter_by(id=request.form['id']).first()
    if current_user.username=="admin" and offer.status=="новая":
        reason=request.form['reason']
        offer.status = 'отклонена'
        offer.reason=reason
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        flash("У вас нет прав изменить статус этой заявки")
        return redirect(url_for('profile'))
    