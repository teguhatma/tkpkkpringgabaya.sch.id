from . import client
from flask import render_template, send_file, request, url_for
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
    page = request.args.get("page", 1, type=int)
    berita = BeritaModel.query.filter(BeritaModel.tampilkan == True).first()
    all_berita = (
        BeritaModel.query.filter(BeritaModel.tampilkan == True)
        .order_by(BeritaModel.waktu_upload.desc())
        .paginate(page, 6, False)
    )

    learning = ElearningModel.query.order_by(
        ElearningModel.waktu_upload.asc()
    ).paginate(page, 6, False)
    profile = ProfileSekolahModel.query.first()

    return render_template(
        "index.html",
        title="TK PKK Pringgabaya",
        berita=berita,
        learning=learning.items,
        all_berita=all_berita.items,
        profile=profile,
    )


@client.route("/<slug>")
def lihat_berita(slug):
    arsip_berita = (
        BeritaModel.query.filter(BeritaModel.tampilkan == True)
        .order_by(BeritaModel.waktu_upload.desc())
        .limit(5)
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
        title="Prestasi Sekolah",
        prestasi=prestasi,
        arsip_berita=arsip_berita,
    )


@client.route("/e-learning")
def learning():
    page = request.args.get("page", 1, type=int)
    learning = ElearningModel.query.order_by(
        ElearningModel.waktu_upload.desc()
    ).paginate(page, 12, False)
    next_url = (
        url_for("client.learning", page=learning.next_num)
        if learning.has_next
        else None
    )
    prev_url = (
        url_for("client.learning", page=learning.prev_num)
        if learning.has_prev
        else None
    )
    profile = ProfileSekolahModel.query.first()
    return render_template(
        "lihatElearning.html",
        title="E-Learning",
        learning=learning.items,
        prev_url=prev_url,
        next_url=next_url,
        profile=profile,
    )


@client.route("/berita")
def berita():
    page = request.args.get("page", 1, type=int)
    all_berita = (
        BeritaModel.query.filter(BeritaModel.tampilkan == True)
        .order_by(BeritaModel.waktu_upload.desc())
        .paginate(page, 9, False)
    )
    next_url = (
        url_for("client.berita", page=all_berita.next_num)
        if all_berita.has_next
        else None
    )
    prev_url = (
        url_for("client.berita", page=all_berita.prev_num)
        if all_berita.has_prev
        else None
    )
    profile = ProfileSekolahModel.query.first()
    return render_template(
        "berita.html",
        title="Berita Sekolah",
        berita=all_berita.items,
        profile=profile,
        next_url=next_url,
        prev_url=prev_url,
    )
