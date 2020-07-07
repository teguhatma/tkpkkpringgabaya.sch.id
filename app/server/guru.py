from flask import render_template, flash, redirect, url_for, request, send_file
from io import BytesIO
import uuid
from app import db
from . import server
from app.models import GuruModel, UserModel, Role
from .forms import (
    TambahGuruForm,
    RubahGuruForm,
    KelasModel,
    RubahProfileGuruForm,
    AddPassword,
    UbahPasswordDiriForm,
)
from flask_login import login_required, current_user
from ..decorators import admin_required, admin_guru_required


def unique_filename(data):
    """
    Create unique and secure filename

    @data is field name of current data now.
    """
    file = data
    get_ext = file.filename.split(".")[-1]
    new_name = "%s.%s" % (uuid.uuid4().hex, get_ext)
    return new_name


@server.route("/image/guru/foto/<filename>")
@admin_guru_required
@login_required
def foto_guru(filename):
    data = GuruModel.query.filter_by(nama_foto=filename).first()
    return send_file(
        BytesIO(data.foto),
        mimetype="images/generic",
        as_attachment=True,
        attachment_filename=data.nama_foto,
    )


@server.route("/image/guru/ijazah/<filename>")
@admin_guru_required
@login_required
def ijazah_guru(filename):
    data = GuruModel.query.filter_by(nama_foto_ijazah=filename).first()
    return send_file(
        BytesIO(data.foto_ijazah),
        mimetype="file/*",
        as_attachment=True,
        attachment_filename=data.nama_foto_ijazah,
    )


@server.route("/dashboard/guru")
@admin_guru_required
@login_required
def data_guru():
    data_guru = GuruModel.query.order_by(GuruModel.jabatan.asc()).all()
    return render_template("guru/dataGuru.html", title="Data Guru", data_guru=data_guru)


@server.route("/dashboard/guru/tambah", methods=["GET", "POST"])
@admin_required
@login_required
def tambah_guru():
    form = TambahGuruForm()
    if form.validate_on_submit():
        tambah_email = UserModel(email=form.email.data)
        tambah_guru = GuruModel(
            nama=form.nama.data,
            alamat=form.alamat.data,
            nik=form.nik.data,
            nip=form.nip.data,
            kelurahan=form.kelurahan.data,
            kecamatan=form.kecamatan.data,
            kabupaten=form.kabupaten.data,
            provinsi=form.provinsi.data,
            agama=form.agama.data,
            tempat_lahir=form.tempat_lahir.data,
            tanggal_lahir=form.tanggal_lahir.data,
            jabatan=form.jabatan.data,
            foto=form.foto.data.read(),
            nama_foto=unique_filename(form.foto.data),
            foto_ijazah=form.foto_ijazah.data.read(),
            nama_foto_ijazah=unique_filename(form.foto_ijazah.data),
            pendidikan_terakhir=form.pendidikan_terakhir.data,
            jenis_kelamin=form.jenis_kelamin.data,
            tahun_masuk=form.tahun_masuk.data,
            golongan=form.golongan.data,
            kelas_id=form.kelas.data.id,
        )
        db.session.add_all([tambah_email, tambah_guru])
        db.session.commit()
        tambah_guru.user_id = tambah_email.id
        tambah_email.role_id = Role.query.filter_by(name="Guru").first().id
        db.session.add_all([tambah_guru, tambah_email])
        db.session.commit()
        flash("Data sudah ditambahkan", "info")
        return redirect(url_for("server.data_guru"))
    return render_template(
        "guru/tambahGuru.html", title="Menambah Data Guru", form=form
    )


