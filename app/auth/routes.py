from app.models import MuridModel, AdminModel, GuruModel
from . import auth
from flask import request, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, login_required
from .forms import LoginMuridForm, LoginAdminForm, LoginGuruForm, LoginPegawaiForm


@auth.route("/login/murid", methods=["GET", "POST"])
def login_murid():
    form = LoginMuridForm()
    if form.validate_on_submit():
        murid = MuridModel.query.filter_by(nomor_induk=form.nomor_induk.data).first()
        if murid is not None and murid.verify_password(form.password.data):
            login_user(murid)
            next_page = request.args.get("next")
            if next_page is None or not next_page.startswith("/"):
                next_page = url_for("murid.murid_dashboard")
            return redirect(next_page)

        flash("Invalid username and password!")
    return render_template("login.html", title="Sign in", form=form)


@auth.route("/login/admin", methods=["GET", "POST"])
def login_admin():
    form = LoginAdminForm()
    if form.validate_on_submit():
        server = AdminModel.query.filter_by(username=form.username.data).first()
        if server is not None and server.verify_password(form.password.data):
            login_user(server)
            next_page = request.args.get("next")
            if next_page is None or not next_page.startswith("/"):
                next_page = url_for("server.data_guru")
            return redirect(next_page)

        flash("Invalid username and password!")
    return render_template("loginAdmin.html", title="Sign in", form=form)


@auth.route("/login/guru", methods=["GET", "POST"])
def login_guru():
    form = LoginGuruForm()
    if form.validate_on_submit():
        guru = GuruModel.query.filter_by(nik=form.nik.data).first()
        if guru is not None and guru.verify_password(form.password.data):
            login_user(guru)
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for("server.data_guru")
            return redirect(next)

        flash("Invalid username and password!")
    return render_template("loginGuru.html", title="Sign in", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("client.index"))
