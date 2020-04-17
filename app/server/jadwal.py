from flask import render_template, flash, redirect, url_for, request, send_file
from io import BytesIO
import uuid
from app import db
from . import server
from app.models import JadwalKelasModel
from .forms import TambahUbahJadwalForm
from flask_login import login_required
from ..decorators import admin_guru_required


@server.route("/dashboard/jadwal-sekolah")
@admin_guru_required
@login_required
def data_jadwal():
    data_jadwal = (
        JadwalKelasModel.query.order_by(JadwalKelasModel.hari.asc())
        .order_by(JadwalKelasModel.jam.asc())
        .all()
    )
    return render_template(
        "jadwal/dataJadwal.html", title="Jadwal Kelas", data_jadwal=data_jadwal
    )


@server.route("/dashboard/jadwal-sekolah/tambah", methods=["GET", "POST"])
@admin_guru_required
@login_required
def tambah_jadwal():
    form = TambahUbahJadwalForm()
    if form.validate_on_submit():
        tambah_jadwal = JadwalKelasModel(
            mata_pelajaran=form.mata_pelajaran.data,
            jam=form.jam.data,
            jam_end=form.jam_end.data,
            hari=form.hari.data,
            kelas_id=form.kelas.data.id,
        )
        db.session.add(tambah_jadwal)
        db.session.commit()
        flash("Jadwal telah ditambahkan.", "Berhasil")
        return redirect(url_for("server.data_jadwal"))
    return render_template(
        "jadwal/tambahUbahJadwal.html", title="Tambah Jadwal", form=form
    )


@server.route("/dashboard/jadwal-sekolah/hapus/<id>")
@admin_guru_required
@login_required
def hapus_jadwal(id):
    hapus_jadwal = JadwalKelasModel.query.get(id)
    db.session.delete(hapus_jadwal)
    db.session.commit()
    flash("Jadwal sudah dihapus.", "Berhasil")
    return redirect(url_for("server.data_jadwal"))


@server.route("/dashboard/jadwal-sekolah/ubah/<id>", methods=["GET", "POST"])
@admin_guru_required
@login_required
def ubah_jadwal(id):
    form = TambahUbahJadwalForm()
    ubah_jadwal = JadwalKelasModel.query.get(id)
    if form.validate_on_submit():

        ubah_jadwal.mata_pelajaran = form.mata_pelajaran.data
        ubah_jadwal.jam = form.jam.data
        ubah_jadwal.jam_end = form.jam_end.data
        ubah_jadwal.hari = form.hari.data
        ubah_jadwal.kelas_id = form.kelas.data.id

        db.session.add(ubah_jadwal)
        db.session.commit()
        flash("Jadwal sudah diubah.", "Berhasil")
        return redirect(url_for("server.data_jadwal"))

    if request.method == "GET":
        form.mata_pelajaran.data = ubah_jadwal.mata_pelajaran
        form.jam.data = ubah_jadwal.jam
        form.jam_end.data = ubah_jadwal.jam_end
        form.hari.data = ubah_jadwal.hari
        form.kelas.data = ubah_jadwal.kelas_id

    return render_template(
        "jadwal/tambahUbahJadwal.html", title=ubah_jadwal.mata_pelajaran, form=form
    )
