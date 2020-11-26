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
from flask import flash
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, URL
from app.models import *
from flask_login import current_user


class GuruForm(FlaskForm):
    nama = StringField("Nama *", validators=[DataRequired(), Length(1, 64)])
    alamat = TextAreaField("Alamat *", validators=[DataRequired()])
    nik = StringField(
        "Nomor Induk Kependudukan *", validators=[DataRequired(), Length(1, 24)]
    )
    nip = StringField("Nomor Induk Pegawai", validators=[Length(0, 24)])
    email = EmailField(
        "Email *", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    kelurahan = StringField("Kelurahan *", validators=[Length(1, 24)])
    kecamatan = StringField("Kecamatan *", validators=[Length(1, 24)])
    kabupaten = StringField("Kabupaten *", validators=[Length(1, 24)])
    provinsi = StringField("Provinsi *", validators=[Length(1, 24)])
    agama = SelectField(
        "Agama *",
        choices=[(g, g) for g in GuruModel.agama.property.columns[0].type.enums],
    )
    tempat_lahir = StringField(
        "Tempat Lahir *", validators=[DataRequired(), Length(1, 24)]
    )
    tanggal_lahir = StringField(
        "Tanggal Lahir *",
        validators=[DataRequired()],
        render_kw={"data-language": "en", "data-date-format": "dd MM yyyy"},
    )
    pendidikan_terakhir = StringField(
        "Pendidikan Terakhir *", validators=[DataRequired(), Length(1, 24)]
    )
    jenis_kelamin = SelectField(
        "Jenis Kelamin *",
        choices=[
            (g, g) for g in GuruModel.jenis_kelamin.property.columns[0].type.enums
        ],
    )
    tahun_masuk = StringField(
        "Tahun Masuk TK *",
        validators=[DataRequired()],
        render_kw={"data-language": "en", "data-date-format": "dd MM yyyy"},
    )
    golongan = SelectField(
        "Golongan *",
        choices=[(g, g) for g in GuruModel.golongan.property.columns[0].type.enums],
    )
    submit = SubmitField("Simpan")


class TambahGuruForm(GuruForm):
    kelas = QuerySelectField(
        "Mengajar Kelompok *",
        query_factory=daftar_kelas,
        get_label="ruang",
        get_pk=lambda a: a.id,
        validators=[DataRequired()],
    )
    jabatan = SelectField(
        "Jabatan *",
        choices=[(g, g) for g in GuruModel.jabatan.property.columns[0].type.enums],
    )
    foto = FileField(
        "Foto Diri *",
        validators=[
            DataRequired(),
            FileAllowed(["png", "jpg", "jpeg", "gif"], "Images Only"),
        ],
    )
    foto_ijazah = FileField(
        "Scan Ijazah *", validators=[DataRequired(), FileAllowed(["pdf"], "Pdf Only")]
    )

    def validate_nip(self, nik):
        if self.nip.data == "":
            self.nip.data = ""
        else:
            data = GuruModel.query.filter_by(nip=self.nip.data).first()
            if data is not None:
                raise ValidationError("NIP sudah terdaftar.")

    def validate_nik(self, nik):
        nik = GuruModel.query.filter_by(nik=self.nik.data).first()
        if nik is not None:
            raise ValidationError("NIK sudah terdaftar.")

    def validate_email(self, nik):
        email = UserModel.query.filter_by(email=self.email.data).first()
        if email is not None:
            raise ValidationError("Email sudah terdaftar.")

    def validate_jabatan(self, jabatan):
        jabatan = GuruModel.query.filter_by(jabatan=self.jabatan.data).first()
        if jabatan is not None and jabatan.jabatan == "Kepala Sekolah":
            raise ValidationError("Kepala sekolah sudah terdaftar.")


class RubahGuruForm(GuruForm):
    kelas = QuerySelectField(
        "Mengajar Kelompok *",
        query_factory=daftar_kelas,
        get_label="ruang",
        get_pk=lambda a: a.id,
        validators=[DataRequired()],
    )
    jabatan = SelectField(
        "Jabatan *",
        choices=[(g, g) for g in GuruModel.jabatan.property.columns[0].type.enums],
    )
    foto = FileField("Foto Diri *")
    foto_ijazah = FileField("Scan Ijazah *")

    def validate_jabatan(self, jabatan):
        jabatan = GuruModel.query.filter_by(jabatan=self.jabatan.data).first()
        if jabatan is not None and jabatan.jabatan == "Kepala Sekolah":
            raise ValidationError("Kepala sekolah sudah terdaftar.")


class RubahProfileGuruForm(GuruForm):
    foto = FileField("Foto Diri *")
    foto_ijazah = FileField("Scan Ijazah *", render_kw={"accept": "application/pdf"})


class AddPassword(FlaskForm):
    password = PasswordField("Kata Sandi")
    submit = SubmitField("Simpan")


class UbahPasswordDiriForm(FlaskForm):
    password = PasswordField(
        "Kata Sandi Lama", validators=[DataRequired(), Length(5, 24)]
    )
    new_password = PasswordField(
        "Kata Sandi Baru", validators=[DataRequired(), Length(5, 24)]
    )
    password_again = PasswordField(
        "Konfirmasi Kata Sandi Baru",
        validators=[
            DataRequired(),
            EqualTo("new_password", "Kata sandi harus sama."),
            Length(5, 24),
        ],
    )
    submit = SubmitField("Simpan")

    def validate_password(self, password):
        data = UserModel.query.filter_by(id=current_user.id).first()
        if data.verify_password(self.password.data) == False:
            raise ValidationError("Kata sandi lama salah.")


class TambahKelasForm(FlaskForm):
    ruang = StringField(
        "Kelompok *",
        validators=[DataRequired(), Length(1, 4)],
    )
    submit = SubmitField("Simpan")

    def validate_ruang(self, ruang):
        ruang = KelasModel.query.filter_by(ruang=self.ruang.data.upper()).first()
        if ruang is not None:
            raise ValidationError(
                "Kelompok {} sudah ada.".format(self.ruang.data.upper())
            )


class AkunForm(FlaskForm):
    email = EmailField(
        "Email", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(1, 24)],
        render_kw={"class": "form-control"},
    )
    submit = SubmitField("Simpan", render_kw={"class": "btn btn-primary"})


