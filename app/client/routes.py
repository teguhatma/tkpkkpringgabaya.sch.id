from . import client
from flask import render_template, send_file
from app.models import (
    BeritaModel,
    ElearningModel,
    JadwalKelasModel,
    KelasModel,
    GuruModel,
)
from app import db
from io import BytesIO


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

    return render_template(
        "index.html",
        title="TK PKK Pringgabaya",
        berita=berita,
        learning=learning,
        all_berita=all_berita,
    )


@client.route("/<slug>")
def lihat_berita(slug):
    arsip_berita = (
        BeritaModel.query.filter(BeritaModel.tampilkan == True)
        .order_by(BeritaModel.waktu_upload.desc())
        .all()
    )
    berita = BeritaModel.query.filter_by(slug=slug).first_or_404()
    return render_template(
        "lihatBerita.html", title=berita.judul, berita=berita, arsip_berita=arsip_berita
    )
