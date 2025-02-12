from flask import render_template, flash, redirect, url_for, request, send_file
from io import BytesIO
import uuid
from app import db
from . import server
from app.models import BeritaModel, KelasModel
from .forms import TambahUbahBeritaForm
from flask_login import login_required
from ..decorators import admin_guru_required
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


@server.route("/dashboard/berita-sekolah")
@admin_guru_required
@login_required
def berita_sekolah():
    kelas = KelasModel.query.order_by(KelasModel.ruang.asc()).all()
    berita_sekolah = BeritaModel.query.all()
    return render_template(
        "berita/dataBerita.html",
        title="Berita Sekolah",
        berita_sekolah=berita_sekolah,
        kelas=kelas,
    )


@server.route("/dashboard/berita-sekolah/tambah", methods=["GET", "POST"])
@admin_guru_required
@login_required
def tambah_berita_sekolah():
    kelas = KelasModel.query.order_by(KelasModel.ruang.asc()).all()
    form = TambahUbahBeritaForm()

    # Mendapatkan file gambar
    import random, os

    directory = "app/static/img/berita"
    join = os.path.join(os.getcwd(), directory)
    files = os.listdir(join)
    index = random.randrange(0, len(files))
    filename = directory + "/" + files[index]

    if form.validate_on_submit():
        if form.gambar.data is None and form.dokumen.data is None:

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
            )

            db.session.add(berita)
            db.session.commit()
            flash("Data berhasil terbuat", "Berhasil")
            return redirect(url_for("server.berita_sekolah"))

        elif form.gambar.data is None and form.dokumen.data is not None:
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
                dokumen=form.dokumen.data.read(),
                nama_dokumen=unique_filename(form.dokumen.data),
            )

            db.session.add(berita)
            db.session.commit()
            flash("Data berhasil terbuat", "Berhasil")
            return redirect(url_for("server.berita_sekolah"))

        elif form.gambar.data is not None and form.dokumen.data is None:
            berita = BeritaModel(
                judul=form.judul.data,
                deskripsi=form.deskripsi.data,
                gambar=form.gambar.data.read(),
                nama_gambar=unique_filename(form.gambar.data),
                tampilkan=form.tampilkan.data,
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
                nama_gambar=unique_filename(form.gambar.data),
                tampilkan=form.tampilkan.data,
                dokumen=form.dokumen.data.read(),
                nama_dokumen=unique_filename(form.dokumen.data),
            )
            db.session.add(berita)
            db.session.commit()
            flash("Data berhasil terbuat", "Berhasil")
            return redirect(url_for("server.berita_sekolah"))
    return render_template(
        "berita/tambahBerita.html",
        title="Tambah berita sekolah",
        form=form,
        data=[],
        kelas=kelas,
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
    kelas = KelasModel.query.order_by(KelasModel.ruang.asc()).all()
    ubah = BeritaModel.query.filter_by(slug=slug).first_or_404()
    form = TambahUbahBeritaForm()
    if form.validate_on_submit():
        ubah.judul = form.judul.data
        ubah.deskripsi = form.deskripsi.data
        ubah.tampilkan = form.tampilkan.data
        if form.gambar.data is None and form.dokumen.data is None:
            ubah.gambar = ubah.gambar
            ubah.nama_gambar = ubah.nama_gambar
            ubah.dokumen = ubah.dokumen
            ubah.nama_dokumen = ubah.nama_dokumen
        elif form.gambar.data is None and form.dokumen.data is not None:
            ubah.gambar = ubah.gambar
            ubah.nama_gambar = ubah.nama_gambar
            ubah.dokumen = form.dokumen.data.read()
            ubah.nama_dokumen = unique_filename(form.dokumen.data)
        elif form.gambar.data is not None and form.dokumen.data is None:
            ubah.gambar = form.gambar.data.read()
            ubah.nama_gambar = unique_filename(form.gambar.data)
            ubah.dokumen = ubah.dokumen
            ubah.nama_dokumen = ubah.nama_dokumen
        else:
            ubah.gambar = form.gambar.data.read()
            ubah.nama_gambar = unique_filename(form.gambar.data)
            ubah.dokumen = form.dokumen.data.read()
            ubah.nama_dokumen = unique_filename(form.dokumen.data)
        db.session.add(ubah)
        db.session.commit()
        flash("Berita sekolah telah diubah", "Berhasil")
        return redirect(url_for("server.berita_sekolah"))

    if request.method == "GET":
        form.judul.data = ubah.judul
        form.deskripsi.data = ubah.deskripsi
        form.tampilkan.data = ubah.tampilkan

    return render_template(
        "berita/ubahBerita.html",
        title="Mengubah Berita",
        form=form,
        data=ubah,
        kelas=kelas,
    )