class MuridForm(FlaskForm):
    nomor_induk = StringField(
        "Nomor Induk *",
        validators=[DataRequired(), Length(1, 5)],
        render_kw={"type": "number"},
    )
    nama_panggilan = StringField(
        "Nama Panggilan *", validators=[DataRequired(), Length(1, 25)]
    )
    email = EmailField("Email *", validators=[DataRequired(), Length(1, 64)])
    anak_ke = StringField(
        "Anak Ke *",
        validators=[DataRequired(), Length(1, 2)],
        render_kw={"type": "number"},
    )
    nama = StringField("Nama *", validators=[DataRequired(), Length(1, 64)])
    alamat = TextAreaField("Alamat *", validators=[DataRequired()])
    dusun = StringField("Dusun *", validators=[Length(1, 24)])
    kelurahan = StringField("Kelurahan *", validators=[Length(1, 24)])
    kecamatan = StringField("Kecamatan *", validators=[Length(1, 24)])
    kabupaten = StringField("Kabupaten *", validators=[Length(1, 24)])
    provinsi = StringField("Provinsi *", validators=[Length(1, 24)])
    agama = SelectField(
        "Agama *",
        choices=[(g, g) for g in GuruModel.agama.property.columns[0].type.enums],
    )
    tempat_lahir = StringField(
        "Tempat Lahir *", validators=[DataRequired(), Length(1, 24)]
    )
    tanggal_lahir = StringField(
        "Tanggal Lahir *",
        validators=[DataRequired()],
        render_kw={"data-language": "en", "data-date-format": "dd MM yyyy"},
    )
    nama_ibu_kandung = StringField(
        "Nama Ibu Kandung *", validators=[DataRequired(), Length(1, 64)]
    )
    jenis_kelamin = SelectField(
        choices=[(g, g) for g in GuruModel.jenis_kelamin.property.columns[0].type.enums]
    )
    tahun_pelajaran = StringField(
        "Tahun Pelajaran *",
        validators=[DataRequired()],
        render_kw={"data-language": "en", "data-date-format": "dd MM yyyy"},
    )
    kelas = QuerySelectField(
        "Kelompok *",
        query_factory=daftar_kelas,
        get_label="ruang",
        get_pk=lambda a: a.id,
        blank_text="Kelompok",
        allow_blank=True,
        validators=[DataRequired()],
    )
    submit = SubmitField("Simpan")


