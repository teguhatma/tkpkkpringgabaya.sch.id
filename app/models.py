from app import db
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import event
from slugify import slugify
from datetime import datetime
from app import login_manager
from flask_login import UserMixin, current_user, AnonymousUserMixin


__fotosize__ = 4028
__filesize__ = 8056


class Permission:
    ADMIN = 2
    MURID = 4
    ADMIN_GURU = 8
    GURU = 16


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    user = db.relationship("UserModel", backref="role", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            "Admin": [Permission.ADMIN, Permission.ADMIN_GURU],
            "Guru": [
                Permission.ADMIN_GURU,
                Permission.GURU,
            ],
            "Murid": [Permission.MURID],
        }

        default_role = "Murid"
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = role.name == default_role
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm


class UserModel(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(120))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    guru = db.relationship("GuruModel", uselist=False, back_populates="user")
    murid = db.relationship("MuridModel", uselist=False, back_populates="user")

    def __init__(self, **kwargs):
        super(UserModel, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config["ADMIN_TK"]:
                self.role = Role.query.filter_by(name="Admin").frist()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    @property
    def password(self):
        raise AttributeError("Password is not readable attribute")

    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def insert_admin():
        insert_admin = UserModel(
            email="baiqiriantini@gmail.com",
            role=Role.query.filter_by(name="Admin").first(),
        )
        insert_admin.password("tkadminadmin")
        db.session.add(insert_admin)
        db.session.commit()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return int(self.id)

    def __repr__(self):
        return "Email {}".format(self.email)


class GuruModel(db.Model):
    __tablename__ = "guru"

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(64), nullable=False)
    alamat = db.Column(db.Text(), nullable=False)
    nik = db.Column(db.String(24), unique=True, nullable=False)
    nip = db.Column(db.String(24))
    kelurahan = db.Column(db.String(24), nullable=False)
    kecamatan = db.Column(db.String(24), nullable=False)
    kabupaten = db.Column(db.String(24), nullable=False)
    provinsi = db.Column(db.String(24), nullable=False)
    agama = db.Column(
        db.Enum(
            "Islam", "Kristen", "Katolik", "Hindu", "Buddha", "Kong Hu Cu", name="agama"
        ),
        nullable=False,
    )
    tempat_lahir = db.Column(db.String(24), nullable=False)
    tanggal_lahir = db.Column(db.String(24), nullable=False)
    jabatan = db.Column(
        db.Enum("Kepala Sekolah", "Guru", name="jabatan"), nullable=False
    )
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
        ),
        nullable=False,
    )
    pendidikan_terakhir = db.Column(db.String(24), nullable=False)
    jenis_kelamin = db.Column(
        db.Enum("Laki-laki", "Perempuan", name="gender"), nullable=False
    )
    tahun_masuk = db.Column(db.String(24), nullable=False)
    kelas_id = db.Column(db.Integer, db.ForeignKey("kelas.id"))
    kelas = db.relationship("KelasModel", back_populates="guru")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("UserModel", back_populates="guru")

    @staticmethod
    def insert_guru():
        insert_admin = GuruModel(
            nama="Baiq Iriantini, S.Pd.",
            user=UserModel.query.first(),
            nik="196512311985023321",
            jabatan="Kepala Sekolah",
            alamat="Dasan Bantek",
            nip="1912341234514",
            kelurahan="Pringgabaya",
            kecamatan="Pringgabaya",
            kabupaten="Lombok Timur",
            provinsi="Nusa Tenggara Barat",
            agama="Islam",
            tempat_lahir="Pringgabaya",
            tanggal_lahir="15 September 1965",
            golongan="IV/e",
            pendidikan_terakhir="S1 PGPAUD",
            jenis_kelamin="Perempuan",
            tahun_masuk="2010",
        )
        db.session.add(insert_admin)
        db.session.commit()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def __repr__(self):
        return "Guru {}".format(self.nama)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return int(self.id)


class MuridModel(db.Model):
    __tablename__ = "murid"

    id = db.Column(db.Integer, primary_key=True)
    nomor_induk = db.Column(db.String(5), nullable=False, unique=True)
    nama = db.Column(db.String(64), nullable=False)
    nama_panggilan = db.Column(db.String(24), nullable=False)
    anak_ke = db.Column(db.String(2), nullable=False)
    alamat = db.Column(db.Text, nullable=False)
    dusun = db.Column(db.String(24), nullable=False)
    kelurahan = db.Column(db.String(24), nullable=False)
    kecamatan = db.Column(db.String(24), nullable=False)
    kabupaten = db.Column(db.String(24), nullable=False)
    provinsi = db.Column(db.String(24), nullable=False)
    agama = db.Column(
        db.Enum(
            "Islam", "Kristen", "Katolik", "Hindu", "Buddha", "Kong Hu Cu", name="agama"
        ),
        nullable=False,
    )
    tempat_lahir = db.Column(db.String(24), nullable=False)
    tanggal_lahir = db.Column(db.String(24), nullable=False)
    lulus = db.Column(db.Boolean, default=False)
    nama_ibu_kandung = db.Column(db.String(64), nullable=False)
    jenis_kelamin = db.Column(
        db.Enum("Laki-laki", "Perempuan", name="gender"), nullable=False
    )
    tahun_pelajaran = db.Column(db.String(24), nullable=False)
    foto_diri = db.Column(db.LargeBinary(__fotosize__))
    nama_foto_diri = db.Column(db.String(64), unique=True)
    kelas_id = db.Column(db.Integer, db.ForeignKey("kelas.id"))
    kelas = db.relationship("KelasModel", back_populates="murid")
    wali_murid = db.relationship("WaliMuridModel", back_populates="murid")
    nilai = db.relationship("NilaiModel")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("UserModel", back_populates="murid")

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def __repr__(self):
        return "Murid {}".format(self.nama)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return int(self.id)


