from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import event
from slugify import slugify
from datetime import datetime


__fotosize__ = 4028
__filesize__ = 8056


class AdminModel(db.Model):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)

    @property
    def password(self):
        raise AttributeError("Password is not readable attribute")

    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "Admin {}".format(self.username)


class GuruModel(db.Model):
    __tablename__ = "guru"

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(64), nullable=False)
    alamat = db.Column(db.Text, nullable=False)
    nik = db.Column(db.String(24), unique=True, nullable=False)
    kelurahan = db.Column(db.String(24))
    kecamatan = db.Column(db.String(24))
    kabupaten = db.Column(db.String(24))
    provinsi = db.Column(db.String(24))
    agama = db.Column(
        db.Enum(
            "Islam", "Kristen", "Katolik", "Hindu", "Buddha", "Kong Hu Cu", name="agama"
        )
    )
    tempat_lahir = db.Column(db.String(24), nullable=False)
    tanggal_lahir = db.Column(db.String(24), nullable=False)
    jabatan = db.Column(db.Enum("Kepala Sekolah", "Guru", "Pegawai", name="jabatan"))
    foto = db.Column(db.LargeBinary(__fotosize__))
    nama_foto = db.Column(db.String(64), unique=True)
    foto_ijazah = db.Column(db.LargeBinary(__fotosize__))
    nama_foto_ijazah = db.Column(db.String(64), unique=True)
    golongan = db.Column(
        db.Enum(
            "None",
            "I/a",
            "I/b",
            "I/c",
            "I/d",
            "II/a",
            "II/b",
            "II/c",
            "II/d",
            "III/a",
            "III/b",
            "III/c",
            "III/d",
            "IV/a",
            "IV/b",
            "IV/c",
            "IV/d",
            "IV/e",
            name="golongan",
        )
    )
    pendidikan_terakhir = db.Column(db.String(24), nullable=False)
    jenis_kelamin = db.Column(db.Enum("Laki-laki", "Perempuan", name="gender"))
    tahun_masuk = db.Column(db.String(24), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    kelas_id = db.Column(db.Integer, db.ForeignKey("kelas.id"))
    kelas = db.relationship("KelasModel", back_populates="guru")

    @property
    def password(self):
        raise AttributeError("Password is not readable attribute")

    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "Guru {}".format(self.nama)


class PegawaiModel(db.Model):
    __tablename__ = "pegawai"

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(64), nullable=False)
    alamat = db.Column(db.Text, nullable=False)
    kelurahan = db.Column(db.String(24))
    kecamatan = db.Column(db.String(24))
    kabupaten = db.Column(db.String(24))
    provinsi = db.Column(db.String(24))
    agama = db.Column(
        db.Enum(
            "Islam", "Kristen", "Katolik", "Hindu", "Buddha", "Kong Hu Cu", name="agama"
        )
    )
    tempat_lahir = db.Column(db.String(24), nullable=False)
    tanggal_lahir = db.Column(db.String(24), nullable=False)
    jabatan = db.Column(db.Enum("Kepala Sekolah", "Guru", "Pegawai", name="jabatan"))
    foto = db.Column(db.LargeBinary(__fotosize__))
    nama_foto = db.Column(db.String(64), unique=True)
    pendidikan_terakhir = db.Column(db.String(24), nullable=False)
    jenis_kelamin = db.Column(db.Enum("Laki-laki", "Perempuan", name="gender"))
    tahun_masuk = db.Column(db.String(24), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)

    @property
    def password(self):
        raise AttributeError("Password is not readable attribute")

    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "Pegawai {}".format(self.nama)


