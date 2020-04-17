from flask import render_template, flash, redirect, url_for, request, send_file
from io import BytesIO
import uuid
from app import db
from . import server
from app.models import BeritaModel
from .forms import TambahUbahBeritaForm
from flask_login import login_required
from ..decorators import admin_guru_required


@server.route("/dashboard/berita-sekolah")
@admin_guru_required
@login_required
def berita_sekolah():
    berita_sekolah = BeritaModel.query.all()
    return render_template(
        "berita/dataBerita.html", title="Berita Sekolah", berita_sekolah=berita_sekolah
    )


@server.route("/dashboard/berita-sekolah/tambah", methods=["GET", "POST"])
@admin_guru_required
@login_required
def tambah_berita_sekolah():
    form = TambahUbahBeritaForm()

    # Mendapatkan file gambar
    import random, os

    directory = "app/static/img/berita"
    join = os.path.join(os.getcwd(), directory)
    files = os.listdir(join)
    index = random.randrange(0, len(files))
    filename = directory + "/" + files[index]

    if form.validate_on_submit():
        if form.gambar.data is None:

            # Covert img to BLOB
            def converToBinaryData(filename):
                with open(filename, "rb") as file:
                    blobData = file.read()
                return blobData

            berita = BeritaModel(
                judul=form.judul.data,
                deskripsi=form.deskripsi.data,
                gambar=converToBinaryData(filename),
                nama_gambar="{}".format(uuid.uuid4().hex),
                tampilkan=form.tampilkan.data,
                kategori=form.kategori.data,
            )
            db.session.add(berita)
            db.session.commit()
            flash("Data berhasil terbuat", "Berhasil")
            return redirect(url_for("server.berita_sekolah"))
        else:
            berita = BeritaModel(
                judul=form.judul.data,
                deskripsi=form.deskripsi.data,
                gambar=form.gambar.data.read(),
                nama_gambar="{}".format(uuid.uuid4().hex),
                tampilkan=form.tampilkan.data,
                kategori=form.kategori.data,
            )
            db.session.add(berita)
            db.session.commit()
            flash("Data berhasil terbuat", "Berhasil")
            return redirect(url_for("server.berita_sekolah"))
    return render_template(
        "berita/tambahUbahBerita.html", title="Tambah berita sekolah", form=form
    )


@server.route("/dashboard/berita-sekolah/hapus/<slug>", methods=["GET", "POST"])
@admin_guru_required
@login_required
def hapus_berita_sekolah(slug):
    hapus_berita_sekolah = BeritaModel.query.filter_by(slug=slug).first_or_404()
    db.session.delete(hapus_berita_sekolah)
    db.session.commit()
    flash("Berita sekolah telah dihapus.", "Berhasil")
    return redirect(url_for("server.berita_sekolah"))


@server.route("/dashboard/berita-sekolah/ubah/<slug>", methods=["GET", "POST"])
@admin_guru_required
@login_required
def ubah_berita_sekolah(slug):
    ubah = BeritaModel.query.filter_by(slug=slug).first_or_404()
    form = TambahUbahBeritaForm()
    if form.validate_on_submit():
        ubah.judul = form.judul.data
        ubah.deskripsi = form.deskripsi.data
        ubah.tampilkan = form.tampilkan.data
        ubah.kategori = form.kategori.data
        if form.gambar.data is None:
            ubah.gambar = ubah.gambar
            ubah.nama_gambar = ubah.nama_gambar
        else:
            ubah.gambar = form.gambar.data.read()
            ubah.nama_gambar = uuid.uuid4().hex
        db.session.add(ubah)
        db.session.commit()
        flash("Berita sekolah telah diubah", "Berhasil")
        return redirect(url_for("server.berita_sekolah"))

    if request.method == "GET":
        form.judul.data = ubah.judul
        form.deskripsi.data = ubah.deskripsi
        form.kategori.data = ubah.kategori
        form.tampilkan.data = ubah.tampilkan

    return render_template("berita/tambahUbahBerita.html", title=ubah.judul, form=form)
