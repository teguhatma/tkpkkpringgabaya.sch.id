from flask import render_template, flash, redirect, url_for
import uuid
from app import db
from . import server
from app.models import GuruModel
from .forms import TambahGuruForm


@server.route("/dashboard/guru")
def data_guru():
    data_guru = GuruModel.query.all()
    return render_template("dataGuru.html", title="Data guru", data_guru=data_guru)


@server.route("/dashboard/guru/tambah", methods=["GET", "POST"])
def tambah_guru():
    form = TambahGuruForm()
    if form.validate_on_submit():
        tambah_guru = GuruModel(
            nama=form.nama.data,
            alamat=form.alamat.data,
            nik=form.nik.data,
            email=form.email.data,
            kelurahan=form.kelurahan.data,
            kecamatan=form.kecamatan.data,
            kabupaten=form.kabupaten.data,
            provinsi=form.provinsi.data,
            agama=form.agama.data,
            tempat_lahir=form.tempat_lahir.data,
            tanggal_lahir=form.tanggal_lahir.data,
            jabatan=form.jabatan.data,
            foto=form.foto.data.read(),
            nama_foto="{}".format(uuid.uuid4().hex),
            foto_ijazah=form.foto_ijazah.data.read(),
            nama_foto_ijazah="{}".format(uuid.uuid4().hex),
            pendidikan_terakhir=form.pendidikan_terakhir.data,
            jenis_kelamin=form.jenis_kelamin.data,
            tahun_masuk=form.tahun_masuk.data,
            golongan=form.golongan.data,
            kelas_id=form.kelas.data.id,
        )
        db.session.add(tambah_guru)
        db.session.commit()
        flash("Data sudah ditambahkan", "Berhasil")
        return redirect(url_for("server.data_guru"))
    return render_template("tambahGuru.html", title="Menambah data guru", form=form)