class TambahMuridForm(MuridForm):
    lulus = BooleanField(
        "Lulus/ Belum", render_kw={"class": "form-control form-control-sm"}
    )
    foto_diri = FileField("Foto Diri *", validators=[DataRequired()])

    def validate_nomor_induk(self, nomor_induk):
        nomor_induk = MuridModel.query.filter_by(
            nomor_induk=self.nomor_induk.data
        ).first()
        if nomor_induk is not None:
            raise ValidationError("Nomor induk yang digunakan sudah terdaftar.")

    def validate_email(self, email):
        email = UserModel.query.filter_by(email=self.email.data).first()
        if email is not None:
            raise ValidationError("Email yang anda gunakan sudah terdaftar.")


class RubahMuridForm(MuridForm):
    lulus = BooleanField(
        "Lulus/ Belum", render_kw={"class": "form-control form-control-sm"}
    )
    foto_diri = FileField("Foto Diri *")


class WaliMurid(FlaskForm):
    nama = StringField("Nama *", validators=[DataRequired(), Length(1, 64)])
    alamat = TextAreaField("Alamat *", validators=[DataRequired()])
    kelurahan = StringField("Kelurahan *", validators=[Length(1, 24)])
    kecamatan = StringField("Kecamatan *", validators=[Length(1, 24)])
    kabupaten = StringField("Kabupaten *", validators=[Length(1, 24)])
    provinsi = StringField("Provinsi *", validators=[Length(1, 24)])
    agama = SelectField(
        "Agama *",
        choices=[(g, g) for g in WaliMuridModel.agama.property.columns[0].type.enums],
    )
    tempat_lahir = StringField(
        "Tempat Lahir *", validators=[DataRequired(), Length(1, 24)]
    )
    tanggal_lahir = StringField(
        "Tanggal Lahir *",
        validators=[DataRequired()],
        render_kw={"data-language": "en", "data-date-format": "dd MM yyyy"},
    )
    pekerjaan = StringField("Pekerjaan *", validators=[DataRequired(), Length(1, 24)])
    jenis_kelamin = SelectField(
        "Jenis Kelamin *",
        choices=[
            (g, g) for g in WaliMuridModel.jenis_kelamin.property.columns[0].type.enums
        ],
    )
    nomor_telepon = StringField(
        "Nomor Telepon *",
        validators=[DataRequired()],
        render_kw={"type": "number"},
    )
    submit = SubmitField("Simpan")


class TambahUbahWaliMurid(WaliMurid):
    murid = QuerySelectField(
        "Nama Anak *",
        query_factory=daftar_murid,
        get_label="nama",
        get_pk=lambda a: a.id,
        blank_text="Nama Anak",
        allow_blank=True,
        validators=[DataRequired()],
    )


class TambahUbahWaliMuridUser(WaliMurid):
    murid = QuerySelectField(
        "Nama Anak *",
        query_factory=daftar_murid_user,
        get_label="nama",
        get_pk=lambda a: a.id,
        blank_text="Nama Anak",
        allow_blank=True,
        validators=[DataRequired()],
    )


