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
from app.models import (
    GuruModel,
    KelasModel,
    daftar_kelas,
    MuridModel,
    daftar_murid,
    DataSekolahModel,
    JadwalKelasModel,
    NilaiModel,
    WaliMuridModel,
)


class TambahGuruForm(FlaskForm):
    nama = StringField("Nama lengkap", validators=[DataRequired(), Length(1, 64)])
    alamat = TextAreaField("Alamat lengkap", validators=[DataRequired()])
    nik = StringField("NIK", validators=[DataRequired(), Length(1, 24)])
    kelurahan = StringField("Kelurahan", validators=[Length(1, 24)])
    email = EmailField("Email", validators=[DataRequired(), Length(1, 64)])
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
    jabatan = SelectField(
        choices=[(g, g) for g in GuruModel.jabatan.property.columns[0].type.enums]
    )
    foto = FileField("Foto diri", validators=[DataRequired()])
    foto_ijazah = FileField("Scan ijazah", validators=[DataRequired()])
    pendidikan_terakhir = StringField(
        "Pendidikan terakhir", validators=[DataRequired(), Length(1, 24)]
    )
    jenis_kelamin = SelectField(
        choices=[(g, g) for g in GuruModel.jenis_kelamin.property.columns[0].type.enums]
    )
    tahun_masuk = StringField(
        "Tahun masuk TK",
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
        if jabatan is not None and jabatan.jabatan == "Kepala Sekolah":
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
    nik = StringField("NIK", validators=[DataRequired(), Length(1, 24)])
    kelurahan = StringField("Kelurahan", validators=[Length(1, 24)])
    email = EmailField("Email", validators=[DataRequired(), Length(1, 64)])
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
    jabatan = SelectField(
        choices=[(g, g) for g in GuruModel.jabatan.property.columns[0].type.enums]
    )
    foto = FileField("Foto diri")
    foto_ijazah = FileField("Scan ijazah")
    pendidikan_terakhir = StringField(
        "Pendidikan terakhir", validators=[DataRequired(), Length(1, 24)]
    )
    jenis_kelamin = SelectField(
        choices=[(g, g) for g in GuruModel.jenis_kelamin.property.columns[0].type.enums]
    )
    tahun_masuk = StringField(
        "Tahun masuk TK",
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
    dusun = StringField("Dusun", validators=[Length(1, 24)])
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
    dusun = StringField("Dusun", validators=[Length(1, 24)])
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
        choices=[
            (g, g) for g in MuridModel.jenis_kelamin.property.columns[0].type.enums
        ]
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


class TambahUbahWaliForm(FlaskForm):
    nama = StringField("Nama lengkap", validators=[DataRequired(), Length(1, 64)])
    alamat = TextAreaField("Alamat lengkap", validators=[DataRequired()])
    kelurahan = StringField("Kelurahan", validators=[Length(1, 24)])
    kecamatan = StringField("Kecamatan", validators=[Length(1, 24)])
    kabupaten = StringField("Kabupaten", validators=[Length(1, 24)])
    provinsi = StringField("Provinsi", validators=[Length(1, 24)])
    agama = SelectField(
        choices=[(g, g) for g in WaliMuridModel.agama.property.columns[0].type.enums]
    )
    tempat_lahir = StringField(
        "Tempat lahir", validators=[DataRequired(), Length(1, 24)]
    )
    tanggal_lahir = StringField(
        "Tanggal lahir",
        validators=[DataRequired()],
        render_kw={"data-language": "en", "data-date-format": "dd MM yyyy"},
    )
    pekerjaan = StringField("Pekerjaan", validators=[DataRequired(), Length(1, 24)])
    jenis_kelamin = SelectField(
        choices=[
            (g, g) for g in WaliMuridModel.jenis_kelamin.property.columns[0].type.enums
        ]
    )
    nomor_telepon = StringField(
        "Nomor telepon", validators=[DataRequired()], render_kw={"type": "number"},
    )
    murid = QuerySelectField(
        "Nama Anak",
        query_factory=daftar_murid,
        get_label="nama",
        get_pk=lambda a: a.id,
        blank_text="Murid",
        allow_blank=True,
        validators=[DataRequired()],
    )
    submit = SubmitField("Tambah")


class TambahUbahProfileForm(FlaskForm):
    nama_lembaga = StringField(
        "Nama Lembaga", validators=[DataRequired(), Length(1, 120)]
    )
    kode_pos = StringField("Kode Pos", validators=[DataRequired(), Length(1, 10)])
    kelurahan = StringField("Kelurahan", validators=[Length(1, 24)])
    kecamatan = StringField("Kecamatan", validators=[Length(1, 24)])
    kabupaten = StringField("Kabupaten", validators=[Length(1, 24)])
    provinsi = StringField("Provinsi", validators=[Length(1, 24)])
    no_statistik = StringField(
        "No. Statitistik", validators=[DataRequired(), Length(1, 60)]
    )
    akte_notaris = StringField(
        "Akte Notaris", validators=[DataRequired(), Length(0, 60)]
    )
    kegiatan_belajar = StringField(
        "Kegiatan Belajar", validators=[DataRequired(), Length(1, 20)]
    )
    tahun_berdiri = StringField(
        "Tahun Berdiri",
        validators=[DataRequired()],
        render_kw={"data-language": "en", "data-date-format": "dd MM yyyy"},
    )
    status_tk = StringField("Status TK", validators=[DataRequired(), Length(1, 10)])
    no_izin_operasional = StringField(
        "No. Izin Operasional", validators=[DataRequired(), Length(1, 46)]
    )
    no_izin_pendirian = StringField(
        "No. Izin Pendirian", validators=[DataRequired(), Length(1, 46)]
    )
    kurikulum = StringField("Kurikulum", validators=[DataRequired(), Length(1, 10)])
    no_telepon = StringField(
        "Nomor Telepon", validators=[DataRequired(), Length(0, 24)]
    )
    email = EmailField("Email", validators=[DataRequired(), Length(1, 24)])
    visi_misi = TextAreaField("Visi dan Misi", validators=[DataRequired()])
    submit = SubmitField("Tambahkan")


class TambahDataSekolahForm(FlaskForm):
    judul = StringField("Judul", validators=[DataRequired(), Length(1, 60)])
    deskripsi = TextAreaField("Deskripsi data sekolah")
    dokumen = FileField("Upload Dokumen", validators=[DataRequired()])
    submit = SubmitField("Tambahkan")

    def validate_judul(self, judul):
        judul = DataSekolahModel.query.filter_by(judul=self.judul.data).first()
        if judul is not None:
            raise ValueError("Judul data sekolah sudah ada.")


class UbahDataSekolahForm(FlaskForm):
    judul = StringField(
        "Judul data sekolah", validators=[DataRequired(), Length(1, 60)]
    )
    judul_hidden = StringField("judul_hidden", render_kw={"type": "hidden"})
    deskripsi = TextAreaField("Deskripsi data sekolah")
    dokumen = FileField("Upload Dokumen")
    submit = SubmitField("Tambahkan")

    def validate_judul(self, judul):
        judul = DataSekolahModel.query.filter_by(judul=self.judul_hidden.data).first()
        for data in DataSekolahModel.query.all():
            if data.judul == judul.judul:
                if data.judul != self.judul.data:
                    raise ValueError("Judul sudah terdaftar.")


class TambahUbahBeritaForm(FlaskForm):
    judul = StringField(
        "Judul berita sekolah", validators=[DataRequired(), Length(1, 120)]
    )
    deskripsi = TextAreaField("Deskripsi berita")
    tampilkan = BooleanField("Tampilkan berita")
    gambar = FileField("Background")
    kategori = StringField(
        "Kategori Berita", validators=[DataRequired(), Length(3, 24)]
    )
    submit = SubmitField("Tambahkan")


class TambahElearningForm(FlaskForm):
    dokumen = FileField("Upload Dokumen", validators=[DataRequired()])
    deskripsi = TextAreaField("Deskripsi")
    judul = StringField("Judul E-learning", validators=[DataRequired(), Length(1, 120)])
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


class UbahElearningForm(FlaskForm):
    dokumen = FileField("Upload Dokumen")
    deskripsi = TextAreaField("Deskripsi")
    judul = StringField("Judul E-learning", validators=[DataRequired(), Length(1, 120)])
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


class TambahUbahJadwalForm(FlaskForm):
    mata_pelajaran = StringField(
        "Mata Pelajaran", validators=[Length(2, 64), DataRequired()]
    )
    jam = StringField("Jam Pelajaran", validators=[DataRequired()])
    jam_end = StringField("Jam Pelajaran", validators=[DataRequired()])
    hari = SelectField(
        choices=[(g, g) for g in JadwalKelasModel.hari.property.columns[0].type.enums]
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
    submit = SubmitField("Simpan")


class TambahNilaiMuridForm(FlaskForm):
    deskripsi = TextAreaField("Deskripsi penilaian", validators=[DataRequired()])
    aspek_penilaian = SelectField(
        choices=[
            (g, g) for g in NilaiModel.aspek_penilaian.property.columns[0].type.enums
        ]
    )
    semester = SelectField(
        choices=[(g, g) for g in NilaiModel.semester.property.columns[0].type.enums]
    )
    tahun_pelajaran = StringField(
        "Tahun Pelajaran", validators=[DataRequired(), Length(0, 10)]
    )
    submit = SubmitField("Tambahkan")
