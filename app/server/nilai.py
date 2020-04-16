from . import server
from app import db
from flask import render_template, request, flash, url_for, redirect, send_file
from io import BytesIO
from app.models import MuridModel, NilaiModel, GuruModel, WaliMuridModel, GuruModel
from .forms import TambahNilaiMuridForm
import uuid
from flask_weasyprint import HTML, render_pdf
from datetime import datetime
from flask_login import login_required


@server.route("/dashboard/nilai/murid")
@login_required
def nilai_murid():
    nilai_murid = MuridModel.query.all()
    return render_template(
        "nilai/dataNilaiMurid.html", title="Data nilai murid", nilai_murid=nilai_murid
    )


@server.route("/dashboard/nilai/murid/<id>", methods=["GET", "POST"])
@login_required
def data_nilai_murid(id):
    murid = MuridModel.query.get(id)
    nilai = NilaiModel.query.filter_by(murid_id=murid.id).all()
    number = []
    for a in NilaiModel.query.order_by(NilaiModel.tahun_pelajaran.asc()).all():
        number.append(a.tahun_pelajaran)
    daftar_tahun_nilai = set(number)
    global nilai_selected
    if request.method == "POST":

        nilai_selected = (
            NilaiModel.query.filter_by(tahun_pelajaran=request.form.get("tahun"))
            .filter_by(semester=request.form.get("semester"))
            .all()
        )
        return redirect(url_for("server.data_nilai_murid_select", id=id))
    return render_template(
        "nilai/lihatNilaiMurid.html",
        nilai=nilai,
        nilai_selected=[],
        title="Nilai {}".format(murid.nama),
        daftar_tahun_nilai=daftar_tahun_nilai,
        murid=murid,
    )


@server.route("/dashboard/nilai/murid/<id>/select", methods=["GET", "POST"])
@login_required
def data_nilai_murid_select(id):
    murid = MuridModel.query.get(id)
    nilai = NilaiModel.query.filter_by(murid_id=murid.id).all()
    number = []
    for a in NilaiModel.query.order_by(NilaiModel.tahun_pelajaran.asc()).all():
        number.append(a.tahun_pelajaran)
    daftar_tahun_nilai = set(number)
    global nilai_selected
    if request.method == "POST":

        nilai_selected = (
            NilaiModel.query.filter_by(tahun_pelajaran=request.form.get("tahun"))
            .filter_by(semester=request.form.get("semester"))
            .filter_by(murid_id=murid.id)
            .all()
        )
        print(request.form.get("semester"))
        return redirect(url_for("server.data_nilai_murid_select", id=id))
    return render_template(
        "nilai/lihatNilaiMurid.html",
        nilai_selected=nilai_selected,
        title="Nilai {}".format(murid.nama),
        daftar_tahun_nilai=daftar_tahun_nilai,
        murid=murid,
        nilai=nilai,
    )


@server.route("/dashboard/nilai/murid/<id>/tambah", methods=["GET", "POST"])
@login_required
def tambah_nilai_murid(id):
    murid = MuridModel.query.get(id)
    form = TambahNilaiMuridForm()
    if form.validate_on_submit():
        tambah_nilai_murid = NilaiModel(
            deskripsi=form.deskripsi.data,
            semester=form.semester.data,
            aspek_penilaian=form.aspek_penilaian.data,
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
@login_required
def ubah_nilai_murid(id):
    nilai = NilaiModel.query.get(id)
    form = TambahNilaiMuridForm()
    if form.validate_on_submit():
        nilai.deskripsi = form.deskripsi.data
        nilai.aspek_penilaian = form.aspek_penilaian.data
        nilai.semester = form.semester.data
        nilai.tahun_pelajaran = form.tahun_pelajaran.data
        nilai.murid_id = nilai.murid_id

        db.session.add(nilai)
        db.session.commit()
        flash("Nilai telah diubah", "Berhasil")
        return redirect(url_for("server.data_nilai_murid", id=nilai.murid_id))

    if request.method == "GET":
        form.deskripsi.data = nilai.deskripsi
        form.tahun_pelajaran.data = nilai.tahun_pelajaran
        form.semester.data = nilai.semester
        form.jenis_penilaian.data = nilai.jenis_penilaian
    return render_template(
        "nilai/tambahUbahNilaiMurid.html", title=nilai.nama, form=form
    )


@server.route("/dashboard/nilai/murid/<id>/hapus")
@login_required
def hapus_nilai_murid(id):
    nilai = NilaiModel.query.get(id)
    db.session.delete(nilai)
    db.session.commit()
    flash("Nilai telah dihapus.", "Berhasil")
    return redirect(url_for("server.data_nilai_murid", id=nilai.murid_id))


@server.route("/dashboard/nilai/murid/print/<id>")
@login_required
def print_nilai(id):
    murid = MuridModel.query.get(id)
    nilai_murid = NilaiModel.query.filter_by(murid_id=murid.id).all()
    wali_murid = WaliMuridModel.query.filter_by(murid_id=murid.id).first()
    guru = (
        GuruModel.query.filter_by(kelas_id=murid.kelas.id)
        .filter(GuruModel.jabatan != "Kepala Sekolah")
        .first()
    )
    kepala_sekolah = GuruModel.query.filter_by(jabatan="Kepala Sekolah").first()
    return render_template(
        "components/printNilai.html",
        nilai_murid=nilai_murid,
        murid=murid,
        guru=guru,
        date=datetime.utcnow(),
        wali_murid=wali_murid,
        kepala_sekolah=kepala_sekolah,
    )


# @server.route("/dashboard/nilai/murid/print/<id>/<nama>.pdf")
# def print_nilai_nama(id, nama):
#     murid = MuridModel.query.get(id)
#     date = datetime.utcnow()
#     nilai_murid = NilaiModel.query.filter_by(murid_id=murid.id).all()
#     html = render_template(
#         "components/printNilai.html",
#         nama=nama,
#         guru=guru,
#         nilai_murid=nilai_murid,
#         murid=murid,
#         date=date,
#     )
#     return render_pdf(HTML(string=html))
