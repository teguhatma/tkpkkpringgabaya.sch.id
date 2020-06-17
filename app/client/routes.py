from . import client
from flask import render_template, send_file
from app.models import (
    BeritaModel,
    ElearningModel,
    JadwalKelasModel,
    KelasModel,
    GuruModel,
    ProfileSekolahModel,
    PrestasiModel,
)
from app import db
from io import BytesIO


@client.route("/dokumen/<filename>/file")
def client_berita_dokumen(filename):
    data = BeritaModel.query.filter_by(nama_dokumen=filename).first()
    return send_file(
        BytesIO(data.dokumen),
        mimetype="file/*",
        as_attachment=True,
        attachment_filename=data.nama_dokumen,
    )


@client.route("/images/berita/<filename>")
def image_berita(filename):
    data = BeritaModel.query.filter_by(nama_gambar=filename).first()
    return send_file(
        BytesIO(data.gambar),
        mimetype="images/generic",
        as_attachment=True,
        attachment_filename=data.nama_gambar,
    )


@client.route("/")
def index():
    berita = BeritaModel.query.filter(BeritaModel.tampilkan == True).first()
    all_berita = (
        BeritaModel.query.filter(BeritaModel.tampilkan == True)
        .order_by(BeritaModel.waktu_upload.desc())
        .all()
    )
    learning = ElearningModel.query.order_by(ElearningModel.waktu_upload.asc()).all()
    profile = ProfileSekolahModel.query.first()

    return render_template(
        "index.html",
        title="TK PKK Pringgabaya",
        berita=berita,
        learning=learning,
        all_berita=all_berita,
        profile=profile,
    )


@client.route("/<slug>")
def lihat_berita(slug):
    arsip_berita = (
        BeritaModel.query.filter(BeritaModel.tampilkan == True)
        .order_by(BeritaModel.waktu_upload.desc())
        .all()
    )
    berita = BeritaModel.query.filter_by(slug=slug).first_or_404()
    profile = ProfileSekolahModel.query.first()
    return render_template(
        "lihatBerita.html",
        title=berita.judul,
        berita=berita,
        arsip_berita=arsip_berita,
        profile=profile,
    )


@client.route("/profile-sekolah")
def lihat_profile():
    profile = ProfileSekolahModel.query.first()
    arsip_berita = (
        BeritaModel.query.filter(BeritaModel.tampilkan == True)
        .order_by(BeritaModel.waktu_upload.desc())
        .all()
    )
    return render_template(
        "lihatProfile.html",
        title="Profile Sekolah",
        profile=profile,
        arsip_berita=arsip_berita,
    )


@client.route("/guru-sekolah")
def guru_sekolah():
    arsip_berita = (
        BeritaModel.query.filter(BeritaModel.tampilkan == True)
        .order_by(BeritaModel.waktu_upload.desc())
        .all()
    )
    profile = ProfileSekolahModel.query.first()
    guru = GuruModel.query.order_by(GuruModel.jabatan.asc()).all()
    return render_template(
        "guruSekolah.html",
        title="Guru Sekolah",
        profile=profile,
        guru=guru,
        arsip_berita=arsip_berita,
    )


@client.route("/prestasi")
def prestasi():
    prestasi = PrestasiModel.query.all()
    arsip_berita = (
        BeritaModel.query.filter(BeritaModel.tampilkan == True)
        .order_by(BeritaModel.waktu_upload.desc())
        .all()
    )
    profile = ProfileSekolahModel.query.first()
    return render_template(
        "lihatPrestasi.html",
        profile=profile,
        titile="Prestasi Sekolah",
        prestasi=prestasi,
        arsip_berita=arsip_berita,
    )


@client.route("/e-learning")
def learning():
    learning = ElearningModel.query.order_by(ElearningModel.waktu_upload.asc()).all()
    profile = ProfileSekolahModel.query.first()
    return render_template(
        "lihatElearning.html", title="E-Learning", learning=learning, profile=profile
    )