class MuridModel(db.Model):
    __tablename__ = "murid"

    id = db.Column(db.Integer, primary_key=True)
    nomor_induk = db.Column(db.String(5), nullable=False)
    nama = db.Column(db.String(64), nullable=False)
    nama_panggilan = db.Column(db.String(24), nullable=False)
    anak_ke = db.Column(db.String(2), nullable=False)
    alamat = db.Column(db.Text, nullable=False)
    kelurahan = db.Column(db.String(24))
    kecamatan = db.Column(db.String(24))
    kabupaten = db.Column(db.String(24))
    provinsi = db.Column(db.String(24))
    agama = db.Column(
        db.Enum(
            "Islam", "Kristen", "Katolik", "Hindu", "Buddha", "Kong Hu Cu", name="agama"
        )
    )
    tempat_lahir = db.Column(db.String(24), nullable=False)
    tanggal_lahir = db.Column(db.String(24), nullable=False)
    lulus = db.Column(db.Boolean, default=False)
    nama_ibu_kandung = db.Column(db.String(64), nullable=False)
    jenis_kelamin = db.Column(db.Enum("Laki-laki", "Perempuan", name="gender"))
    tahun_pelajaran = db.Column(db.String(24))
    foto_diri = db.Column(db.LargeBinary(__fotosize__))
    nama_foto_diri = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(120))
    kelas_id = db.Column(db.Integer, db.ForeignKey("kelas.id"))
    kelas = db.relationship("KelasModel", back_populates="murid")
    nilai = db.relationship("NilaiModel", back_populates="murid")
    wali_murid_id = db.Column(db.Integer, db.ForeignKey("wali_murid.id"))
    wali_murid = db.relationship("WaliMuridModel", back_populates="murid")

    @property
    def password(self):
        raise AttributeError("Password is not readable attribute")

    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "Murid {}".format(self.nama)


class WaliMuridModel(db.Model):
    __tablename__ = "wali_murid"

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(120), nullable=False)
    agama = db.Column(
        db.Enum(
            "Islam", "Kristen", "Katolik", "Hindu", "Buddha", "Kong Hu Cu", name="agama"
        )
    )
    alamat = db.Column(db.String(120), nullable=False)
    kelurahan = db.Column(db.String(60))
    kecamatan = db.Column(db.String(60))
    kabupaten = db.Column(db.String(60))
    provinsi = db.Column(db.String(60))
    jenis_kelamin = db.Column(
        db.Enum("Laki-laki", "Perempuan", name="gender"), nullable=False
    )
    tempat_lahir = db.Column(db.String(60), nullable=False)
    tanggal_lahir = db.Column(db.String(60), nullable=False)
    pekerjaan = db.Column(db.String(40), nullable=False)
    nomor_telepon = db.Column(db.String(12), nullable=False)
    murid = db.relationship("MuridModel", back_populates="wali_murid")

    def __repr__(self):
        return "Wali Murid {}".format(self.nama)


class ProfileSekolahModel(db.Model):
    __tablename__ = "profil_sekolah"

    id = db.Column(db.Integer, primary_key=True)
    nama_lembaga = db.Column(db.String(120), nullable=False)
    kode_pos = db.Column(db.String(10), nullable=False)
    kelurahan = db.Column(db.String(60), nullable=False)
    kecamatan = db.Column(db.String(60), nullable=False)
    kabupaten = db.Column(db.String(60), nullable=False)
    provinsi = db.Column(db.String(60), nullable=False)
    no_statistik = db.Column(db.String(60), nullable=False)
    akte_notaris = db.Column(db.String(60), nullable=False)
    kegiatan_belajar = db.Column(db.String(20), nullable=False)
    tahun_berdiri = db.Column(db.String(10), nullable=False)
    status_tk = db.Column(db.String(10), nullable=False)
    no_izin_pendirian = db.Column(db.String(46), nullable=False)
    no_izin_operasional = db.Column(db.String(46), nullable=False)
    kurikulum = db.Column(db.String(10), nullable=False)
    no_telepon = db.Column(db.String(13), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    visi_misi = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "Profile Sekolah {}".format(self.nama_lembaga)


class DataSekolahModel(db.Model):
    __tablename__ = "data_sekolah"

    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(60), unique=True, nullable=False)
    deskripsi = db.Column(db.Text)
    filename = db.Column(db.String(120), unique=True)
    file = db.Column(db.LargeBinary(__filesize__))
    slug = db.Column(db.String(120), unique=True)
    waktu_upload = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def generate_slug(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)

    def __repr__(self):
        return "Data Sekolah {}".format(self.judul)


