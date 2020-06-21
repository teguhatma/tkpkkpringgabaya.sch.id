from . import server
from app.models import GuruModel, MuridModel, KelasModel, WaliMuridModel
from flask import render_template


@server.route("/dashboard")
def dashboard():
    guru = GuruModel.query.count()
    murid = MuridModel.query.count()
    kelas = KelasModel.query.count()
    wali = WaliMuridModel.query.count()
    murid_baru = MuridModel.query.order_by(MuridModel.id.desc()).all()
    guru_baru = GuruModel.query.order_by(GuruModel.jabatan.asc()).all()
    return render_template(
        "dashboard.html",
        title="Dashboard",
        guru_baru=guru_baru,
        murid_baru=murid_baru,
        guru=guru,
        kelas=kelas,
        wali=wali,
        murid=murid,
    )