class WaliMuridModel(db.Model):
    __tablename__ = "wali_murid"

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(120), nullable=False)
    agama = db.Column(
        db.Enum(
            "Islam", "Kristen", "Katolik", "Hindu", "Buddha", "Kong Hu Cu", name="agama"
        ),
        nullable=False,
    )
    alamat = db.Column(db.Text, nullable=False)
    kelurahan = db.Column(db.String(60), nullable=False)
    kecamatan = db.Column(db.String(60), nullable=False)
    kabupaten = db.Column(db.String(60), nullable=False)
    provinsi = db.Column(db.String(60), nullable=False)
    jenis_kelamin = db.Column(
        db.Enum("Laki-laki", "Perempuan", name="gender"), nullable=False
    )
    tempat_lahir = db.Column(db.String(60), nullable=False)
    tanggal_lahir = db.Column(db.String(60), nullable=False)
    pekerjaan = db.Column(db.String(40), nullable=False)
    nomor_telepon = db.Column(db.String(12), nullable=False)
    murid_id = db.Column(db.Integer, db.ForeignKey("murid.id"))
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
    alamat = db.Column(db.Text(), nullable=False)
    no_telepon = db.Column(db.String(13), nullable=False)
    website = db.Column(db.String(64), nullable=False)
    sosmed = db.Column(db.JSON, nullable=True)
    email = db.Column(db.String(64), nullable=False)
    visi_misi = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "Profile Sekolah {}".format(self.nama_lembaga)


class DataSekolahModel(db.Model):
    __tablename__ = "dokumen_sekolah"

    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(60), unique=True, nullable=False)
    deskripsi = db.Column(db.Text)
    nama_dokumen = db.Column(db.String(120), unique=True)
    dokumen = db.Column(db.LargeBinary(__filesize__))
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
    dokumen = db.Column(db.LargeBinary(__filesize__))
    nama_dokumen = db.Column(db.String(124), unique=True)
    gambar = db.Column(db.LargeBinary(__fotosize__))
    nama_gambar = db.Column(db.String(124), unique=True)
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
    __tablename__ = "nilai_model"

    id = db.Column(db.Integer, primary_key=True)
    deskripsi = db.Column(db.Text, nullable=False)
    aspek_penilaian = db.Column(
        db.Enum(
            "Perkembangan Nilai Agama dan Moral",
            "Perkembangan Sosial, Emosional",
            "Perkembangan Bahasa",
            "Perkembangan Kognitif",
            "Perkembangan Fisik Motorik",
            "Perkembangan Seni",
            name="aspek_penilaian",
        ),
        nullable=False,
    )
    semester = db.Column(
        db.Enum("Semester I", "Semester II", name="semester"), nullable=False
    )
    tahun_pelajaran = db.Column(db.String(24), nullable=False)
    murid_id = db.Column(db.Integer, db.ForeignKey("murid.id"))

    def __repr__(self):
        return "Nilai {}".format(self.aspek_penilaian)


class JadwalKelasModel(db.Model):
    __tablename__ = "jadwal_kelas"

    id = db.Column(db.Integer, primary_key=True)
    mata_pelajaran = db.Column(db.String(64), nullable=False)
    jam = db.Column(db.String(10), nullable=False)
    jam_end = db.Column(db.String(10), nullable=False)
    hari = db.Column(
        db.Enum("Senin", "Selasa", "Rabu", "Kamis", "Jum'at", "Sabtu", name="hari"),
        nullable=False,
    )
    kelas_id = db.Column(db.Integer, db.ForeignKey("kelas.id"))
    kelas = db.relationship("KelasModel", back_populates="jadwal")

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

    @staticmethod
    def insert_kelas():
        insert_kelas_a = KelasModel(ruang="A1")
        insert_kelas_b = KelasModel(ruang="A2")
        db.session.add_all([insert_kelas_a, insert_kelas_b])
        db.session.commit()

    def __repr__(self):
        return "Kelas {}".format(self.ruang)


class PrestasiModel(db.Model):
    __tablename__ = "prestasi"

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(64), nullable=True)
    kategori = db.Column(db.String(24), nullable=False)
    tahun = db.Column(db.String(24), nullable=False)
    juara = db.Column(db.String(24), nullable=False)
    tingkat = db.Column(db.String(48), nullable=False)

    def __repr__(self):
        return "Prestasi {}".format(self.nama)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


event.listen(
    DataSekolahModel.judul, "set", DataSekolahModel.generate_slug, retval=False
)
event.listen(BeritaModel.judul, "set", BeritaModel.generate_slug, retval=False)
event.listen(ElearningModel.judul, "set", ElearningModel.generate_slug, retval=False)


def daftar_kelas():
    return KelasModel.query


def daftar_murid():
    return MuridModel.query.order_by(MuridModel.nama.asc())


@login_manager.user_loader
def load_user(id):
    return UserModel.query.get(id)
