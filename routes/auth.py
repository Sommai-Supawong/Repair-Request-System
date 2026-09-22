from urllib.parse import urljoin, urlparse

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from models import User


auth_bp = Blueprint("auth", __name__)


def _safe_next(target: str | None) -> bool:
    if not target:
        return False
    host = urlparse(request.host_url)
    destination = urlparse(urljoin(request.host_url, target))
    return destination.scheme in ("http", "https") and host.netloc == destination.netloc


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get("username", "").strip().lower()).first()
        if user and user.is_active and user.check_password(request.form.get("password", "")):
            login_user(user, remember=bool(request.form.get("remember")))
            flash("เข้าสู่ระบบสำเร็จ", "success")
            target = request.args.get("next")
            return redirect(target if _safe_next(target) else url_for("dashboard.index"))
        flash("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง", "error")
    return render_template("login.html")


@auth_bp.post("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    flash("ออกจากระบบเรียบร้อยแล้ว", "success")
    return redirect(url_for("auth.login"))