@server.route("/dashboard/guru/ubah/<id>", methods=["GET", "POST"])
@admin_required
@login_required
def ubah_guru(id):
    ubah = GuruModel.query.get(id)
    if current_user.guru.nama == ubah.nama:
        return redirect(url_for(".ubah_profile_guru"))
    else:
        form = RubahGuruForm()
        if form.validate_on_submit():
            ubah.nama = form.nama.data
            ubah.nip = form.nip.data
            ubah.alamat = form.alamat.data
            ubah.nik = form.nik.data
            ubah.user.email = form.email.data
            ubah.kelurahan = form.kelurahan.data
            ubah.kecamatan = form.kecamatan.data
            ubah.kabupaten = form.kabupaten.data
            ubah.provinsi = form.provinsi.data
            ubah.agama = form.agama.data
            ubah.tempat_lahir = form.tempat_lahir.data
            ubah.tanggal_lahir = form.tanggal_lahir.data
            ubah.jabatan = form.jabatan.data
            ubah.pendidikan_terakhir = form.pendidikan_terakhir.data
            ubah.jenis_kelamin = form.jenis_kelamin.data
            ubah.tahun_masuk = form.tahun_masuk.data
            ubah.golongan = form.golongan.data
            ubah.kelas_id = form.kelas.data.id
            if form.foto.data is not None and form.foto_ijazah.data is not None:
                ubah.foto = form.foto.data.read()
                ubah.nama_foto = unique_filename(form.foto.data)
                ubah.foto_ijazah = form.foto_ijazah.data.read()
                ubah.nama_foto_ijazah = unique_filename(form.foto_ijazah.data)
            elif form.foto.data is None and form.foto_ijazah.data is None:
                ubah.foto = ubah.foto
                ubah.nama_foto_ijazah = ubah.nama_foto_ijazah
                ubah.foto_ijazah = ubah.foto_ijazah
                ubah.nama_foto = ubah.nama_foto
            elif form.foto.data is not None and form.foto_ijazah is None:
                ubah.foto = form.foto.data.read()
                ubah.nama_foto_ijazah = ubah.nama_foto_ijazah
                ubah.foto_ijazah = ubah.foto_ijazah
                ubah.nama_foto = unique_filename(form.foto.data)
            elif form.foto.data is None and form.foto_ijazah is not None:
                ubah.foto_ijazah = form.foto_ijazah.data.read()
                ubah.nama_foto = ubah.nama_foto
                ubah.foto = ubah.foto
                ubah.nama_foto_ijazah = unique_filename(form.foto_ijazah.data)
            db.session.add(ubah)
            db.session.commit()
            flash("Data sudah dirubah", "info")
            return redirect(url_for("server.data_guru"))

        form.nama.data = ubah.nama
        form.alamat.data = ubah.alamat
        form.nik.data = ubah.nik
        form.nip.data = ubah.nip
        form.kelurahan.data = ubah.kelurahan
        form.kabupaten.data = ubah.kabupaten
        form.kecamatan.data = ubah.kecamatan
        form.provinsi.data = ubah.provinsi
        form.agama.data = ubah.agama
        form.tempat_lahir.data = ubah.tempat_lahir
        form.tanggal_lahir.data = ubah.tanggal_lahir
        form.jabatan.data = ubah.jabatan
        form.foto.data = ubah.nama_foto
        form.foto_ijazah.data = ubah.nama_foto_ijazah
        form.pendidikan_terakhir.data = ubah.pendidikan_terakhir
        form.jenis_kelamin.data = ubah.jenis_kelamin
        form.tahun_masuk.data = ubah.tahun_masuk
        form.golongan.data = ubah.golongan
        form.kelas.data = ubah.kelas
        form.email.data = ubah.user.email

    return render_template(
        "guru/ubahGuru.html", title="Mengubah Data Guru", form=form, data=ubah,
    )


@server.route("/dashboard/guru/ubah/<id>/kata-sandi", methods=["GET", "POST"])
@login_required
@admin_required
def ubah_password_guru(id):
    data = GuruModel.query.filter_by(id=id).first_or_404()
    pwd = UserModel.query.filter_by(id=data.user_id).first_or_404()
    form = AddPassword()
    if form.validate_on_submit():
        pwd.password(form.password.data)
        db.session.add(pwd)
        db.session.commit()
        flash("Data sudah dirubah", "info")
        return redirect(url_for("server.data_guru"))
    return render_template(
        "guru/ubahPasswordGuru.html", form=form, title="Password Guru"
    )


@server.route("/dashboard/ubah/kata-sandi", methods=["GET", "POST"])
@login_required
def ubah_password_diri():
    data = UserModel.query.filter_by(id=current_user.id).first_or_404()
    form = UbahPasswordDiriForm()
    if form.validate_on_submit():
        data.password(form.password.data)
        db.session.add(data)
        db.session.commit()
        flash("Password berhasil dirubah.", "info")
        return redirect(url_for(".ubah_profile_guru"))
    return render_template("guru/ubahPasswordDiri.html", title="Password", form=form)


