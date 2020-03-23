from . import server
from app import db
from flask import render_template, request, flash, url_for, redirect, send_file
from io import BytesIO
from app.models import MuridModel, NilaiModel
from .forms import TambahNilaiMuridForm
import uuid


@server.route("/dashboard/nilai/murid")
def nilai_murid():
    nilai_murid = MuridModel.query.all()
    return render_template(
        "nilai/dataNilaiMurid.html", title="Data nilai murid", nilai_murid=nilai_murid
    )


@server.route("/dashboard/nilai/murid/<id>")
def data_nilai_murid(id):
    murid = MuridModel.query.get(id)
    nilai = NilaiModel.query.filter_by(murid_id=murid.id).all()
    return render_template(
        "nilai/lihatNilaiMurid.html",
        title="Nilai {}".format(murid.nama),
        murid=murid,
        nilai=nilai,
    )


@server.route("/dashboard/nilai/murid/<id>/tambah", methods=["GET", "POST"])
def tambah_nilai_murid(id):
    murid = MuridModel.query.get(id)
    form = TambahNilaiMuridForm()
    if form.validate_on_submit():
        tambah_nilai_murid = NilaiModel(
            nama=form.nama.data,
            deskripsi=form.deskripsi.data,
            semester=form.semester.data,
            jenis_penilaian=form.jenis_penilaian.data,
            tahun_pelajaran=form.tahun_pelajaran.data,
            murid_id=murid.id,
        )
        db.session.add(tambah_nilai_murid)
        db.session.commit()
        flash("Nilai murid telah ditambahkan.", "Berhasil")
        return redirect(url_for("server.data_nilai_murid", id=id))
    return render_template(
        "nilai/tambahUbahNilaiMurid.html",
        title="Tambah Nilai {}".format(murid.nama),
        form=form,
        murid=murid,
    )


@server.route("/dashboard/nilai/murid/<id>/ubah", methods=["GET", "POST"])
def ubah_nilai_murid(id):
    nilai = NilaiModel.query.get(id)
    form = TambahNilaiMuridForm()
    if form.validate_on_submit():
        nilai.nama = form.nama.data
        nilai.deskripsi = form.deskripsi.data
        nilai.jenis_penilaian = form.jenis_penilaian.data
        nilai.semester = form.semester.data
        nilai.tahun_pelajaran = form.tahun_pelajaran.data
        nilai.murid_id = nilai.murid_id

        db.session.add(nilai)
        db.session.commit()
        flash("Nilai telah diubah", "Berhasil")
        return redirect(url_for("server.data_nilai_murid", id=nilai.murid_id))

    if request.method == "GET":
        form.nama.data = nilai.nama
        form.deskripsi.data = nilai.deskripsi
        form.tahun_pelajaran.data = nilai.tahun_pelajaran
        form.semester.data = nilai.semester
        form.jenis_penilaian.data = nilai.jenis_penilaian
    return render_template(
        "nilai/tambahUbahNilaiMurid.html", title=nilai.nama, form=form
    )


@server.route("/dashboard/nilai/murid/<id>/hapus")
def hapus_nilai_murid(id):
    nilai = NilaiModel.query.get(id)
    db.session.delete(nilai)
    db.session.commit()
    flash("Nilai telah dihapus.", "Berhasil")
    return redirect(url_for("server.data_nilai_murid", id=nilai.murid_id))
