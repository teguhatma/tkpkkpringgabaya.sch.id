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
from app.models import GuruModel, KelasModel, daftar_kelas, PegawaiModel, MuridModel


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

    def validate_jabatan(self, jabatan):
        jabatan = GuruModel.query.filter_by(jabatan=self.jabatan.data).first()
        if jabatan is not None:
            raise ValueError("Kepala sekolah diperbolehkan hanya satu.")


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


class RubahGuruForm(FlaskForm):
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
    foto = FileField("Foto diri anda")
    foto_ijazah = FileField("Scan ijazah anda")
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
    email_hidden = StringField("Email hidden", render_kw={"type": "hidden"})
    nik_hidden = StringField("NIK hidden", render_kw={"type": "hidden"})
    jabatan_hidden = StringField("Jabatan hidden", render_kw={"type": "hidden"})
    submit = SubmitField("Tambahkan")

    def validate_nik(self, nik):
        nik = GuruModel.query.filter_by(nik=self.nik_hidden.data).first()
        for guru in GuruModel.query.all():
            if guru.nik != nik.nik:
                if guru.nik == self.nik.data:
                    raise ValueError("NIK sudah terdaftar.")

    def validate_email(self, nik):
        email = GuruModel.query.filter_by(email=self.email_hidden.data).first()
        for guru in GuruModel.query.all():
            if guru.email != email.email:
                if guru.email == self.email.data:
                    raise ValueError("Email sudah terdaftar.")

    def validate_jabatan(self, nik):
        jabatan = GuruModel.query.filter_by(jabatan=self.jabatan_hidden.data).first()
        for guru in GuruModel.query.all():
            if guru.jabatan != jabatan.jabatan:
                if guru.jabatan == self.jabatan.data:
                    raise ValueError("Kepala sekolah hanya diperbolehkan satu.")


class AkunForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), Length(1, 24)])
    submit = SubmitField("Simpan")


class TambahPegawaiForm(FlaskForm):
    nama = StringField("Nama lengkap", validators=[DataRequired(), Length(1, 64)])
    alamat = TextAreaField("Alamat lengkap", validators=[DataRequired()])
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
    foto = FileField("Foto diri anda", validators=[DataRequired()])
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
    submit = SubmitField("Tambahkan")

    def validate_email(self, nik):
        email = GuruModel.query.filter_by(email=self.email.data).first()
        if email is not None:
            raise ValueError("Email sudah terdaftar.")


class RubahPegawaiForm(FlaskForm):
    nama = StringField("Nama lengkap", validators=[DataRequired(), Length(1, 64)])
    alamat = TextAreaField("Alamat lengkap", validators=[DataRequired()])
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
    foto = FileField("Foto diri anda")
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
    email_hidden = StringField("Email hidden", render_kw={"type": "hidden"})
    submit = SubmitField("Tambahkan")

    def validate_email(self, nik):
        email = PegawaiModel.query.filter_by(email=self.email_hidden.data).first()
        for pegawai in PegawaiModel.query.all():
            if pegawai.email != email.email:
                if pegawai.email == self.email.data:
                    raise ValueError("Email sudah terdaftar.")


class TambahMuridForm(FlaskForm):
    nomor_induk = StringField(
        "Nomor induk",
        validators=[DataRequired(), Length(1, 5)],
        render_kw={"type": "number"},
    )
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
        choices=[(g, g) for g in GuruModel.agama.property.columns[0].type.enums]
    )
    tempat_lahir = StringField(
        "Tempat lahir", validators=[DataRequired(), Length(1, 24)]
    )
    tanggal_lahir = StringField(
        "Tanggal lahir",
        validators=[DataRequired()],
        render_kw={"data-language": "en", "data-date-format": "dd MM yyyy"},
    )
    lulus = BooleanField(
        "Sudah lulus?", render_kw={"class": "form-control form-control-sm"}
    )
    nama_ibu_kandung = StringField(
        "Nama ibu kandung", validators=[DataRequired(), Length(1, 64)]
    )
    foto_diri = FileField("Foto diri", validators=[DataRequired()])
    jenis_kelamin = SelectField(
        choices=[(g, g) for g in GuruModel.jenis_kelamin.property.columns[0].type.enums]
    )
    tahun_pelajaran = StringField(
        "Tahun Pelajaran",
        validators=[DataRequired()],
        render_kw={"data-language": "en", "data-date-format": "dd MM yyyy"},
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

    def validate_nomor_induk(self, nik):
        nomor_induk = MuridModel.query.filter_by(
            nomor_induk=self.nomor_induk.data
        ).first()
        if nomor_induk is not None:
            raise ValueError("Nomor induk sudah terdaftar.")


class RubahMuridForm(FlaskForm):
    nomor_induk_hidden = StringField("Nomor induk hidden", render_kw={"type": "hidden"})
    nomor_induk = StringField(
        "Nomor induk",
        validators=[DataRequired(), Length(1, 5)],
        render_kw={"type": "number"},
    )
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
        choices=[(g, g) for g in GuruModel.agama.property.columns[0].type.enums]
    )
    tempat_lahir = StringField(
        "Tempat lahir", validators=[DataRequired(), Length(1, 24)]
    )
    tanggal_lahir = StringField(
        "Tanggal lahir",
        validators=[DataRequired()],
        render_kw={"data-language": "en", "data-date-format": "dd MM yyyy"},
    )
    lulus = BooleanField(
        "Sudah lulus?", render_kw={"class": "form-control form-control-sm"}
    )
    nama_ibu_kandung = StringField(
        "Nama ibu kandung", validators=[DataRequired(), Length(1, 64)]
    )
    foto_diri = FileField("Foto diri")
    jenis_kelamin = SelectField(
        choices=[(g, g) for g in GuruModel.jenis_kelamin.property.columns[0].type.enums]
    )
    tahun_pelajaran = StringField(
        "Tahun Pelajaran",
        validators=[DataRequired()],
        render_kw={"data-language": "en", "data-date-format": "dd MM yyyy"},
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

    def validate_nomor_induk(self, nik):
        nomor_induk = MuridModel.query.filter_by(
            nomor_induk=self.nomor_induk_hidden.data
        ).first()
        for murid in MuridModel.query.all():
            if murid.nomor_induk != nomor_induk.nomor_induk:
                if murid.nomor_induk == self.nomor_induk.data:
                    raise ValueError("Nomor induk sudah terdaftar.")
