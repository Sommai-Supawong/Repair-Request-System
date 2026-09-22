from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from enums import UserRole
from extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    __table_args__ = (
        db.CheckConstraint(
            "role IN ('admin', 'teacher', 'technician')", name="ck_users_role"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    fullname = db.Column(db.String(150), nullable=False)
    role = db.Column(db.Enum(UserRole, values_callable=lambda e: [x.value for x in e]), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    is_active_account = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    reported_repairs = db.relationship(
        "RepairRequest", foreign_keys="RepairRequest.user_id", back_populates="reporter"
    )
    assigned_repairs = db.relationship(
        "RepairRequest", foreign_keys="RepairRequest.assigned_to", back_populates="technician"
    )
    comments = db.relationship("Comment", back_populates="author")

    @property
    def is_active(self):
        return self.is_active_account

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def has_role(self, *roles: str) -> bool:
        return self.role.value in roles

