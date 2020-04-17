from . import server
from app import db
from flask import render_template, request, flash, url_for, redirect, send_file
from io import BytesIO
from app.models import MuridModel, Permission
from .forms import TambahMuridForm, RubahMuridForm, KelasModel
import uuid
from flask_login import login_required
from ..decorators import admin_guru_required


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
    return render_template(
        "murid/dataMurid.html", title="Data Murid", data_murid=data_murid
    )


@server.route("/dashboard/murid/hapus/<id>", methods=["GET", "POST"])
@admin_guru_required
@login_required
def hapus_murid(id):
    murid = MuridModel.query.get(id)
    db.session.delete(murid)
    db.session.commit()
    flash("Data {} berhasil dihapus.".format(murid.nama), "Berhasil")
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
            nama_foto_diri="{}".format(uuid.uuid4().hex),
            kelas_id=form.kelas.data.id,
        )
        db.session.add(tambah_murid)
        db.session.commit()
        flash("Data sudah ditambahkan", "Berhasil")
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
            murid.nama_foto_diri = "{}".format(uuid.uuid4().hex)
        elif form.foto_diri.data is None:
            murid.foto = murid.foto_diri
            murid.nama_foto = murid.nama_foto_diri

        db.session.add(murid)
        db.session.commit()
        flash("Data sudah dirubah", "Berhasil")
        return redirect(url_for("server.data_murid"))

    if request.method == "GET":
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
        form.kelas.data = murid.kelas
        form.nomor_induk_hidden.data = murid.nomor_induk

    return render_template("murid/ubahMurid.html", form=form, title=murid.nama)


@server.route("/dashboard/murid/lihat/<id>")
@admin_guru_required
@login_required
def lihat_murid(id):
    murid = MuridModel.query.get(id)
    return render_template("murid/lihatMurid.html", title=murid.nama, murid=murid)


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
