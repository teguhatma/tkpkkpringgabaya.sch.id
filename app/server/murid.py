from . import server
from app import db
from flask import render_template, request, flash, url_for, redirect, send_file
from io import BytesIO
from app.models import MuridModel, Permission
from .forms import TambahMuridForm, RubahMuridForm, KelasModel, UserModel, AddPassword
import uuid
from flask_login import login_required
from ..decorators import admin_guru_required


def unique_filename(data):
    """
    Create unique and secure filename

    @data is field name of current data now.
    """
    file = data
    get_ext = file.filename.split(".")[-1]
    new_name = "%s.%s" % (uuid.uuid4().hex, get_ext)
    return new_name


@server.route("/image/murid/foto/<filename>")
@admin_guru_required
@login_required
def foto_murid(filename):
    data = MuridModel.query.filter_by(nama_foto_diri=filename).first()
    return send_file(
        BytesIO(data.foto_diri),
        mimetype="images/generic",
        as_attachment=True,
        attachment_filename=data.nama_foto_diri,
    )


@server.route("/dashboard/murid")
@admin_guru_required
@login_required
def data_murid():
    data_murid = MuridModel.query.all()
    kelas = KelasModel.query.order_by(KelasModel.ruang.asc()).all()
    return render_template(
        "murid/dataMurid.html", title="Data Murid", data_murid=data_murid, kelas=kelas
    )


@server.route("/dashboard/murid/<ruang>")
@admin_guru_required
@login_required
def data_murid_kelas(ruang):
    data_murid = MuridModel.query.filter_by(kelas_id=ruang).all()
    kelas = KelasModel.query.order_by(KelasModel.ruang.asc()).all()
    return render_template(
        "murid/dataMurid.html", title="Data Murid", data_murid=data_murid, kelas=kelas
    )


@server.route("/dashboard/murid/hapus/<id>", methods=["GET", "POST"])
@admin_guru_required
@login_required
def hapus_murid(id):
    murid = MuridModel.query.get(id)
    user = UserModel.query.get(murid.user_id)
    db.session.delete(murid)
    db.session.delete(user)
    db.session.commit()
    flash("Data {} berhasil dihapus.".format(murid.nama), "info")
    return redirect(url_for("server.data_murid"))


@server.route("/dashboard/murid/tambah", methods=["GET", "POST"])
@admin_guru_required
@login_required
def tambah_murid():
    form = TambahMuridForm()
    if form.validate_on_submit():
        tambah_murid = MuridModel(
            nomor_induk=form.nomor_induk.data,
            nama_panggilan=form.nama_panggilan.data,
            anak_ke=form.anak_ke.data,
            nama=form.nama.data,
            alamat=form.alamat.data,
            dusun=form.dusun.data,
            kelurahan=form.kelurahan.data,
            kecamatan=form.kecamatan.data,
            kabupaten=form.kabupaten.data,
            provinsi=form.provinsi.data,
            agama=form.agama.data,
            tempat_lahir=form.tempat_lahir.data,
            tanggal_lahir=form.tanggal_lahir.data,
            lulus=form.lulus.data,
            nama_ibu_kandung=form.nama_ibu_kandung.data,
            jenis_kelamin=form.jenis_kelamin.data,
            tahun_pelajaran=form.tahun_pelajaran.data,
            foto_diri=form.foto_diri.data.read(),
            nama_foto_diri=unique_filename(form.foto_diri.data),
            kelas_id=form.kelas.data.id,
        )
        tambah_email = UserModel(email=form.email.data)
        db.session.add_all([tambah_murid, tambah_email])
        db.session.commit()
        tambah_murid.user_id = tambah_email.id
        db.session.add(tambah_murid)
        db.session.commit()
        flash("Data berhasil ditambahkan", "info")
        return redirect(url_for("server.data_murid"))
    return render_template(
        "murid/tambahMurid.html", form=form, title="Menambah data murid"
    )


