from flask import render_template, flash, redirect, url_for
import uuid
from app import db
from . import server
from app.models import KelasModel
from .forms import TambahKelasForm
from flask_login import login_required
from ..decorators import admin_required, admin_guru_required


@server.route("/dashboard/kelas")
@admin_guru_required
@login_required
def data_kelas():
    kelas_side = KelasModel.query.order_by(KelasModel.ruang.asc()).all()
    kelas = KelasModel.query.all()
    return render_template(
        "kelas/dataKelas.html", data_kelas=kelas, title="Data Kelas", kelas=kelas_side
    )


@server.route("/dashboard/kelas/tambah", methods=["GET", "POST"])
@admin_required
@login_required
def tambah_kelas():
    kelas = KelasModel.query.order_by(KelasModel.ruang.asc()).all()
    form = TambahKelasForm()
    if form.validate_on_submit():
        tambah_kelas = KelasModel(ruang=form.ruang.data.upper())
        db.session.add(tambah_kelas)
        db.session.commit()
        flash("Ruang kelas {} sudah terbuat".format(tambah_kelas.ruang))
        return redirect(url_for("server.data_kelas"))
    return render_template(
        "kelas/tambahKelas.html", title="Menambah Kelas", form=form, kelas=kelas
    )


@server.route("/dashboard/kelas/hapus/<id>")
@admin_required
@login_required
def hapus_kelas(id):
    hapus_kelas = KelasModel.query.get(id)
    db.session.delete(hapus_kelas)
    db.session.commit()
    flash("Ruang kelas {} sudah dihapus".format(hapus_kelas.ruang))
    return redirect(url_for("server.data_kelas"))
