from flask import render_template, flash, redirect, url_for, request, send_file
from io import BytesIO
import uuid
from app import db
from . import server
from app.models import ElearningModel
from .forms import TambahElearningForm, UbahElearningForm
from flask_login import login_required


@server.route("/file/e-learning/<filename>")
@login_required
def dokumen_elearning(filename):
    data = ElearningModel.query.filter_by(nama_dokumen=filename).first()
    return send_file(
        BytesIO(data.dokumen),
        mimetype="file/*",
        as_attachment=True,
        attachment_filename=data.nama_dokumen,
    )


@server.route("/dashboard/e-learning")
@login_required
def data_elearning():
    data_elearning = ElearningModel.query.all()
    return render_template(
        "elearning/dataLearning.html",
        title="E-Learning",
        data_elearning=data_elearning,
    )


@server.route("/dashboard/e-learning/tambah", methods=["GET", "POST"])
@login_required
def tambah_elearning():
    form = TambahElearningForm()
    if form.validate_on_submit():
        tambah_elearning = ElearningModel(
            judul=form.judul.data,
            deskripsi=form.deskripsi.data,
            dokumen=form.dokumen.data.read(),
            nama_dokumen=uuid.uuid4().hex,
            kelas_id=form.kelas.data.id,
        )
        db.session.add(tambah_elearning)
        db.session.commit()
        flash("Elearning sudah dibuat", "Berhasil")
        return redirect(url_for("server.data_elearning"))
    return render_template(
        "elearning/tambahUbahLearning.html", title="Tambah Elearning", form=form
    )


@server.route("/dashboard/e-learning/hapus/<slug>")
@login_required
def hapus_elearning(slug):
    hapus_elearning = ElearningModel.query.filter_by(slug=slug).first_or_404()
    db.session.delete(hapus_elearning)
    db.session.commit()
    flash("E-Learning berhasil dihapus.", "Berhasil")
    return redirect(url_for("server.data_elearning"))


@server.route("/dashboard/e-learning/ubah/<slug>", methods=["GET", "POST"])
@login_required
def ubah_elearning(slug):
    ubah_elearning = ElearningModel.query.filter_by(slug=slug).first_or_404()
    form = UbahElearningForm()
    if form.validate_on_submit():
        ubah_elearning.judul = form.judul.data
        ubah_elearning.deskripsi = form.deskripsi.data
        ubah_elearning.kelas_id = form.kelas.data.id
        if form.dokumen.data is not None:
            ubah_elearning.dokumen = form.dokumen.data.read()
            ubah_elearning.nama_dokumen = uuid.uuid4().hex
        else:
            ubah_elearning.dokumen = ubah_elearning.dokumen
            ubah_elearning.nama_dokumen = ubah_elearning.nama_dokumen

        db.session.add(ubah_elearning)
        db.session.commit()
        flash("E-Learning telah diubah.", "Berhasil")
        return redirect(url_for("server.data_elearning"))

    if request.method == "GET":
        form.judul.data = ubah_elearning.judul
        form.deskripsi.data = ubah_elearning.deskripsi
        form.kelas.data = ubah_elearning.kelas_id

    return render_template(
        "elearning/tambahUbahLearning.html", title=ubah_elearning.judul, form=form
    )