@server.route("/dashboard/guru/profile-diri", methods=["GET", "POST"])
@admin_guru_required
@login_required
def ubah_profile_guru():
    form = RubahProfileGuruForm()
    ubah = GuruModel.query.get(current_user.guru.id)
    if form.validate_on_submit():
        ubah.nama = form.nama.data
        ubah.alamat = form.alamat.data
        ubah.nik = form.nik.data
        ubah.user.email = form.email.data
        ubah.kelurahan = form.kelurahan.data
        ubah.kecamatan = form.kecamatan.data
        ubah.kabupaten = form.kabupaten.data
        ubah.provinsi = form.provinsi.data
        ubah.nip = form.nip.data
        ubah.agama = form.agama.data
        ubah.tempat_lahir = form.tempat_lahir.data
        ubah.tanggal_lahir = form.tanggal_lahir.data
        ubah.pendidikan_terakhir = form.pendidikan_terakhir.data
        ubah.jenis_kelamin = form.jenis_kelamin.data
        ubah.tahun_masuk = form.tahun_masuk.data
        ubah.golongan = form.golongan.data
        if form.foto.data is not None and form.foto_ijazah.data is not None:
            ubah.foto = form.foto.data.read()
            ubah.nama_foto = unique_filename(form.foto.data)
            ubah.foto_ijazah = form.foto_ijazah.data.read()
            ubah.nama_foto_ijazah = unique_filename(form.foto_ijazah.data)
        elif form.foto.data is None and form.foto_ijazah.data is None:
            ubah.foto = ubah.foto
            ubah.nama_foto_ijazah = ubah.nama_foto_ijazah
            ubah.foto_ijazah = ubah.foto_ijazah
            ubah.nama_foto = ubah.nama_foto
        elif form.foto.data is not None and form.foto_ijazah is None:
            ubah.foto = form.foto.data.read()
            ubah.nama_foto = unique_filename(form.foto.data)
            ubah.foto_ijazah = ubah.foto_ijazah
            ubah.nama_foto_ijazah = ubah.nama_foto_ijazah
        elif form.foto.data is None and form.foto_ijazah is not None:
            ubah.foto_ijazah = form.foto_ijazah.data.read()
            ubah.nama_foto_ijazah = unique_filename(form.foto_ijazah.data)
            ubah.nama_foto = ubah.nama_foto
            ubah.foto = ubah.foto
        db.session.add(ubah)
        db.session.commit()
        flash("Data sudah dirubah", "info")
        return redirect(url_for("server.dashboard"))

    if request.method == "GET":
        form.nama.data = ubah.nama
        form.alamat.data = ubah.alamat
        form.nip.data = ubah.nip
        form.nik.data = ubah.nik
        form.kelurahan.data = ubah.kelurahan
        form.kabupaten.data = ubah.kabupaten
        form.kecamatan.data = ubah.kecamatan
        form.provinsi.data = ubah.provinsi
        form.agama.data = ubah.agama
        form.tempat_lahir.data = ubah.tempat_lahir
        form.tanggal_lahir.data = ubah.tanggal_lahir
        form.foto.data = ubah.nama_foto
        form.foto_ijazah.data = ubah.nama_foto_ijazah
        form.pendidikan_terakhir.data = ubah.pendidikan_terakhir
        form.jenis_kelamin.data = ubah.jenis_kelamin
        form.tahun_masuk.data = ubah.tahun_masuk
        form.golongan.data = ubah.golongan
        form.email.data = ubah.user.email

    return render_template(
        "guru/ubahProfileGuru.html", title="Profil Diri", form=form, data=ubah
    )


@server.route("/dashboard/guru/hapus/<id>", methods=["POST", "GET"])
@login_required
@admin_required
def hapus_guru(id):
    hapus_guru = GuruModel.query.get(id)
    hapus_user = UserModel.query.get(hapus_guru.user_id)
    db.session.delete(hapus_guru)
    db.session.delete(hapus_user)
    db.session.commit()
    flash("Data {} sudah berhasil dihapus".format(hapus_guru.nama), "info")
    return redirect(url_for("server.data_guru"))
