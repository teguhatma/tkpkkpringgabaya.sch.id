from app.models import MuridModel
from . import auth
from flask import request, redirect, url_for, render_template, flash
from flask_login import current_user, login_user, login_required, logout_user
from .forms import LoginForm


@auth.route("/login/murid", methods=["GET", "POST"])
def login_murid():
    form = LoginForm()
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


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login_students"))
