from . import server
from flask import render_template, flash, redirect, url_for
from .forms import AkunForm
from app import db
from app.models import GuruModel, PegawaiModel, MuridModel


@server.route("/dashboard/akun/guru/<id>", methods=["GET", "POST"])
def akun_guru(id):
    akun_guru = GuruModel.query.get(id)
    form = AkunForm()
    if form.validate_on_submit():
        akun_guru.password(form.password.data)
        db.session.add(akun_guru)
        db.session.commit()
        flash("Password berhasil ditambahkan", "Berhasil")
        return redirect(url_for("server.lihat_guru", id=id))
    return render_template(
        "akun/password.html", form=form, title=akun_guru.nama, akun_guru=akun_guru
    )


@server.route("/dashboard/akun/pegawai/<id>", methods=["GET", "POST"])
def akun_pegawai(id):
    akun_pegawai = PegawaiModel.query.get(id)
    form = AkunForm()
    if form.validate_on_submit():
        akun_pegawai.password(form.password.data)
        db.session.add(akun_pegawai)
        db.session.commit()
        flash("Password berhasil ditambahkan", "Berhasil")
        return redirect(url_for("server.lihat_pegawai", id=id))
    return render_template("akun/password.html", form=form, title=akun_pegawai.nama)


@server.route("/dashboard/akun/murid/<id>", methods=["GET", "POST"])
def akun_murid(id):
    akun_murid = MuridModel.query.get(id)
    form = AkunForm()
    if form.validate_on_submit():
        akun_murid.password(form.password.data)
        db.session.add(akun_murid)
        db.session.commit()
        flash("Password berhasil ditambahkan", "Berhasil")
        return redirect(url_for("server.lihat_murid", id=id))
    return render_template("akun/password.html", form=form, title=akun_murid.nama)
