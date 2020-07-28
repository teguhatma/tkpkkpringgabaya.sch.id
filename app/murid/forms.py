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
from app.models import MuridModel, WaliMuridModel


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


class MuridGantiProfileForm(FlaskForm):
    nama_panggilan = StringField(
        "Nama panggilan", validators=[DataRequired(), Length(1, 25)]
    )
    anak_ke = StringField(
        "Anak ke",
        validators=[DataRequired(), Length(1, 2)],
        render_kw={"type": "number"},
    )
    nama = StringField("Nama lengkap", validators=[DataRequired(), Length(1, 64)])
    alamat = TextAreaField("Alamat lengkap", validators=[DataRequired()])
    kelurahan = StringField("Kelurahan", validators=[Length(1, 24)])
    kecamatan = StringField("Kecamatan", validators=[Length(1, 24)])
    kabupaten = StringField("Kabupaten", validators=[Length(1, 24)])
    provinsi = StringField("Provinsi", validators=[Length(1, 24)])
    agama = SelectField(
        choices=[(g, g) for g in MuridModel.agama.property.columns[0].type.enums]
    )
    tempat_lahir = StringField(
        "Tempat lahir", validators=[DataRequired(), Length(1, 24)]
    )
    tanggal_lahir = StringField(
        "Tanggal lahir",
        validators=[DataRequired()],
        render_kw={"data-language": "en", "data-date-format": "dd MM yyyy",},
    )
    nama_ibu_kandung = StringField(
        "Nama ibu kandung", validators=[DataRequired(), Length(1, 64)]
    )
    jenis_kelamin = SelectField(
        choices=[
            (g, g) for g in MuridModel.jenis_kelamin.property.columns[0].type.enums
        ]
    )

    submit = SubmitField("Simpan")


class MuridGantiProfileWaliForm(FlaskForm):
    nama = StringField("Nama", validators=[DataRequired(), Length(3, 64)])
    agama = SelectField(
        choices=[(g, g) for g in WaliMuridModel.agama.property.columns[0].type.enums]
    )
    jenis_kelamin = SelectField(
        choices=[
            (g, g) for g in WaliMuridModel.jenis_kelamin.property.columns[0].type.enums
        ]
    )
    tempat_lahir = StringField(
        "Tempat Lahir Anda",
        validators=[DataRequired(), Length(1, 24)],
        render_kw={"data-language": "en", "data-date-format": "dd MM yyyy"},
    )
    tanggal_lahir = StringField("Tanggal Lahir Anda", validators=[DataRequired()])
    pekerjaan = StringField("Pekerjaan", validators=[DataRequired()])
    nomor_telepon = StringField("Nomor Telepon", validators=[DataRequired()])
    alamat = TextAreaField(
        "Alamat lengkap", validators=[DataRequired(), Length(1, 120)]
    )
    kelurahan = StringField("Kelurahan", validators=[DataRequired(), Length(1, 24)])
    kecamatan = StringField("Kecamatan", validators=[DataRequired(), Length(1, 24)])
    kabupaten = StringField("Kabupaten", validators=[DataRequired(), Length(1, 24)])
    provinsi = StringField("Provinsi", validators=[DataRequired(), Length(1, 24)])
    submit = SubmitField("Simpan")