class BeritaModel(db.Model):
    __tablename__ = "berita"

    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(120), nullable=False)
    deskripsi = db.Column(db.Text)
    slug = db.Column(db.String(120))
    kategori = db.Column(db.String(24), nullable=False)
    gambar = db.Column(db.LargeBinary(__fotosize__))
    nama_gambar = db.Column(db.String(124))
    waktu_upload = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    tampilkan = db.Column(db.Boolean, default=False)

    @staticmethod
    def generate_slug(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)

    def __repr__(self):
        return "Berita {}".format(self.judul)


class ElearningModel(db.Model):
    __tablename__ = "elearning"

    id = db.Column(db.Integer, primary_key=True)
    dokumen = db.Column(db.LargeBinary(__filesize__))
    nama_dokumen = db.Column(db.String(120), unique=True)
    waktu_upload = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    deskripsi = db.Column(db.Text)
    slug = db.Column(db.String(120), unique=True)
    judul = db.Column(db.String(120), nullable=False)
    kelas_id = db.Column(db.Integer, db.ForeignKey("kelas.id"))
    kelas = db.relationship("KelasModel", back_populates="elearning")

    @staticmethod
    def generate_slug(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)

    def __repr__(self):
        return "ELearning {}".format(self.judul)


class NilaiModel(db.Model):
    __tablename__ = "nilai"

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(120), unique=True, nullable=False)
    deskripsi = db.Column(db.Text, nullable=False)
    jenis_penilaian = db.Column(
        db.Enum(
            "Nilai Agama dan Moral",
            "Fisik",
            "Kognitif",
            "Bahasa",
            "Sosial, Emosi",
            "Seni",
            name="kategori",
        ),
        nullable=False,
    )
    semester = db.Column(
        db.Enum("Semester I", "Semester II", name="semester"), nullable=False
    )
    tahun_pelajaran = db.Column(db.String(24))
    murid_id = db.Column(db.Integer, db.ForeignKey("murid.id"))
    murid = db.relationship("MuridModel", back_populates="nilai")

    def __repr__(self):
        return "Nilai {}".format(self.nama)


class JadwalKelasModel(db.Model):
    __tablename__ = "jadwal_kelas"

    id = db.Column(db.Integer, primary_key=True)
    mata_pelajaran = db.Column(db.String(64), nullable=False)
    jam = db.Column(db.String(10), nullable=False)
    hari = db.Column(
        db.Enum("Senin", "Selasa", "Rabu", "Kamis", "Jum'at", "Sabtu", name="hari")
    )
    kelas_id = db.Column(db.Integer, db.ForeignKey("kelas.id"))
    kelas = db.relationship("KelasModel", back_populates="jadwal_kelas")

    def __repr__(self):
        return "Jadwal Kelas {}".format(self.mata_pelajaran)


class KelasModel(db.Model):
    __tablename__ = "kelas"

    id = db.Column(db.Integer, primary_key=True)
    ruang = db.Column(db.String(5), nullable=False, unique=True)
    murid = db.relationship("MuridModel", back_populates="kelas")
    jadwal = db.relationship("JadwalKelasModel", back_populates="kelas")
    elearning = db.relationship("ElearningModel", back_populates="kelas")
    guru = db.relationship("GuruModel", back_populates="kelas")

    def __repr__(self):
        return "Kelas {}".format(self.ruang)


event.listen(
    DataSekolahModel.judul, "set", DataSekolahModel.generate_slug, retval=False
)
event.listen(BeritaModel.judul, "set", BeritaModel.generate_slug, retval=False)
event.listen(ElearningModel.judul, "set", ElearningModel.generate_slug, retval=False)

