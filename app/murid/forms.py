from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import (
    StringField,
    SubmitField,
    SelectField,
    TextAreaField,
    BooleanField,
    PasswordField,
    IntegerField,
)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, EqualTo


class MuridGantiPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), Length(5, 24)])
    new_password = PasswordField(
        "New Password", validators=[DataRequired(), Length(5, 24)]
    )
    password_again = PasswordField(
        "Verify New Password",
        validators=[
            DataRequired(),
            EqualTo("new_password", "Password must match"),
            Length(5, 24),
        ],
    )
    submit = SubmitField("Simpan")

