from . import server
from app import db
from flask import render_template, request, flash, url_for, redirect, send_file
from io import BytesIO
from app.models import (
    MuridModel,
    NilaiModel,
    GuruModel,
    WaliMuridModel,
    GuruModel,
    KelasModel,
)
from .forms import TambahNilaiMuridForm
import uuid
from datetime import datetime
from flask_login import login_required, current_user
from ..decorators import admin_guru_required


@server.route("/dashboard/nilai/murid")
@admin_guru_required
@login_required
def nilai_murid():
    kelas = KelasModel.query.order_by(KelasModel.ruang.asc()).all()
    if current_user.is_administrator():
        nilai_murid = MuridModel.query.all()
    else:
        nilai_murid = MuridModel.query.filter_by(
            kelas_id=current_user.guru.kelas.id
        ).all()
    return render_template(
        "nilai/dataNilaiMurid.html",
        title="Data Nilai Murid",
        nilai_murid=nilai_murid,
        kelas=kelas,
    )


@server.route("/dashboard/nilai/murid/<id>", methods=["GET", "POST"])
@admin_guru_required
@login_required
def data_nilai_murid(id):
    kelas = KelasModel.query.order_by(KelasModel.ruang.asc()).all()
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
        kelas=kelas,
    )


@server.route("/dashboard/nilai/murid/<id>/select", methods=["GET", "POST"])
@admin_guru_required
@login_required
def data_nilai_murid_select(id):
    kelas = KelasModel.query.order_by(KelasModel.ruang.asc()).all()
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
        kelas=kelas,
    )


@server.route("/dashboard/nilai/murid/<id>/tambah", methods=["GET", "POST"])
@admin_guru_required
@login_required
def tambah_nilai_murid(id):
    kelas = KelasModel.query.order_by(KelasModel.ruang.asc()).all()
    murid = MuridModel.query.get(id)
    form = TambahNilaiMuridForm()
    if form.validate_on_submit():
        data = (
            NilaiModel.query.filter_by(aspek_penilaian=form.aspek_penilaian.data)
            .filter_by(semester=form.semester.data)
            .filter_by(tahun_pelajaran=form.tahun_pelajaran.data)
            .first()
        )
        if data is not None:
            flash(
                "Nilai {} pada {} tahun {} sudah ada.".format(
                    form.aspek_penilaian.data,
                    form.semester.data,
                    form.tahun_pelajaran.data,
                )
            )
            return redirect(url_for(".tambah_nilai_murid", id=id))
        else:
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
        kelas=kelas,
    )


@server.route("/dashboard/nilai/murid/<id>/ubah", methods=["GET", "POST"])
@admin_guru_required
@login_required
def ubah_nilai_murid(id):
    kelas = KelasModel.query.order_by(KelasModel.ruang.asc()).all()
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
        form.aspek_penilaian.data = nilai.aspek_penilaian
    return render_template(
        "nilai/tambahUbahNilaiMurid.html",
        title=nilai.aspek_penilaian,
        form=form,
        kelas=kelas,
    )


@server.route("/dashboard/nilai/murid/<id>/hapus")
@admin_guru_required
@login_required
def hapus_nilai_murid(id):
    nilai = NilaiModel.query.get(id)
    db.session.delete(nilai)
    db.session.commit()
    flash("Nilai telah dihapus.", "Berhasil")
    return redirect(url_for("server.data_nilai_murid", id=nilai.murid_id))


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
