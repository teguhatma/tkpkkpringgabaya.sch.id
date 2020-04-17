from flask import render_template, flash, redirect, url_for, request, send_file
from io import BytesIO
import uuid
from app import db
from . import server
from app.models import GuruModel
from .forms import TambahGuruForm, RubahGuruForm, KelasModel
from flask_login import login_required, current_user
from ..decorators import admin_required, admin_guru_required


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
        mimetype="images/generic",
        as_attachment=True,
        attachment_filename=data.nama_foto_ijazah,
    )


@server.route("/dashboard/guru")
@admin_guru_required
@login_required
def data_guru():
    data_guru = GuruModel.query.order_by(GuruModel.jabatan.asc()).all()
    return render_template("guru/dataGuru.html", title="Data guru", data_guru=data_guru)


@server.route("/dashboard/guru/tambah", methods=["GET", "POST"])
@admin_required
@login_required
def tambah_guru():
    form = TambahGuruForm()
    if form.validate_on_submit():
        tambah_guru = GuruModel(
            nama=form.nama.data,
            alamat=form.alamat.data,
            nik=form.nik.data,
            email=form.email.data,
            kelurahan=form.kelurahan.data,
            kecamatan=form.kecamatan.data,
            kabupaten=form.kabupaten.data,
            provinsi=form.provinsi.data,
            agama=form.agama.data,
            tempat_lahir=form.tempat_lahir.data,
            tanggal_lahir=form.tanggal_lahir.data,
            jabatan=form.jabatan.data,
            foto=form.foto.data.read(),
            nama_foto="{}".format(uuid.uuid4().hex),
            foto_ijazah=form.foto_ijazah.data.read(),
            nama_foto_ijazah="{}".format(uuid.uuid4().hex),
            pendidikan_terakhir=form.pendidikan_terakhir.data,
            jenis_kelamin=form.jenis_kelamin.data,
            tahun_masuk=form.tahun_masuk.data,
            golongan=form.golongan.data,
            kelas_id=form.kelas.data.id,
        )
        db.session.add(tambah_guru)
        db.session.commit()
        flash("Data sudah ditambahkan", "Berhasil")
        return redirect(url_for("server.data_guru"))
    return render_template(
        "guru/tambahGuru.html", title="Menambah data guru", form=form
    )


@server.route("/dashboard/guru/ubah/<id>", methods=["GET", "POST"])
@admin_required
@login_required
def ubah_guru(id):
    form = RubahGuruForm()
    ubah = GuruModel.query.get(id)
    if form.validate_on_submit():
        ubah.nama = form.nama.data
        ubah.alamat = form.alamat.data
        ubah.nik = form.nik.data
        ubah.email = form.email.data
        ubah.kelurahan = form.kelurahan.data
        ubah.kecamatan = form.kecamatan.data
        ubah.kabupaten = form.kabupaten.data
        ubah.provinsi = form.provinsi.data
        ubah.agama = form.agama.data
        ubah.tempat_lahir = form.tempat_lahir.data
        ubah.tanggal_lahir = form.tanggal_lahir.data
        ubah.jabatan = form.jabatan.data
        ubah.pendidikan_terakhir = form.pendidikan_terakhir.data
        ubahjenis_kelamin = form.jenis_kelamin.data
        ubahtahun_masuk = form.tahun_masuk.data
        ubah.golongan = form.golongan.data
        ubah.kelas_id = form.kelas.data.id
        if form.foto.data is not None and form.foto_ijazah.data is not None:
            ubah.foto = form.foto.data.read()
            ubah.nama_foto = "{}".format(uuid.uuid4().hex)
            ubah.foto_ijazah = form.foto_ijazah.data.read()
            ubah.nama_foto_ijazah = "{}".format(uuid.uuid4().hex)
        elif form.foto.data is None and form.foto_ijazah.data is None:
            ubah.foto = ubah.foto
            ubah.nama_foto_ijazah = ubah.nama_foto_ijazah
            ubah.foto_ijazah = ubah.foto_ijazah
            ubah.nama_foto = ubah.nama_foto
        elif form.foto.data is not None and form.foto_ijazah is None:
            ubah.foto = form.foto.data.read()
            ubah.nama_foto_ijazah = "{}".format(uuid.uuid4().hex)
            ubah.foto_ijazah = ubah.foto_ijazah
            ubah.nama_foto = ubah.nama_foto
        elif form.foto.data is None and form.foto_ijazah is not None:
            ubah.foto_ijazah = form.foto_ijazah.data.read()
            ubah.nama_foto = "{}".format(uuid.uuid4().hex)
            ubah.foto = ubah.foto
            ubah.nama_foto_ijazah = ubah.nama_foto_ijazah
        db.session.add(ubah)
        db.session.commit()
        flash("Data sudah dirubah", "Berhasil")
        return redirect(url_for("server.data_guru"))

    if request.method == "GET":
        form.nama.data = ubah.nama
        form.alamat.data = ubah.alamat
        form.nik.data = ubah.nik
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
        form.kelas.data = ubah.kelas_id
        form.email.data = ubah.email
        form.nik_hidden.data = ubah.nik
        form.email_hidden.data = ubah.email
        form.jabatan_hidden.data = ubah.jabatan

    return render_template("guru/ubahGuru.html", title=ubah.nama, form=form)


