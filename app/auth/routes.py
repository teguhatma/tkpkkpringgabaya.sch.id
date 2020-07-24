from app.models import UserModel
from . import auth
from flask import request, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                if user.guru:
                    next = url_for("server.dashboard")
                else:
                    next = url_for("murid.murid_dashboard")
            return redirect(next)
        elif user is None:
            flash("Maaf, Anda belum terdaftar.")
        else:
            flash("Email dan password anda salah.")
    return render_template("login.html", title="Sign in", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("client.index"))
