from flask import render_template, flash, redirect, url_for, request, send_file
from io import BytesIO
import uuid
from app import db
from . import server
from app.models import DataSekolahModel
from .forms import TambahDataSekolahForm, UbahDataSekolahForm
from flask_login import login_required
from ..decorators import admin_guru_required


@server.route("/data-sekolah/<filename>")
@admin_guru_required
@login_required
def dokumen_data_sekolah(filename):
    dokumen = DataSekolahModel.query.filter_by(nama_dokumen=filename).first()
    return send_file(
        BytesIO(dokumen.dokumen),
        mimetype="file/*",
        as_attachment=True,
        attachment_filename=dokumen.nama_dokumen,
    )


@server.route("/dashboard/data-sekolah")
@admin_guru_required
@login_required
def data_sekolah():
    data_sekolah = DataSekolahModel.query.all()
    return render_template(
        "dataSekolah/dataSekolah.html", data_sekolah=data_sekolah, title="Data Sekolah"
    )


@server.route("/dashboard/data-sekolah/tambah", methods=["POST", "GET"])
@admin_guru_required
@login_required
def tambah_data_sekolah():
    form = TambahDataSekolahForm()
    if form.validate_on_submit():
        tambah_data_sekolah = DataSekolahModel(
            judul=form.judul.data,
            deskripsi=form.deskripsi.data,
            dokumen=form.dokumen.data.read(),
            nama_dokumen=uuid.uuid4().hex,
        )
        db.session.add(tambah_data_sekolah)
        db.session.commit()
        flash("Data sekolah sudah tersimpan", "Berhasil")
        return redirect(url_for("server.data_sekolah"))
    return render_template(
        "dataSekolah/tambahDataSekolah.html", form=form, title="Tambah data sekolah"
    )


@server.route("/dashboard/data-sekolah/hapus/<slug>", methods=["GET", "POST"])
@admin_guru_required
@login_required
def hapus_data_sekolah(slug):
    hapus_data_sekolah = DataSekolahModel.query.filter_by(slug=slug).first_or_404()
    db.session.delete(hapus_data_sekolah)
    db.session.commit()
    flash("Data sekolah berhasil terhapus", "Berhasil")
    return redirect(url_for("server.data_sekolah"))


@server.route("/dashboard/data-sekolah/ubah/<slug>", methods=["GET", "POST"])
@admin_guru_required
@login_required
def ubah_data_sekolah(slug):
    ubah_data_sekolah = DataSekolahModel.query.filter_by(slug=slug).first_or_404()
    form = UbahDataSekolahForm()
    if form.validate_on_submit():
        ubah_data_sekolah.judul = form.judul.data
        ubah_data_sekolah.deskripsi = form.deskripsi.data
        if form.dokumen.data is not None:
            ubah_data_sekolah.dokumen = form.dokumen.data.read()
            ubah_data_sekolah.nama_dokumen = uuid.uuid4().hex
        else:
            ubah_data_sekolah.dokumen = ubah_data_sekolah.dokumen
            ubah_data_sekolah.nama_dokumen = ubah_data_sekolah.nama_dokumen

        db.session.add(ubah_data_sekolah)
        db.session.commit()
        flash("Data sekolah sudah diubah", "Berhasil")
        return redirect(url_for("server.data_sekolah"))

    if request.method == "GET":
        form.judul.data = ubah_data_sekolah.judul
        form.deskripsi.data = ubah_data_sekolah.deskripsi
        form.judul_hidden.data = ubah_data_sekolah.judul

    return render_template(
        "dataSekolah/ubahDataSekolah.html", title=ubah_data_sekolah.judul, form=form
    )