@server.route("/dashboard/murid/ubah/<id>", methods=["GET", "POST"])
@admin_guru_required
@login_required
def ubah_murid(id):
    form = RubahMuridForm()
    murid = MuridModel.query.get(id)
    if form.validate_on_submit():
        murid.nomor_induk = form.nomor_induk.data
        murid.nama_panggilan = form.nama_panggilan.data
        murid.anak_ke = form.anak_ke.data
        murid.user.email = form.email.data
        murid.nama = form.nama.data
        murid.alamat = form.alamat.data
        murid.dusun = form.dusun.data
        murid.kelurahan = form.kelurahan.data
        murid.kecamatan = form.kecamatan.data
        murid.kabupaten = form.kabupaten.data
        murid.provinsi = form.provinsi.data
        murid.agama = form.agama.data
        murid.tempat_lahir = form.tempat_lahir.data
        murid.tanggal_lahir = form.tanggal_lahir.data
        murid.lulus = form.lulus.data
        murid.nama_ibu_kandung = form.nama_ibu_kandung.data
        murid.jenis_kelamin = form.jenis_kelamin.data
        murid.tahun_pelajaran = form.tahun_pelajaran.data
        murid.kelas_id = form.kelas.data.id
        if form.foto_diri.data is not None:
            murid.foto_diri = form.foto_diri.data.read()
            murid.nama_foto_diri = unique_filename(form.foto_diri.data)
        elif form.foto_diri.data is None:
            murid.foto = murid.foto_diri
            murid.nama_foto = murid.nama_foto_diri

        db.session.add(murid)
        db.session.commit()
        flash("Data berhasil dirubah", "info")
        return redirect(url_for("server.data_murid"))

    form.nomor_induk.data = murid.nomor_induk
    form.nama_panggilan.data = murid.nama_panggilan
    form.anak_ke.data = murid.anak_ke
    form.nama.data = murid.nama
    form.alamat.data = murid.alamat
    form.dusun.data = murid.dusun
    form.kelurahan.data = murid.kelurahan
    form.kecamatan.data = murid.kecamatan
    form.kabupaten.data = murid.kabupaten
    form.provinsi.data = murid.provinsi
    form.agama.data = murid.agama
    form.tempat_lahir.data = murid.tempat_lahir
    form.tanggal_lahir.data = murid.tanggal_lahir
    form.lulus.data = murid.lulus
    form.nama_ibu_kandung.data = murid.nama_ibu_kandung
    form.jenis_kelamin.data = murid.jenis_kelamin
    form.tahun_pelajaran.data = murid.tahun_pelajaran
    form.foto_diri.data = murid.foto_diri
    form.email.data = murid.user.email
    form.kelas.data = murid.kelas

    return render_template(
        "murid/ubahMurid.html", form=form, title="Merubah Data Murid", data=murid
    )


@server.route("/dashboard/murid/ubah/<id>/kata-sandi", methods=["GET", "POST"])
@login_required
@admin_guru_required
def ubah_password_murid(id):
    data = MuridModel.query.filter_by(id=id).first_or_404()
    pwd = UserModel.query.filter_by(id=data.user_id).first_or_404()
    form = AddPassword()
    if form.validate_on_submit():
        pwd.password(form.password.data)
        db.session.add(pwd)
        db.session.commit()
        flash("Data sudah dirubah", "info")
        return redirect(url_for("server.data_guru"))
    return render_template(
        "guru/ubahPasswordGuru.html", form=form, title="Password Murid"
    )


@server.route("/dashboard/kelas/murid/<id>")
@admin_guru_required
@login_required
def kelas_murid(id):
    kelas = KelasModel.query.get(id)
    data_murid = MuridModel.query.filter_by(kelas_id=id).all()
    return render_template(
        "murid/dataMurid.html",
        data_murid=data_murid,
        title="Daftar murid di kelas {}".format(kelas.ruang),
    )
