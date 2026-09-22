from flask import Blueprint, abort, flash, make_response, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from enums import ImageType, ProblemType, RequestStatus, Urgency, UserRole
from extensions import db
from models import RepairRequest, User
from routes.decorators import roles_required
from services import RepairService
from services.export_service import ExportService


repairs_bp = Blueprint("repairs", __name__)


def _get_visible_repair(repair_id: int) -> RepairRequest:
    repair = db.get_or_404(RepairRequest, repair_id)
    if not RepairService.can_view(current_user, repair):
        abort(403)
    return repair


@repairs_bp.route("/repair/create", methods=["GET", "POST"])
@login_required
@roles_required("teacher", "admin")
def create():
    if request.method == "POST":
        try:
            repair = RepairService.create(current_user, request.form, request.files.getlist("images"))
            flash(f"สร้างใบแจ้งซ่อม {repair.request_no} เรียบร้อยแล้ว", "success")
            return redirect(url_for("repairs.detail", repair_id=repair.id))
        except (ValueError, PermissionError) as exc:
            db.session.rollback()
            flash(str(exc), "error")
    return render_template("repairs/create.html", problem_types=ProblemType, urgencies=Urgency)


@repairs_bp.get("/repairs")
@login_required
def list_repairs():
    repairs = RepairService.filtered_query(current_user, request.args).all()
    technicians = User.query.filter_by(role=UserRole.TECHNICIAN, is_active_account=True).order_by(User.fullname).all()
    return render_template(
        "repairs/list.html",
        repairs=repairs,
        technicians=technicians,
        statuses=RequestStatus,
        urgencies=Urgency,
        problem_types=ProblemType,
    )


@repairs_bp.get("/repair/<int:repair_id>")
@login_required
def detail(repair_id):
    repair = _get_visible_repair(repair_id)
    technicians = User.query.filter_by(role=UserRole.TECHNICIAN, is_active_account=True).order_by(User.fullname).all()
    return render_template(
        "repairs/detail.html", repair=repair, technicians=technicians, image_types=ImageType
    )


@repairs_bp.post("/repair/<int:repair_id>/assign")
@login_required
@roles_required("admin")
def assign(repair_id):
    repair = db.get_or_404(RepairRequest, repair_id)
    technician = db.session.get(User, request.form.get("technician_id", type=int))
    if not technician:
        flash("กรุณาเลือกเจ้าหน้าที่ซ่อมที่ถูกต้อง", "error")
    else:
        try:
            RepairService.assign(repair, technician, request.form.get("due_date", ""))
            flash("มอบหมายเจ้าหน้าที่ซ่อมเรียบร้อยแล้ว", "success")
        except ValueError as exc:
            db.session.rollback()
            flash(str(exc), "error")
    return redirect(url_for("repairs.detail", repair_id=repair.id))


@repairs_bp.post("/repair/<int:repair_id>/start")
@login_required
@roles_required("technician")
def start(repair_id):
    repair = _get_visible_repair(repair_id)
    try:
        RepairService.start(repair)
        flash("เริ่มดำเนินการซ่อมแล้ว", "success")
    except ValueError as exc:
        db.session.rollback()
        flash(str(exc), "error")
    return redirect(url_for("repairs.detail", repair_id=repair.id))


@repairs_bp.post("/repair/<int:repair_id>/complete")
@login_required
@roles_required("technician")
def complete(repair_id):
    repair = _get_visible_repair(repair_id)
    try:
        RepairService.complete(
            repair,
            request.form.get("cost", ""),
            request.form.get("result", ""),
            request.files.getlist("images"),
        )
        flash("บันทึกผลและปิดงานซ่อมเรียบร้อยแล้ว", "success")
    except ValueError as exc:
        db.session.rollback()
        flash(str(exc), "error")
    return redirect(url_for("repairs.detail", repair_id=repair.id))


@repairs_bp.post("/repair/<int:repair_id>/comments")
@login_required
def comment(repair_id):
    repair = _get_visible_repair(repair_id)
    try:
        RepairService.add_comment(repair, current_user, request.form.get("comment", ""))
        flash("เพิ่มความคิดเห็นเรียบร้อยแล้ว", "success")
    except ValueError as exc:
        flash(str(exc), "error")
    return redirect(url_for("repairs.detail", repair_id=repair.id))


@repairs_bp.get("/repair/<int:repair_id>/print")
@login_required
def print_detail(repair_id):
    return render_template("repairs/print.html", repair=_get_visible_repair(repair_id))


@repairs_bp.get("/repair/<int:repair_id>/pdf")
@login_required
def pdf(repair_id):
    repair = _get_visible_repair(repair_id)
    try:
        from weasyprint import HTML

        html = render_template("repairs/print.html", repair=repair, pdf_mode=True)
        data = HTML(string=html, base_url=request.url_root).write_pdf()
        response = make_response(data)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = f'attachment; filename="{repair.request_no}.pdf"'
        return response
    except (ImportError, OSError):
        flash("ไม่สามารถสร้างไฟล์ PDF ได้ กรุณาใช้คำสั่งพิมพ์หรือบันทึกเป็น PDF จากเบราว์เซอร์", "warning")
        return redirect(url_for("repairs.print_detail", repair_id=repair.id))


@repairs_bp.get("/repairs/export.csv")
@login_required
@roles_required("admin")
def export_csv():
    content = ExportService.repairs_csv(RepairService.filtered_query(current_user, request.args).all())
    response = make_response(content)
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = 'attachment; filename="repairs.csv"'
    return response
