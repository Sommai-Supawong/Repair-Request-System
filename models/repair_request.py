from datetime import date, datetime, timezone
from decimal import Decimal

from enums import ProblemType, RequestStatus, Urgency, UserRole
from extensions import db


class RepairRequest(db.Model):
    __tablename__ = "repair_requests"
    __table_args__ = (
        db.CheckConstraint("cost IS NULL OR cost >= 0", name="ck_repairs_cost_nonnegative"),
    )

    id = db.Column(db.Integer, primary_key=True)
    request_no = db.Column(db.String(20), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    building = db.Column(db.String(100), nullable=False)
    room = db.Column(db.String(100), nullable=False)
    problem_type = db.Column(db.Enum(ProblemType, values_callable=lambda e: [x.value for x in e]), nullable=False)
    description = db.Column(db.Text, nullable=False)
    urgency = db.Column(db.Enum(Urgency, values_callable=lambda e: [x.value for x in e]), nullable=False)
    status = db.Column(
        db.Enum(RequestStatus, values_callable=lambda e: [x.value for x in e]),
        nullable=False,
        default=RequestStatus.PENDING,
        index=True,
    )
    assigned_to = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    due_date = db.Column(db.Date)
    completion_date = db.Column(db.Date)
    cost = db.Column(db.Numeric(12, 2))
    result = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True)

    reporter = db.relationship("User", foreign_keys=[user_id], back_populates="reported_repairs")
    technician = db.relationship("User", foreign_keys=[assigned_to], back_populates="assigned_repairs")
    images = db.relationship("RepairImage", back_populates="repair", cascade="all, delete-orphan")
    comments = db.relationship(
        "Comment", back_populates="repair", cascade="all, delete-orphan", order_by="Comment.created_at"
    )

    def assign_to(self, technician, due_date: date | None = None) -> None:
        if technician.role != UserRole.TECHNICIAN:
            raise ValueError("ผู้รับผิดชอบต้องเป็นเจ้าหน้าที่ซ่อม")
        if self.status not in (RequestStatus.PENDING, RequestStatus.ACCEPTED):
            raise ValueError("มอบหมายงานได้เฉพาะใบแจ้งซ่อมที่รอรับเรื่องหรือรับเรื่องแล้วเท่านั้น")
        self.assigned_to = technician.id
        self.technician = technician
        self.due_date = due_date
        self.status = RequestStatus.ACCEPTED

    def start_repair(self) -> None:
        if self.status != RequestStatus.ACCEPTED:
            raise ValueError("ต้องรับเรื่องก่อนเริ่มดำเนินการซ่อม")
        self.status = RequestStatus.IN_PROGRESS

    def complete_repair(self, cost: Decimal, result: str) -> None:
        if self.status != RequestStatus.IN_PROGRESS:
            raise ValueError("ต้องเริ่มดำเนินการซ่อมก่อนปิดงาน")
        if cost < 0:
            raise ValueError("ค่าใช้จ่ายต้องไม่ติดลบ")
        if not result.strip():
            raise ValueError("กรุณาระบุผลการซ่อม")
        self.cost = cost
        self.result = result.strip()
        self.completion_date = date.today()
        self.status = RequestStatus.COMPLETED
