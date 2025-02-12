from . import murid
from app import db
from app.models import (
    JadwalKelasModel,
    MuridModel,
    WaliMuridModel,
    NilaiModel,
    UserModel,
    GuruModel,
)
from flask import render_template, send_file, flash, redirect, url_for, request
from flask_login import login_required, current_user
from io import BytesIO
from .forms import (
    MuridGantiPasswordForm,
    MuridGantiProfileForm,
    MuridGantiProfileWaliForm,
)
from ..decorators import murid_required
from datetime import datetime


@murid.route("/image/murid/<filename>")
@murid_required
@login_required
def foto_diri_murid(filename):
    data = MuridModel.query.filter_by(nama_foto_diri=filename).first()
    return send_file(
        BytesIO(data.foto_diri),
        mimetype="images/generic",
        as_attachment=True,
        attachment_filename=data.nama_foto_diri,
    )


@murid.route("/murid/dashboard")
@murid_required
@login_required
def murid_dashboard():
    jadwal = (
        JadwalKelasModel.query.filter_by(kelas_id=current_user.murid.kelas.id)
        .order_by(JadwalKelasModel.hari.asc())
        .order_by(JadwalKelasModel.jam.asc())
        .all()
    )
    return render_template("dashboardMurid.html", title="Dashboard", jadwal=jadwal)


@murid.route("/murid/profile")
@murid_required
@login_required
def murid_profile():
    wali = WaliMuridModel.query.filter_by(murid_id=current_user.murid.id).first()
    murid = MuridModel.query.filter_by(id=current_user.murid.id).first()
    return render_template(
        "profileMurid.html", wali=wali, murid=murid, title="Profile Peserta Didik"
    )


@murid.route("/murid/nilai", methods=["GET", "POST"])
@murid_required
@login_required
def murid_nilai():
    semester = {semester.semester for semester in NilaiModel.query.all()}

    tahun_pelajaran = {tahun.tahun_pelajaran for tahun in NilaiModel.query.all()}
    return render_template(
        "nilaiMurid.html",
        semester=semester,
        tahun_pelajaran=tahun_pelajaran,
        title="Nilai Peserta Didik",
    )


@murid.route("/murid/ganti-password", methods=["GET", "POST"])
@murid_required
@login_required
def murid_ganti_password():
    akun = UserModel.query.filter_by(id=current_user.id).first()
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


@murid.route("/murid/profile/ubah", methods=["POST", "GET"])
@murid_required
@login_required
def murid_ganti_profile_diri():
    form = MuridGantiProfileForm()
    murid = MuridModel.query.filter_by(id=current_user.murid.id).first_or_404()
    if form.validate_on_submit():
        murid.nama = form.nama.data
        murid.nama_panggilan = form.nama_panggilan.data
        murid.anak_ke = form.anak_ke.data
        murid.nama_ibu_kandung = form.nama_ibu_kandung.data
        murid.agama = form.agama.data
        murid.jenis_kelamin = form.jenis_kelamin.data
        murid.tempat_lahir = form.tempat_lahir.data
        murid.tanggal_lahir = form.tanggal_lahir.data
        murid.alamat = form.alamat.data
        murid.kelurahan = form.kelurahan.data
        murid.kecamatan = form.kecamatan.data
        murid.kabupaten = form.kabupaten.data
        murid.provinsi = form.provinsi.data

        db.session.commit()
        flash("Data berhasil tersimpan", "Berhasil")
        return redirect(url_for("murid.murid_profile"))

    if request.method == "GET":
        form.nama.data = murid.nama
        form.nama_panggilan.data = murid.nama_panggilan
        form.anak_ke.data = murid.anak_ke
        form.nama_ibu_kandung.data = murid.nama_ibu_kandung
        form.agama.data = murid.agama
        form.jenis_kelamin.data = murid.jenis_kelamin
        form.tempat_lahir.data = murid.tempat_lahir
        form.tanggal_lahir.data = murid.tanggal_lahir
        form.alamat.data = murid.alamat
        form.kecamatan.data = murid.kecamatan
        form.kabupaten.data = murid.kabupaten
        form.kelurahan.data = murid.kelurahan
        form.provinsi.data = murid.provinsi

    return render_template("ubahProfile.html", title="Profile Peserta Didik", form=form)


@murid.route("/murid/profile/wali-murid/ubah", methods=["POST", "GET"])
@murid_required
@login_required
def murid_ganti_profile_wali():
    form = MuridGantiProfileWaliForm()
    wali = WaliMuridModel.query.filter_by(murid_id=current_user.murid.id).first_or_404()
    if form.validate_on_submit():
        wali.nama = form.nama.data
        wali.agama = form.agama.data
        wali.jenis_kelamin = form.jenis_kelamin.data
        wali.tempat_lahir = form.tempat_lahir.data
        wali.tanggal_lahir = form.tanggal_lahir.data
        wali.pekerjaan = form.pekerjaan.data
        wali.nomor_telepon = form.nomor_telepon.data
        wali.alamat = form.alamat.data
        wali.kelurahan = form.kelurahan.data
        wali.kecamatan = form.kecamatan.data
        wali.kabupaten = form.kabupaten.data
        wali.provinsi = form.provinsi.data

        db.session.commit()
        flash("Data berhasil tersimpan", "Berhasil")
        return redirect(url_for("murid.murid_profile"))

    if request.method == "GET":
        form.nama.data = wali.nama
        form.nomor_telepon.data = wali.nomor_telepon
        form.pekerjaan.data = wali.pekerjaan
        form.agama.data = wali.agama
        form.jenis_kelamin.data = wali.jenis_kelamin
        form.tempat_lahir.data = wali.tempat_lahir
        form.tanggal_lahir.data = wali.tanggal_lahir
        form.alamat.data = wali.alamat
        form.kecamatan.data = wali.kecamatan
        form.kabupaten.data = wali.kabupaten
        form.kelurahan.data = wali.kelurahan
        form.provinsi.data = wali.provinsi

    return render_template(
        "ubahWali.html", title="Profile Wali Peserta Didik", form=form
    )


@murid.route("/print", methods=["POST"])
@murid_required
@login_required
def print_murid_murid():
    semester = request.form.get("semester")
    tahun = request.form.get("tahun")

    murid = MuridModel.query.get(current_user.murid.id)

    nilai_murid = (
        NilaiModel.query.filter_by(murid_id=murid.id)
        .filter_by(semester=semester)
        .filter_by(tahun_pelajaran=tahun)
        .all()
    )

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