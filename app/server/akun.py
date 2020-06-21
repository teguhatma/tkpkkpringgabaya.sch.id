from . import server
from flask import render_template, flash, redirect, url_for, request
from .forms import AkunForm
from app import db
from app.models import MuridModel, GuruModel
from flask_login import login_required
from ..decorators import admin_guru_required


@server.route("/dashboard/akun/guru/<id>", methods=["GET", "POST"])
@admin_guru_required
@login_required
def akun_guru(id):
    akun = GuruModel.query.get(id)
    form = AkunForm()
    if form.validate_on_submit():
        akun.user.email = form.email.data
        akun.user.password(form.password.data)
        db.session.add(akun)
        db.session.commit()
        flash("Password berhasil ditambahkan", "Berhasil")
        return redirect(url_for("server.lihat_guru", id=id))
    elif request.method == "GET":
        form.email.data = akun.user.email
    return render_template(
        "akun/password.html", form=form, title="Password", akun_guru=akun
    )


@server.route("/dashboard/akun/murid/<id>", methods=["GET", "POST"])
@admin_guru_required
@login_required
def akun_murid(id):
    akun_murid = MuridModel.query.get(id)
    form = AkunForm()
    if form.validate_on_submit():
        akun_murid.user.email = form.email.data
        akun_murid.user.password(form.password.data)
        db.session.add(akun_murid)
        db.session.commit()
        flash("Password berhasil ditambahkan", "Berhasil")
        return redirect(url_for("server.lihat_murid", id=id))
    elif request.method == "GET":
        form.email.data = akun_murid.user.email
    return render_template("akun/password.html", form=form, title=akun_murid.nama)


@server.route("/back_office")
def back():
    return render_template("dashboard.html")

