from . import server
from flask import render_template, request, redirect, url_for
from app.models import (
    GuruModel,
    MuridModel,
    WaliMuridModel,
    PrestasiModel,
    KelasModel,
    NilaiModel,
)
from flask_login import login_required
from ..decorators import admin_guru_required
from datetime import datetime


@server.route("/report/guru")
@login_required
@admin_guru_required
def report_guru():
    data_guru = GuruModel.query.order_by(GuruModel.jabatan.asc()).all()
    return render_template(
        "report/xls_guru.html", title="Data Guru", data_guru=data_guru
    )


@server.route("/report/murid")
@login_required
@admin_guru_required
def report_murid():
    data_murid = MuridModel.query.order_by(MuridModel.nomor_induk.asc()).all()
    return render_template(
        "report/xls_murid.html", title="Data Murid", data_murid=data_murid
    )


@server.route("/report/wali-murid")
@login_required
@admin_guru_required
def report_wali():
    data_wali = WaliMuridModel.query.order_by(WaliMuridModel.nama.asc()).all()
    return render_template(
        "report/xls_wali.html", title="Data Wali Murid", data_wali=data_wali
    )


@server.route("/report/prestasi")
@login_required
@admin_guru_required
def report_prestasi():
    data_prestasi = PrestasiModel.query.order_by(PrestasiModel.tahun.desc()).all()
    return render_template(
        "report/xls_prestasi.html", title="Data Prestasi", data_prestasi=data_prestasi
    )


@server.route("/report/nilai/<ruang_id>")
@login_required
@admin_guru_required
def report_nilai(ruang_id):
    kelas = KelasModel.query.order_by(KelasModel.ruang.asc()).all()
    semester = {semester.semester for semester in NilaiModel.query.all()}

    tahun_pelajaran = {tahun.tahun_pelajaran for tahun in NilaiModel.query.all()}

    title = KelasModel.query.filter_by(id=ruang_id).first()
    data = MuridModel.query.filter_by(kelas_id=ruang_id).all()
    return render_template(
        "report/nilai_murid.html",
        data=data,
        title="Cetak nilai kelas {}".format(title.ruang),
        kelas=kelas,
        ruang_id=ruang_id,
        semester=semester,
        tahun_pelajaran=tahun_pelajaran,
    )


@server.route("/report/nilai/<semester>/<tahun_pelajaran>/<id>")
@admin_guru_required
@login_required
def report_nilai_murid(semester, tahun_pelajaran, id):
    murid = (
        NilaiModel.query.filter_by(semester=semester)
        .filter_by(tahun_pelajaran=tahun_pelajaran)
        .all()
    )
    kelas = KelasModel.query.order_by(KelasModel.ruang.asc()).all()

    return render_template(
        "report/nilai_murid.html",
        murid=murid,
        semester=semester,
        tahun_pelajaran=tahun_pelajaran,
        kelas=kelas,
        title="Nilai Murid",
    )


@server.route("/print/<id>", methods=["POST"])
@admin_guru_required
@login_required
def print_murid(id):
    semester = request.form.get("semester")
    tahun = request.form.get("tahun")

    murid = MuridModel.query.get(id)

    nilai_murid = NilaiModel.query.filter_by(murid_id=murid.id).filter_by(semester=semester).filter_by(tahun_pelajaran=tahun).all()

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
        semester=semester,
        tahun=tahun,
        date=datetime.utcnow(),
        wali_murid=wali_murid,
        kepala_sekolah=kepala_sekolah,
    )