class TambahUbahProfileForm(FlaskForm):
    nama_lembaga = StringField(
        "Nama Lembaga *", validators=[DataRequired(), Length(1, 120)]
    )
    kode_pos = StringField("Kode Pos *", validators=[DataRequired(), Length(1, 10)])
    kelurahan = StringField("Kelurahan *", validators=[Length(1, 24), DataRequired()])
    kecamatan = StringField("Kecamatan *", validators=[Length(1, 24), DataRequired()])
    kabupaten = StringField("Kabupaten *", validators=[Length(1, 24), DataRequired()])
    provinsi = StringField("Provinsi *", validators=[Length(1, 24), DataRequired()])
    no_statistik = StringField(
        "No. Statitistik *", validators=[DataRequired(), Length(1, 60)]
    )
    akte_notaris = StringField(
        "Akte Notaris *", validators=[DataRequired(), Length(0, 60)]
    )
    kegiatan_belajar = StringField(
        "Kegiatan Belajar *", validators=[DataRequired(), Length(1, 20)]
    )
    tahun_berdiri = StringField(
        "Tahun Berdiri *",
        validators=[DataRequired()],
        render_kw={"data-language": "en", "data-date-format": "dd MM yyyy"},
    )
    status_tk = StringField("Status TK *", validators=[DataRequired(), Length(1, 10)])
    no_izin_operasional = StringField(
        "No. Izin Operasional *", validators=[DataRequired(), Length(1, 46)]
    )
    no_izin_pendirian = StringField(
        "No. Izin Pendirian *", validators=[DataRequired(), Length(1, 46)]
    )
    kurikulum = StringField("Kurikulum *", validators=[DataRequired(), Length(1, 10)])
    no_telepon = StringField(
        "Nomor Telepon *", validators=[DataRequired(), Length(0, 24)]
    )
    website = StringField(
        "Website *", validators=[DataRequired(), Length(1, 64), DataRequired()]
    )
    instagram = StringField("Instagram *", validators=[URL(), DataRequired()])
    facebook = StringField("Facebook *", validators=[URL(), DataRequired()])
    twitter = StringField("Twitter *", validators=[URL(), DataRequired()])
    email = EmailField("Email *", validators=[DataRequired(), Length(1, 64)])
    visi_misi = TextAreaField("Visi dan Misi *", validators=[DataRequired()])
    alamat = TextAreaField("Alamat *", validators=[DataRequired()])
    submit = SubmitField("Simpan")


class TambahDataSekolahForm(FlaskForm):
    judul = StringField("Judul *", validators=[DataRequired(), Length(1, 60)])
    deskripsi = TextAreaField("Deskripsi")
    dokumen = FileField("Dokumen *", validators=[DataRequired()])
    submit = SubmitField("Simpan")

    def validate_judul(self, judul):
        judul = DataSekolahModel.query.filter_by(judul=self.judul.data).first()
        if judul is not None:
            raise ValueError("Judul data sekolah sudah ada.")


class UbahDataSekolahForm(FlaskForm):
    judul = StringField("Judul *", validators=[DataRequired(), Length(1, 60)])
    deskripsi = TextAreaField("Deskripsi")
    dokumen = FileField("Dokumen *")
    submit = SubmitField("Simpan")


class TambahUbahBeritaForm(FlaskForm):
    judul = StringField("Judul *", validators=[DataRequired(), Length(1, 120)])
    deskripsi = TextAreaField("Deskripsi berita")
    tampilkan = BooleanField("Tampilkan berita")
    gambar = FileField("Background")
    dokumen = FileField("Dokumen")
    submit = SubmitField("Simpan")

    def validate_judul(self, judul):
        data = BeritaModel.query.filter_by(judul=self.judul.data).first()
        if data is not None:
            raise ValidationError("Judul yang dimasukkan sudah ada.")


