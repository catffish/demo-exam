from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')

class RegistrationForm(FlaskForm):
    fio = StringField('fio', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    personaldata = BooleanField('')
    submit = SubmitField('Register', validators=[DataRequired()])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class CreateOfferForm(FlaskForm):
    name=StringField('name', validators=[DataRequired()])
    description=TextAreaField('description')
    category=StringField('category', validators=[DataRequired()])
    submit = SubmitField('Добавить заявку', validators=[DataRequired()])

class CreateCategoryForm(FlaskForm):
    name=StringField('name', validators=[DataRequired()])
    submit = SubmitField('Создать категорию', validators=[DataRequired()])
