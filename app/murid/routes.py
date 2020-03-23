from . import murid
from app import db
from app.models import JadwalKelasModel, MuridModel, WaliMuridModel, NilaiModel
from flask import render_template, send_file, flash, redirect, url_for
from flask_login import login_required, current_user
from io import BytesIO
from .forms import MuridGantiPasswordForm


@murid.route("/image/murid/foto/<filename>")
@login_required
def foto_murid(filename):
    data = MuridModel.query.filter_by(nama_foto_diri=filename).first()
    return send_file(
        BytesIO(data.foto_diri),
        mimetype="images/generic",
        as_attachment=True,
        attachment_filename=data.nama_foto_diri,
    )


@murid.route("/murid/dashboard")
@login_required
def murid_dashboard():
    jadwal = (
        JadwalKelasModel.query.filter_by(kelas_id=current_user.id)
        .order_by(JadwalKelasModel.hari.asc())
        .order_by(JadwalKelasModel.jam.asc())
        .all()
    )
    return render_template("dashboardMurid.html", title="Dashboard", jadwal=jadwal)


@murid.route("/murid/profile")
@login_required
def murid_profile():
    wali = WaliMuridModel.query.filter_by(murid_id=current_user.id).first()
    murid = MuridModel.query.filter_by(id=current_user.id).first()
    return render_template(
        "profileMurid.html", wali=wali, murid=murid, title="Profile Peserta Didik"
    )


@murid.route("/murid/nilai")
@login_required
def murid_nilai():
    nilai = NilaiModel.query.filter_by(murid_id=current_user.id).all()
    return render_template("nilaiMurid.html", nilai=nilai, title="Nilai Peserta Didik")


@murid.route("/student/akun", methods=["GET", "POST"])
@login_required
def murid_ganti_password():
    akun = MuridModel.query.filter_by(id=current_user.id).first()
    form = MuridGantiPasswordForm()
    if form.validate_on_submit():
        if akun.verify_password(form.password.data) == True:
            akun.password(form.new_password.data)

            db.session.commit()
            flash("Passsword telah diubah.", "Berhasil")
            return redirect(url_for("murid.murid_ganti_password"))

        elif akun.verify_password(form.password.data) == False:
            flash("Password anda salah.")
            return redirect(url_for("murid.murid_ganti_password"))

    return render_template(
        "loginMurid.html", title="Ganti Password Peserta Didik", form=form
    )