class TambahElearningForm(FlaskForm):
    dokumen = FileField("Dokumen *", validators=[DataRequired()])
    deskripsi = TextAreaField("Deskripsi")
    judul = StringField("Judul *", validators=[DataRequired(), Length(1, 120)])
    kelas = QuerySelectField(
        "Kelompok *",
        query_factory=daftar_kelas,
        get_label="ruang",
        get_pk=lambda a: a.id,
        blank_text="Kelompok",
        allow_blank=True,
        validators=[DataRequired()],
    )
    submit = SubmitField("Simpan")

    def validate_judul(self, judul):
        data = ElearningModel.query.filter(
            ElearningModel.judul == self.judul.data
        ).first()
        if data is not None:
            raise ValidationError("Data yang dimasukkan sudah ada.")


class UbahElearningForm(FlaskForm):
    dokumen = FileField("Upload *")
    deskripsi = TextAreaField("Deskripsi")
    judul = StringField("Judul *", validators=[DataRequired(), Length(1, 120)])
    kelas = QuerySelectField(
        "Kelompok *",
        query_factory=daftar_kelas,
        get_label="ruang",
        get_pk=lambda a: a.id,
        blank_text="Pilih kelas",
        allow_blank=True,
        validators=[DataRequired()],
    )
    submit = SubmitField("Simpan")


class TambahElearningGuruForm(FlaskForm):
    dokumen = FileField("Upload *", validators=[DataRequired()])
    deskripsi = TextAreaField("Deskripsi")
    judul = StringField("Judul *", validators=[DataRequired(), Length(1, 120)])
    submit = SubmitField("Simpan")


class UbahElearningGuruForm(FlaskForm):
    dokumen = FileField("Upload *")
    deskripsi = TextAreaField("Deskripsi")
    judul = StringField("Judul *", validators=[DataRequired(), Length(1, 120)])
    submit = SubmitField("Simpan")


class TambahJadwalForm(FlaskForm):
    mata_pelajaran = StringField(
        "Mata Pelajaran *", validators=[Length(2, 64), DataRequired()]
    )
    jam = StringField("Jam Mulai *", validators=[DataRequired()])
    jam_end = StringField("Jam Selesai *", validators=[DataRequired()])
    hari = SelectField(
        "Hari *",
        choices=[(g, g) for g in JadwalKelasModel.hari.property.columns[0].type.enums],
    )
    submit = SubmitField("Simpan")


class TambahAdminJadwalForm(TambahJadwalForm):
    kelas = QuerySelectField(
        "Kelompok *",
        query_factory=daftar_kelas,
        get_label="ruang",
        get_pk=lambda a: a.id,
        blank_text="Kelompok",
        allow_blank=True,
        validators=[DataRequired()],
    )


class TambahNilaiMuridForm(FlaskForm):
    deskripsi = TextAreaField("Deskripsi Penilaian *")
    aspek_penilaian = SelectField(
        "Aspek Penilaian *",
        choices=[
            (g, g) for g in NilaiModel.aspek_penilaian.property.columns[0].type.enums
        ],
    )
    semester = SelectField(
        "Semester",
        choices=[(g, g) for g in NilaiModel.semester.property.columns[0].type.enums],
    )
    tahun_pelajaran = StringField(
        "Tahun Pelajaran *",
        validators=[DataRequired(), Length(5, 10)],
    )
    submit = SubmitField("Simpan")


class TambahUbahPrestasiForm(FlaskForm):
    nama = StringField("Nama *", validators=[DataRequired(), Length(1, 64)])
    kategori = StringField("Kategori *", validators=[DataRequired(), Length(1, 24)])
    tingkat = StringField("Tingkat Lomba *", validators=[DataRequired(), Length(1, 48)])
    juara = StringField("Juara *", validators=[Length(1, 24)])
    tahun = StringField("Tahun *", validators=[DataRequired(), Length(1, 24)])
    submit = SubmitField("Simpan")
