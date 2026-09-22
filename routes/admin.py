from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from enums import UserRole
from extensions import db
from models import User
from routes.decorators import roles_required
from services import UserService


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/users", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def users():
    if request.method == "POST":
        try:
            UserService.create(
                request.form.get("username", ""),
                request.form.get("password", ""),
                request.form.get("fullname", ""),
                request.form.get("email", ""),
                request.form.get("role", ""),
            )
            flash("สร้างผู้ใช้งานเรียบร้อยแล้ว", "success")
            return redirect(url_for("admin.users"))
        except ValueError as exc:
            db.session.rollback()
            flash(str(exc), "error")
    return render_template("admin/users.html", users=User.query.order_by(User.created_at.desc()).all(), roles=UserRole)


@admin_bp.post("/users/<int:user_id>/edit")
@login_required
@roles_required("admin")
def edit_user(user_id):
    user = db.get_or_404(User, user_id)
    try:
        try:
            new_role = UserRole(request.form.get("role"))
        except ValueError as exc:
            raise ValueError("สิทธิ์ผู้ใช้งานไม่ถูกต้อง") from exc
        active = request.form.get("is_active") == "on"
        if user.id == current_user.id and (new_role != UserRole.ADMIN or not active):
            raise ValueError("ไม่สามารถยกเลิกสิทธิ์ผู้ดูแลระบบของบัญชีตนเองได้")
        user.fullname = request.form.get("fullname", "").strip()
        user.email = request.form.get("email", "").strip().lower()
        if not user.fullname or not user.email:
            raise ValueError("กรุณากรอกชื่อ-นามสกุลและอีเมล")
        user.role = new_role
        user.is_active_account = active
        password = request.form.get("password", "")
        if password:
            if len(password) < 8:
                raise ValueError("รหัสผ่านต้องมีอย่างน้อย 8 ตัวอักษร")
            user.set_password(password)
        db.session.commit()
        flash("บันทึกข้อมูลผู้ใช้งานเรียบร้อยแล้ว", "success")
    except ValueError as exc:
        db.session.rollback()
        flash(str(exc), "error")
    return redirect(url_for("admin.users"))
