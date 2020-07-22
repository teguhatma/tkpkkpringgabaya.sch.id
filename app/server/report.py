from . import server
from flask import render_template
from app.models import GuruModel, MuridModel, WaliMuridModel, PrestasiModel
from flask_login import login_required
from ..decorators import admin_guru_required

@server.route('/report/guru')
@login_required
@admin_guru_required
def report_guru():
    data_guru = GuruModel.query.order_by(GuruModel.jabatan.asc()).all()
    return render_template('report/xls_guru.html', title="Data Guru", data_guru=data_guru)

@server.route('/report/murid')
@login_required
@admin_guru_required
def report_murid():
    data_murid = MuridModel.query.order_by(MuridModel.nomor_induk.asc()).all()
    return render_template('report/xls_murid.html', title="Data Murid", data_murid=data_murid)

@server.route('/report/wali-murid')
@login_required
@admin_guru_required
def report_wali():
    data_wali = WaliMuridModel.query.order_by(WaliMuridModel.nama.asc()).all()
    return render_template('report/xls_wali.html', title="Data Wali Murid", data_wali=data_wali)

@server.route('/report/prestasi')
@login_required
@admin_guru_required
def report_prestasi():
    data_prestasi = PrestasiModel.query.order_by(PrestasiModel.tahun.desc()).all()
    return render_template('report/xls_prestasi.html', title="Data Prestasi", data_prestasi=data_prestasi)