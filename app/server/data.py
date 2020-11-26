from flask import render_template, flash, redirect, url_for, request, send_file
from io import BytesIO
import uuid
from app import db
from . import server
from app.models import DataSekolahModel, KelasModel
from .forms import TambahDataSekolahForm, UbahDataSekolahForm
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


@server.route("/data-sekolah/<filename>")
@admin_guru_required
@login_required
def dokumen_data_sekolah(filename):
    kelas = KelasModel.query.order_by(KelasModel.ruang.asc()).all()
    dokumen = DataSekolahModel.query.filter_by(nama_dokumen=filename).first()
    return send_file(
        BytesIO(dokumen.dokumen),
        mimetype="file/*",
        as_attachment=True,
        attachment_filename=dokumen.nama_dokumen,
        kelas=kelas,
    )


@server.route("/dashboard/data-sekolah")
@admin_guru_required
@login_required
def data_sekolah():
    kelas = KelasModel.query.order_by(KelasModel.ruang.asc()).all()
    data_sekolah = DataSekolahModel.query.all()
    return render_template(
        "dataSekolah/dataSekolah.html",
        data_sekolah=data_sekolah,
        title="Data Sekolah",
        kelas=kelas,
    )


@server.route("/dashboard/data-sekolah/tambah", methods=["POST", "GET"])
@admin_guru_required
@login_required
def tambah_data_sekolah():
    kelas = KelasModel.query.order_by(KelasModel.ruang.asc()).all()
    form = TambahDataSekolahForm()
    if form.validate_on_submit():
        tambah_data_sekolah = DataSekolahModel(
            judul=form.judul.data,
            deskripsi=form.deskripsi.data,
            dokumen=form.dokumen.data.read(),
            nama_dokumen=unique_filename(form.dokumen.data),
        )
        db.session.add(tambah_data_sekolah)
        db.session.commit()
        flash("Data sekolah sudah tersimpan", "info")
        return redirect(url_for("server.data_sekolah"))
    return render_template(
        "dataSekolah/tambahDataSekolah.html",
        form=form,
        title="Tambah data sekolah",
        kelas=kelas,
    )


@server.route("/dashboard/data-sekolah/hapus/<slug>", methods=["GET", "POST"])
@admin_guru_required
@login_required
def hapus_data_sekolah(slug):
    hapus_data_sekolah = DataSekolahModel.query.filter_by(slug=slug).first_or_404()
    db.session.delete(hapus_data_sekolah)
    db.session.commit()
    flash("Data sekolah berhasil terhapus", "info")
    return redirect(url_for("server.data_sekolah"))


@server.route("/dashboard/data-sekolah/ubah/<slug>", methods=["GET", "POST"])
@admin_guru_required
@login_required
def ubah_data_sekolah(slug):
    kelas = KelasModel.query.order_by(KelasModel.ruang.asc()).all()
    ubah_data_sekolah = DataSekolahModel.query.filter_by(slug=slug).first_or_404()
    form = UbahDataSekolahForm()
    if form.validate_on_submit():
        ubah_data_sekolah.judul = form.judul.data
        ubah_data_sekolah.deskripsi = form.deskripsi.data
        if form.dokumen.data is not None:
            ubah_data_sekolah.dokumen = form.dokumen.data.read()
            ubah_data_sekolah.nama_dokumen = unique_filename(form.dokumen.data)
        else:
            ubah_data_sekolah.dokumen = ubah_data_sekolah.dokumen
            ubah_data_sekolah.nama_dokumen = ubah_data_sekolah.nama_dokumen

        db.session.add(ubah_data_sekolah)
        db.session.commit()
        flash("Data sekolah sudah diubah", "info")
        return redirect(url_for("server.data_sekolah"))

    if request.method == "GET":
        form.judul.data = ubah_data_sekolah.judul
        form.deskripsi.data = ubah_data_sekolah.deskripsi

    return render_template(
        "dataSekolah/tambahDataSekolah.html",
        title=ubah_data_sekolah.judul,
        form=form,
        kelas=kelas,
    )