@server.route("/dashboard/guru/edit-your-profile", methods=["GET", "POST"])
@admin_guru_required
@login_required
def ubah_profile_guru():
    form = RubahGuruForm()
    ubah = GuruModel.query.get(current_user.id)
    if form.validate_on_submit():
        ubah.nama = form.nama.data
        ubah.alamat = form.alamat.data
        ubah.nik = form.nik.data
        ubah.email = form.email.data
        ubah.kelurahan = form.kelurahan.data
        ubah.kecamatan = form.kecamatan.data
        ubah.kabupaten = form.kabupaten.data
        ubah.provinsi = form.provinsi.data
        ubah.agama = form.agama.data
        ubah.tempat_lahir = form.tempat_lahir.data
        ubah.tanggal_lahir = form.tanggal_lahir.data
        ubah.jabatan = form.jabatan.data
        ubah.pendidikan_terakhir = form.pendidikan_terakhir.data
        ubahjenis_kelamin = form.jenis_kelamin.data
        ubahtahun_masuk = form.tahun_masuk.data
        ubah.golongan = form.golongan.data
        ubah.kelas_id = form.kelas.data.id
        if form.foto.data is not None and form.foto_ijazah.data is not None:
            ubah.foto = form.foto.data.read()
            ubah.nama_foto = "{}".format(uuid.uuid4().hex)
            ubah.foto_ijazah = form.foto_ijazah.data.read()
            ubah.nama_foto_ijazah = "{}".format(uuid.uuid4().hex)
        elif form.foto.data is None and form.foto_ijazah.data is None:
            ubah.foto = ubah.foto
            ubah.nama_foto_ijazah = ubah.nama_foto_ijazah
            ubah.foto_ijazah = ubah.foto_ijazah
            ubah.nama_foto = ubah.nama_foto
        elif form.foto.data is not None and form.foto_ijazah is None:
            ubah.foto = form.foto.data.read()
            ubah.nama_foto_ijazah = "{}".format(uuid.uuid4().hex)
            ubah.foto_ijazah = ubah.foto_ijazah
            ubah.nama_foto = ubah.nama_foto
        elif form.foto.data is None and form.foto_ijazah is not None:
            ubah.foto_ijazah = form.foto_ijazah.data.read()
            ubah.nama_foto = "{}".format(uuid.uuid4().hex)
            ubah.foto = ubah.foto
            ubah.nama_foto_ijazah = ubah.nama_foto_ijazah
        db.session.add(ubah)
        db.session.commit()
        flash("Data sudah dirubah", "Berhasil")
        return redirect(url_for("server.lihat_profile_guru"))

    if request.method == "GET":
        form.nama.data = ubah.nama
        form.alamat.data = ubah.alamat
        form.nik.data = ubah.nik
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
        form.kelas.data = ubah.kelas_id
        form.email.data = ubah.email
        form.nik_hidden.data = ubah.nik
        form.email_hidden.data = ubah.email
        form.jabatan_hidden.data = ubah.jabatan

    return render_template("guru/ubahGuru.html", title=ubah.nama, form=form)


@server.route("/dashboard/guru/lihat/<id>")
@admin_required
@login_required
def lihat_guru(id):
    guru = GuruModel.query.filter_by(id=id).first_or_404()
    return render_template(
        "guru/lihatGuru.html", title="{}".format(guru.nama), guru=guru
    )


@server.route("/dashboard/guru/your-profile")
@admin_guru_required
@login_required
def lihat_profile_guru():
    guru = GuruModel.query.get(current_user.id)
    return render_template(
        "guru/lihatGuru.html", title="{}".format(guru.nama), guru=guru
    )


@server.route("/dashboard/guru/hapus/<id>", methods=["POST", "GET"])
@login_required
@admin_required
def hapus_guru(id):
    hapus_guru = GuruModel.query.get(id)
    db.session.delete(hapus_guru)
    db.session.commit()
    flash("Data {} sudah berhasil dihapus".format(hapus_guru.nama), "Berhasil")
    return redirect(url_for("server.data_guru"))
