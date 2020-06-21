from flask import render_template, flash, redirect, url_for, request, send_file
from io import BytesIO
import uuid
from app import db
from . import server
from app.models import ProfileSekolahModel
from .forms import TambahUbahProfileForm
from flask_login import login_required
from ..decorators import admin_required, admin_guru_required


@server.route("/dashboard/profil-sekolah", methods=["GET", "POST"])
@admin_required
@login_required
def profile_sekolah():
    form = TambahUbahProfileForm()
    profile = ProfileSekolahModel.query.first()
    if profile is None:
        if form.validate_on_submit():
            tambah_profile = ProfileSekolahModel(
                nama_lembaga=form.nama_lembaga.data,
                kode_pos=form.kode_pos.data,
                kelurahan=form.kelurahan.data,
                kecamatan=form.kecamatan.data,
                kabupaten=form.kabupaten.data,
                provinsi=form.provinsi.data,
                no_statistik=form.no_statistik.data,
                alamat=form.alamat.data,
                akte_notaris=form.akte_notaris.data,
                kegiatan_belajar=form.kegiatan_belajar.data,
                tahun_berdiri=form.tahun_berdiri.data,
                status_tk=form.status_tk.data,
                no_izin_pendirian=form.no_izin_pendirian.data,
                no_izin_operasional=form.no_izin_operasional.data,
                kurikulum=form.kurikulum.data,
                no_telepon=form.no_telepon.data,
                email=form.email.data,
                visi_misi=form.visi_misi.data,
            )
            db.session.add(tambah_profile)
            db.session.commit()
            flash("Profile sekolah berhasil ditambah", "info")
            return redirect(url_for("server.profile_sekolah"))
    else:
        if form.validate_on_submit():
            profile.nama_lembaga = form.nama_lembaga.data
            profile.kode_pos = form.kode_pos.data
            profile.kelurahan = form.kelurahan.data
            profile.kecamatan = form.kecamatan.data
            profile.kabupaten = form.kabupaten.data
            profile.provinsi = form.provinsi.data
            profile.no_statistik = form.no_statistik.data
            profile.akte_notaris = form.akte_notaris.data
            profile.kegiatan_belajar = form.kegiatan_belajar.data
            profile.tahun_berdiri = form.tahun_berdiri.data
            profile.status_tk = form.status_tk.data
            profile.no_izin_pendirian = form.no_izin_pendirian.data
            profile.no_izin_operasional = form.no_izin_operasional.data
            profile.kurikulum = form.kurikulum.data
            profile.no_telepon = form.no_telepon.data
            profile.email = form.email.data
            profile.alamat = form.alamat.data
            profile.visi_misi = form.visi_misi.data
            db.session.add(profile)
            db.session.commit()
            flash("Profile sekolah berhasil diubah", "info")
            return redirect(url_for("server.profile_sekolah"))

        form.nama_lembaga.data = profile.nama_lembaga
        form.kode_pos.data = profile.kode_pos
        form.kelurahan.data = profile.kelurahan
        form.kecamatan.data = profile.kecamatan
        form.kabupaten.data = profile.kabupaten
        form.provinsi.data = profile.provinsi
        form.no_statistik.data = profile.no_statistik
        form.akte_notaris.data = profile.akte_notaris
        form.kegiatan_belajar.data = profile.kegiatan_belajar
        form.tahun_berdiri.data = profile.tahun_berdiri
        form.status_tk.data = profile.status_tk
        form.alamat.data = profile.alamat
        form.no_izin_operasional.data = profile.no_izin_operasional
        form.no_izin_pendirian.data = profile.no_izin_pendirian
        form.kurikulum.data = profile.kurikulum
        form.no_telepon.data = profile.no_telepon
        form.email.data = profile.email
        form.visi_misi.data = profile.visi_misi

    return render_template(
        "profile/tambahUbahProfile.html", title="Profil Sekolah", form=form
    )
