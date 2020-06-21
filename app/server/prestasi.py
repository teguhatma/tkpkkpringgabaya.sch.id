from flask import render_template, flash, redirect, url_for, request, send_file
from io import BytesIO
import uuid
from app import db
from . import server
from app.models import PrestasiModel
from .forms import TambahUbahPrestasiForm
from flask_login import login_required
from ..decorators import admin_required, admin_guru_required


@server.route("/dashboard/prestasi")
@login_required
@admin_guru_required
def prestasi():
    prestasi = PrestasiModel.query.all()
    return render_template(
        "prestasi/dataPrestasi.html", prestasi=prestasi, title="Data Prestasi"
    )


@server.route("/dashboard/prestasi/tambah", methods=["GET", "POST"])
@login_required
@admin_guru_required
def tambah_prestasi():
    form = TambahUbahPrestasiForm()
    if form.validate_on_submit():
        tambah = PrestasiModel(
            nama=form.nama.data,
            kategori=form.kategori.data,
            tahun=form.tahun.data,
            tingkat=form.tingkat.data,
            juara=form.juara.data,
        )
        db.session.add(tambah)
        db.session.commit()
        flash("Data berhasil ditambahkan.", "info")
        return redirect(url_for(".prestasi"))
    return render_template(
        "prestasi/tambahUbahPrestasi.html", title="Tambah Prestasi", form=form
    )


@server.route("/dashboard/prestasi/ubah/<id>", methods=["GET", "POST"])
@login_required
@admin_guru_required
def ubah_prestasi(id):
    form = TambahUbahPrestasiForm()
    ubah = PrestasiModel.query.get(id)
    if form.validate_on_submit():
        ubah.nama = form.nama.data
        ubah.kategori = form.kategori.data
        ubah.tahun = form.tahun.data
        ubah.tingkat = form.tingkat.data
        ubah.juara = form.juara.data
        db.session.add(ubah)
        db.session.commit()
        flash("Data berhasil ditambahkan.", "info")
        return redirect(url_for(".prestasi"))

    if request.method == "GET":
        form.nama.data = ubah.nama
        form.kategori.data = ubah.kategori
        form.tahun.data = ubah.tahun
        form.tingkat.data = ubah.tingkat
        form.juara.data = ubah.juara

    return render_template(
        "prestasi/tambahUbahPrestasi.html", title="Tambah Prestasi", form=form
    )


@server.route("/dashboard/prestasi/hapus/<id>", methods=["GET", "POST"])
@login_required
@admin_guru_required
def hapus_prestasi(id):
    hapus = PrestasiModel.query.get(id)
    db.session.delete(hapus)
    db.session.commit()
    flash("Data berhasil dihapus.", "info")
    return redirect(url_for(".prestasi"))
