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
from app.models import GuruModel, KelasModel, daftar_kelas


class TambahGuruForm(FlaskForm):
    nama = StringField("Nama lengkap", validators=[DataRequired(), Length(1, 64)])
    alamat = TextAreaField("Alamat lengkap", validators=[DataRequired()])
    nik = StringField("NIK anda", validators=[DataRequired(), Length(1, 24)])
    kelurahan = StringField("Kelurahan anda", validators=[Length(1, 24)])
    email = EmailField("Email anda", validators=[DataRequired(), Length(1, 64)])
    kecamatan = StringField("Kecamatan anda", validators=[Length(1, 24)])
    kabupaten = StringField("Kabupaten anda", validators=[Length(1, 24)])
    provinsi = StringField("Provinsi anda", validators=[Length(1, 24)])
    agama = SelectField(
        choices=[(g, g) for g in GuruModel.agama.property.columns[0].type.enums]
    )
    tempat_lahir = StringField(
        "Tempat lahir anda", validators=[DataRequired(), Length(1, 24)]
    )
    tanggal_lahir = StringField(
        "Tanggal lahir",
        validators=[DataRequired()],
        render_kw={"data-language": "en", "data-date-format": "dd MM yyyy"},
    )
    jabatan = SelectField(
        choices=[(g, g) for g in GuruModel.jabatan.property.columns[0].type.enums]
    )
    foto = FileField("Foto diri anda", validators=[DataRequired()])
    foto_ijazah = FileField("Scan ijazah anda", validators=[DataRequired()])
    pendidikan_terakhir = StringField(
        "Pendidikan terakhir anda", validators=[DataRequired(), Length(1, 24)]
    )
    jenis_kelamin = SelectField(
        choices=[(g, g) for g in GuruModel.jenis_kelamin.property.columns[0].type.enums]
    )
    tahun_masuk = StringField(
        "Tahun masuk anda",
        validators=[DataRequired()],
        render_kw={"data-language": "en", "data-date-format": "dd MM yyyy"},
    )
    golongan = SelectField(
        choices=[(g, g) for g in GuruModel.golongan.property.columns[0].type.enums]
    )
    kelas = QuerySelectField(
        "Kelas",
        query_factory=daftar_kelas,
        get_label="ruang",
        get_pk=lambda a: a.id,
        blank_text="Pilih kelas",
        allow_blank=True,
        validators=[DataRequired()],
    )
    submit = SubmitField("Tambahkan")

    def validate_nik(self, nik):
        nik = GuruModel.query.filter_by(nik=self.nik.data).first()
        if nik is not None:
            raise ValueError("NIK sudah terdaftar.")

    def validate_email(self, nik):
        email = GuruModel.query.filter_by(email=self.email.data).first()
        if email is not None:
            raise ValueError("Email sudah terdaftar.")


class TambahKelasForm(FlaskForm):
    ruang = StringField(
        "Ruang Kelas",
        validators=[DataRequired(), Length(1, 4)],
        render_kw={"placeholder": "Ruang kelas"},
    )
    submit = SubmitField("Simpan")

    def validate_ruang(self, ruang):
        ruang = KelasModel.query.filter_by(ruang=self.ruang.data.upper()).first()
        if ruang is not None:
            raise ValueError("Ruang kelas sudah ada.")

