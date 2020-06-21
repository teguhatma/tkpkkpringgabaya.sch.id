from flask import render_template, flash, redirect, url_for, request, send_file
from io import BytesIO
import uuid
from app import db
from . import server
from app.models import ElearningModel
from .forms import (
    TambahElearningForm,
    UbahElearningForm,
    TambahElearningGuruForm,
    UbahElearningGuruForm,
)
from flask_login import login_required
from ..decorators import admin_guru_required
from flask_login import current_user
from werkzeug.utils import secure_filename


def unique_filename(data):
    """
    Create unique and secure filename

    @data is field name of current data now.
    """
    file = data
    get_ext = file.filename.split(".")[-1]
    new_name = "%s.%s" % (uuid.uuid4().hex, get_ext)
    return new_name


@server.route("/file/e-learning/<filename>")
@admin_guru_required
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
@admin_guru_required
@login_required
def data_elearning():
    if current_user.is_administrator():
        data_elearning = ElearningModel.query.all()
    else:
        data_elearning = ElearningModel.query.filter_by(
            kelas_id=current_user.guru.kelas_id
        ).all()
    return render_template(
        "elearning/dataLearning.html",
        title="E-Learning",
        data_elearning=data_elearning,
    )


@server.route("/dashboard/e-learning/tambah", methods=["GET", "POST"])
@admin_guru_required
@login_required
def tambah_elearning():
    if current_user.is_administrator():
        form = TambahElearningForm()
        if form.validate_on_submit():
            tambah_elearning = ElearningModel(
                judul=form.judul.data,
                deskripsi=form.deskripsi.data,
                dokumen=form.dokumen.data.read(),
                nama_dokumen=unique_filename(form.dokumen.data),
                kelas_id=form.kelas.data.id,
            )
            db.session.add(tambah_elearning)
            db.session.commit()
            flash("Elearning sudah dibuat", "Berhasil")
            return redirect(url_for("server.data_elearning"))
    else:
        form = TambahElearningGuruForm()
        if form.validate_on_submit():
            tambah_elearning = ElearningModel(
                judul=form.judul.data,
                deskripsi=form.deskripsi.data,
                dokumen=form.dokumen.data.read(),
                nama_dokumen=unique_filename(form.dokumen.data),
                kelas_id=current_user.guru.kelas_id,
            )
            db.session.add(tambah_elearning)
            db.session.commit()
            flash("Elearning sudah dibuat", "Berhasil")
            return redirect(url_for("server.data_elearning"))
    return render_template(
        "elearning/tambahUbahLearning.html", title="Tambah Elearning", form=form
    )


@server.route("/dashboard/e-learning/hapus/<slug>")
@admin_guru_required
@login_required
def hapus_elearning(slug):
    hapus_elearning = ElearningModel.query.filter_by(slug=slug).first_or_404()
    db.session.delete(hapus_elearning)
    db.session.commit()
    flash("E-Learning berhasil dihapus.", "Berhasil")
    return redirect(url_for("server.data_elearning"))


@server.route("/dashboard/e-learning/ubah/<slug>", methods=["GET", "POST"])
@admin_guru_required
@login_required
def ubah_elearning(slug):
    ubah_elearning = ElearningModel.query.filter_by(slug=slug).first_or_404()
    if current_user.is_administrator():
        form = UbahElearningForm()
        if form.validate_on_submit():
            ubah_elearning.judul = form.judul.data
            ubah_elearning.deskripsi = form.deskripsi.data
            ubah_elearning.kelas_id = form.kelas.data.id
            if form.dokumen.data is not None:
                ubah_elearning.dokumen = form.dokumen.data.read()
                ubah_elearning.nama_dokumen = unique_filename(form.dokumen.data)
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
            form.kelas.data = ubah_elearning.kelas
    else:
        form = UbahElearningGuruForm()
        if form.validate_on_submit():
            ubah_elearning.judul = form.judul.data
            ubah_elearning.deskripsi = form.deskripsi.data
            ubah_elearning.kelas_id = current_user.guru.kelas_id
            if form.dokumen.data is not None:
                ubah_elearning.dokumen = form.dokumen.data.read()
                ubah_elearning.nama_dokumen = unique_filename(form.dokumen.data)
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
            form.kelas.data = ubah_elearning.kelas
    return render_template(
        "elearning/tambahUbahLearning.html", title=ubah_elearning.judul, form=form
    )
