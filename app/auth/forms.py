from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import EmailField


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Length(1, 64) ])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
