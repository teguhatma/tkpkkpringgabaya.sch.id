from flask import render_template, flash, redirect, url_for
import uuid
from app import db
from . import server
from app.models import KelasModel
from .forms import TambahKelasForm


@server.route("/dashboard/kelas")
def data_kelas():
    kelas = KelasModel.query.all()
    return render_template("dataKelas.html", kelas=kelas, title="Data Kelas")


@server.route("/dashboard/kelas/tambah", methods=["GET", "POST"])
def tambah_kelas():
    form = TambahKelasForm()
    if form.validate_on_submit():
        tambah_kelas = KelasModel(ruang=form.ruang.data.upper())
        db.session.add(tambah_kelas)
        db.session.commit()
        flash("Ruang kelas {} sudah terbuat".format(tambah_kelas.ruang))
        return redirect(url_for("server.data_kelas"))
    return render_template("tambahKelas.html", title="Menambah Kelas", form=form)


@server.route("/dashboard/kelas/hapus/<id>")
def hapus_kelas(id):
    hapus_kelas = KelasModel.query.get(id)
    db.session.delete(hapus_kelas)
    db.session.commit()
    flash("Ruang kelas {} sudah dihapus".format(hapus_kelas.ruang))
    return redirect(url_for("server.data_kelas"))

