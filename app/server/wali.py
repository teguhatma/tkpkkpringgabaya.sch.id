from . import server
from flask import request, redirect, url_for, send_file, flash, render_template
from uuid import uuid4
from app import db
from app.models import WaliMuridModel
from .forms import TambahUbahWaliForm
from flask_login import login_required
from ..decorators import admin_guru_required


@server.route("/dashboard/wali-murid")
@admin_guru_required
@login_required
def data_wali():
    data_wali_murid = WaliMuridModel.query.all()
    return render_template(
        "wali/dataWali.html", title="Daftar wali murid", data_wali_murid=data_wali_murid
    )


@server.route("/dashboard/wali-murid/hapus/<id>")
@admin_guru_required
@login_required
def hapus_wali(id):
    hapus_wali = WaliMuridModel.query.get(id)
    db.session.delete(hapus_wali)
    db.session.commit()
    flash("Data berhasil dihapus.", "Berhasil")
    return redirect(url_for("server.data_wali"))


@server.route("/dashboard/wali-murid/tambah", methods=["GET", "POST"])
@admin_guru_required
@login_required
def tambah_wali():
    form = TambahUbahWaliForm()
    if form.validate_on_submit():
        tambah_wali = WaliMuridModel(
            nama=form.nama.data,
            agama=form.agama.data,
            alamat=form.alamat.data,
            kelurahan=form.kelurahan.data,
            kecamatan=form.kecamatan.data,
            kabupaten=form.kabupaten.data,
            provinsi=form.provinsi.data,
            jenis_kelamin=form.jenis_kelamin.data,
            tempat_lahir=form.tempat_lahir.data,
            tanggal_lahir=form.tanggal_lahir.data,
            pekerjaan=form.pekerjaan.data,
            nomor_telepon=form.nomor_telepon.data,
            murid_id=form.murid.data.id,
        )
        db.session.add(tambah_wali)
        db.session.commit()
        flash("Data berhasil dibuat", "Berhasil")
        return redirect(url_for("server.data_wali"))
    return render_template(
        "wali/tambahUbahWali.html", title="Menambah data wali", form=form
    )


@server.route("/dashboard/wali-murid/ubah/<id>", methods=["GET", "POST"])
@admin_guru_required
@login_required
def ubah_wali(id):
    form = TambahUbahWaliForm()
    wali = WaliMuridModel.query.get(id)
    if form.validate_on_submit():
        wali.nama = form.nama.data
        wali.agama = form.agama.data
        wali.alamat = form.alamat.data
        wali.kelurahan = form.kelurahan.data
        wali.kecamatan = form.kecamatan.data
        wali.kabupaten = form.kabupaten.data
        wali.provinsi = form.provinsi.data
        wali.jenis_kelamin = form.jenis_kelamin.data
        wali.tempat_lahir = form.tempat_lahir.data
        wali.tanggal_lahir = form.tanggal_lahir.data
        wali.pekerjaan = form.pekerjaan.data
        wali.nomor_telepon = form.nomor_telepon.data
        wali.murid_id = form.murid.data.id

        db.session.add(wali)
        db.session.commit()
        flash("Data berhasil dirubah", "Berhasil")
        return redirect(url_for("server.data_wali"))

    if request.method == "GET":
        form.nama.data = wali.nama
        form.agama.data = wali.agama
        form.alamat.data = wali.alamat
        form.kelurahan.data = wali.kelurahan
        form.kabupaten.data = wali.kabupaten
        form.kecamatan.data = wali.kecamatan
        form.provinsi.data = wali.provinsi
        form.jenis_kelamin.data = wali.jenis_kelamin
        form.tempat_lahir.data = wali.tempat_lahir
        form.tanggal_lahir.data = wali.tanggal_lahir
        form.pekerjaan.data = wali.pekerjaan
        form.nomor_telepon.data = wali.nomor_telepon
        form.murid.data = wali.murid_id

    return render_template("wali/tambahUbahWali.html", title=wali.nama, form=form)


@server.route("/dashbaord/wali/lihat/<id>")
@admin_guru_required
@login_required
def lihat_wali(id):
    wali = WaliMuridModel.query.get(id)
    return render_template("wali/lihatWali.html", title=wali.nama, wali=wali)
