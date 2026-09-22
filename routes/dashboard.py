from flask import Blueprint, render_template
from flask_login import current_user, login_required

from enums import RequestStatus
from models import RepairRequest
from services import RepairService


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/dashboard")
@login_required
def index():
    query = RepairService.visible_query(current_user)
    stats = {"total": query.count()}
    for status in RequestStatus:
        stats[status.value] = query.filter_by(status=status).count()
    recent = query.order_by(RepairRequest.created_at.desc()).limit(8).all()
    return render_template("dashboard/index.html", stats=stats, recent=recent)
