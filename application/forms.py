from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length



class ContactForm(FlaskForm):
    name = StringField(label='Your Name', validators=[Length(min=1, max=255)])
    email = StringField(validators=[DataRequired(), Email()])
    subject = StringField(validators=[Length(min=1)])
    message = StringField(validators=[Length(min=1)])



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')

