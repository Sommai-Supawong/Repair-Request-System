from enums import UserRole
from extensions import db
from models import User


class UserService:
    @staticmethod
    def create(username: str, password: str, fullname: str, email: str, role: str) -> User:
        username = username.strip().lower()
        if not all((username, password, fullname.strip(), email.strip())):
            raise ValueError("กรุณากรอกข้อมูลผู้ใช้งานให้ครบถ้วน")
        if len(password) < 8:
            raise ValueError("รหัสผ่านต้องมีอย่างน้อย 8 ตัวอักษร")
        if User.query.filter_by(username=username).first():
            raise ValueError("ชื่อผู้ใช้นี้มีอยู่ในระบบแล้ว")
        try:
            user_role = UserRole(role)
        except ValueError as exc:
            raise ValueError("สิทธิ์ผู้ใช้งานไม่ถูกต้อง") from exc
        user = User(
            username=username,
            fullname=fullname.strip(),
            email=email.strip().lower(),
            role=user_role,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def seed_demo_users() -> None:
        demo = [
            ("admin", "Admin123!", "System Administrator", "admin@school.local", "admin"),
            ("teacher01", "Teacher123!", "Demo Teacher", "teacher01@school.local", "teacher"),
            ("tech01", "Tech123!", "Demo Technician", "tech01@school.local", "technician"),
        ]
        for username, password, fullname, email, role in demo:
            if not User.query.filter_by(username=username).first():
                UserService.create(username, password, fullname, email, role)
