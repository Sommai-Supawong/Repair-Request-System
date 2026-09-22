from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from enums import ProblemType, RequestStatus, Urgency, UserRole
from extensions import db
from models import Comment, RepairRequest, User


class RepairService:
    @staticmethod
    def generate_request_no(now: datetime | None = None) -> str:
        now = now or datetime.now()
        prefix = f"RP-{now:%Y%m}-"
        existing = (
            RepairRequest.query.filter(RepairRequest.request_no.like(f"{prefix}%"))
            .with_entities(RepairRequest.request_no)
            .all()
        )
        sequence = max((int(row[0].rsplit("-", 1)[1]) for row in existing), default=0) + 1
        return f"{prefix}{sequence:03d}"

    @staticmethod
    def create(reporter: User, form, files=()) -> RepairRequest:
        if reporter.role not in (UserRole.TEACHER, UserRole.ADMIN):
            raise PermissionError("เฉพาะครู บุคลากร และผู้ดูแลระบบเท่านั้นที่แจ้งซ่อมได้")
        building = form.get("building", "").strip()
        room = form.get("room", "").strip()
        description = form.get("description", "").strip()
        if not all((building, room, description)):
            raise ValueError("กรุณาระบุอาคาร ห้อง และรายละเอียดปัญหา")
        try:
            problem_type = ProblemType(form.get("problem_type"))
            urgency = Urgency(form.get("urgency"))
        except ValueError as exc:
            raise ValueError("ประเภทปัญหาหรือระดับความเร่งด่วนไม่ถูกต้อง") from exc

        repair = None
        for _ in range(3):
            repair = RepairRequest(
                request_no=RepairService.generate_request_no(),
                reporter=reporter,
                building=building,
                room=room,
                problem_type=problem_type,
                description=description,
                urgency=urgency,
            )
            db.session.add(repair)
            try:
                db.session.flush()
                break
            except IntegrityError:
                db.session.rollback()
        else:
            raise ValueError("ไม่สามารถสร้างเลขที่ใบแจ้งซ่อมได้ กรุณาลองอีกครั้ง")
        if files:
            from services.upload_service import UploadService

            UploadService.attach_images(repair, files, "before")
        db.session.commit()
        return repair

    @staticmethod
    def visible_query(user: User):
        query = RepairRequest.query
        if user.role == UserRole.TEACHER:
            query = query.filter_by(user_id=user.id)
        elif user.role == UserRole.TECHNICIAN:
            query = query.filter_by(assigned_to=user.id)
        return query

    @staticmethod
    def can_view(user: User, repair: RepairRequest) -> bool:
        return (
            user.role == UserRole.ADMIN
            or repair.user_id == user.id
            or repair.assigned_to == user.id
        )

    @staticmethod
    def filtered_query(user: User, args):
        query = RepairService.visible_query(user)
        search = args.get("q", "").strip()
        if search:
            like = f"%{search}%"
            query = query.filter(
                or_(
                    RepairRequest.request_no.ilike(like),
                    RepairRequest.building.ilike(like),
                    RepairRequest.room.ilike(like),
                    RepairRequest.description.ilike(like),
                )
            )
        mappings = {
            "status": (RepairRequest.status, RequestStatus),
            "urgency": (RepairRequest.urgency, Urgency),
            "problem_type": (RepairRequest.problem_type, ProblemType),
        }
        for key, (column, enum_cls) in mappings.items():
            value = args.get(key)
            if value:
                try:
                    query = query.filter(column == enum_cls(value))
                except ValueError:
                    pass
        technician = args.get("technician")
        if technician and technician.isdigit():
            query = query.filter(RepairRequest.assigned_to == int(technician))
        date_from = args.get("date_from")
        if date_from:
            try:
                query = query.filter(RepairRequest.created_at >= date.fromisoformat(date_from))
            except ValueError:
                pass
        return query.order_by(RepairRequest.created_at.desc())

    @staticmethod
    def assign(repair: RepairRequest, technician: User, due_date_text: str) -> None:
        try:
            due_date = date.fromisoformat(due_date_text) if due_date_text else None
        except ValueError as exc:
            raise ValueError("รูปแบบกำหนดเสร็จไม่ถูกต้อง") from exc
        repair.assign_to(technician, due_date)
        db.session.commit()

    @staticmethod
    def start(repair: RepairRequest) -> None:
        repair.start_repair()
        db.session.commit()

    @staticmethod
    def complete(repair: RepairRequest, cost_text: str, result: str, files=()) -> None:
        try:
            cost = Decimal(cost_text)
        except InvalidOperation as exc:
            raise ValueError("กรุณาระบุค่าใช้จ่ายเป็นตัวเลขที่ถูกต้อง") from exc
        if not cost.is_finite():
            raise ValueError("กรุณาระบุค่าใช้จ่ายเป็นตัวเลขที่ถูกต้อง")
        repair.complete_repair(cost, result)
        if files:
            from services.upload_service import UploadService

            UploadService.attach_images(repair, files, "after")
        db.session.commit()

    @staticmethod
    def add_comment(repair: RepairRequest, author: User, text: str) -> Comment:
        text = text.strip()
        if not text:
            raise ValueError("กรุณากรอกความคิดเห็น")
        comment = Comment(repair=repair, author=author, comment=text)
        db.session.add(comment)
        db.session.commit()
        return comment
