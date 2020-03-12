from . import server
from app import db
from flask import (
    render_template,
    redirect,
    url_for,
    redirect,
    flash,
    request,
    send_file,
)
from app.models import PegawaiModel
import uuid
from io import BytesIO
from .forms import TambahPegawaiForm, RubahPegawaiForm


@server.route("/image/pegawai/foto/<filename>")
def foto_pegawai(filename):
    data = PegawaiModel.query.filter_by(nama_foto=filename).first()
    return send_file(
        BytesIO(data.foto),
        mimetype="images/generic",
        as_attachment=True,
        attachment_filename=data.nama_foto,
    )


@server.route("/dashboard/pegawai")
def data_pegawai():
    data_pegawai = PegawaiModel.query.all()
    return render_template(
        "pegawai/dataPegawai.html",
        title="Daftar data pegawai",
        data_pegawai=data_pegawai,
    )


@server.route("/dashboard/pegawai/hapus/<id>", methods=["GET", "POST"])
def hapus_pegawai():
    hapus_pegawai = PegawaiModel.query.get(id)
    db.session.delete(hapus_pegawai)
    db.session.commit()
    flash("{} Berhasil dihapus", "Berhasil")
    return redirect(url_for("server.data_pegawai"))


@server.route("/dashboard/pegawai/tambah", methods=["GET", "POST"])
def tambah_pegawai():
    form = TambahPegawaiForm()
    if form.validate_on_submit():
        tambah_pegawai = PegawaiModel(
            nama=form.nama.data,
            alamat=form.alamat.data,
            kelurahan=form.kelurahan.data,
            kecamatan=form.kecamatan.data,
            kabupaten=form.kabupaten.data,
            provinsi=form.provinsi.data,
            agama=form.agama.data,
            tempat_lahir=form.tempat_lahir.data,
            tanggal_lahir=form.tanggal_lahir.data,
            foto=form.foto.data.read(),
            nama_foto="{}".format(uuid.uuid4().hex),
            pendidikan_terakhir=form.pendidikan_terakhir.data,
            jenis_kelamin=form.jenis_kelamin.data,
            tahun_masuk=form.tahun_masuk.data,
            email=form.email.data,
        )
        db.session.add(tambah_pegawai)
        db.session.commit()
        return redirect(url_for("server.data_pegawai"))
    return render_template(
        "pegawai/tambahPegawai.html", title="Tambah pegawai", form=form
    )


@server.route("/dashboard/pegawai/ubah/<id>", methods=["GET", "POST"])
def ubah_pegawai(id):
    form = RubahPegawaiForm()
    pegawai = PegawaiModel.query.get(id)
    if form.validate_on_submit():
        pegawai.nama = form.nama.data
        pegawai.alamat = form.alamat.data
        pegawai.kelurahan = form.kelurahan.data
        pegawai.kecamatan = form.kecamatan.data
        pegawai.kabupaten = form.kabupaten.data
        pegawai.provinsi = form.provinsi.data
        pegawai.agama = form.agama.data
        pegawai.tempat_lahir = form.tempat_lahir.data
        pegawai.tanggal_lahir = form.tanggal_lahir.data
        pegawai.pendidikan_terakhir = form.pendidikan_terakhir.data
        pegawai.jenis_kelamin = form.jenis_kelamin.data
        pegawai.tahun_masuk = form.tahun_masuk.data
        pegawai.email = form.email.data
        if form.foto.data is not None:
            pegawai.foto = form.foto.data.read()
            pegawai.nama_foto = "{}".format(uuid.uuid4().hex)
        elif form.foto.data is None:
            pegawai.foto = pegawai.foto
            pegawai.nama_foto = pegawai.nama_foto
        db.session.add(pegawai)
        db.session.commit()
        flash("Data {} berhasil diubah.".format(pegawai.nama), "Berhasil")
        return redirect(url_for("server.data_pegawai"))

    if request.method == "GET":
        form.nama.data = pegawai.nama
        form.alamat.data = pegawai.alamat
        form.kelurahan.data = pegawai.kelurahan
        form.kecamatan.data = pegawai.kecamatan
        form.kabupaten.data = pegawai.kabupaten
        form.provinsi.data = pegawai.provinsi
        form.agama.data = pegawai.agama
        form.tempat_lahir.data = pegawai.tempat_lahir
        form.tanggal_lahir.data = pegawai.tanggal_lahir
        form.foto.data = pegawai.foto
        form.pendidikan_terakhir.data = pegawai.pendidikan_terakhir
        form.jenis_kelamin.data = pegawai.jenis_kelamin
        form.tahun_masuk.data = pegawai.tahun_masuk
        form.email.data = pegawai.email
        form.email_hidden.data = pegawai.email

    return render_template("pegawai/ubahPegawai.html", title=pegawai.nama, form=form)


@server.route("/dashboard/pegawai/lihat/<id>", methods=["GET", "POST"])
def lihat_pegawai(id):
    pegawai = PegawaiModel.query.get(id)
    return render_template(
        "pegawai/lihatPegawai.html", pegawai=pegawai, title=pegawai.nama
    )
