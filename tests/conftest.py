import pytest

from app import create_app
from config import TestConfig
from enums import UserRole
from extensions import db
from models import User


@pytest.fixture()
def app(tmp_path):
    class LocalTestConfig(TestConfig):
        UPLOAD_FOLDER = str(tmp_path / "uploads")

    app = create_app(LocalTestConfig)
    with app.app_context():
        db.create_all()
        for username, role in [
            ("admin", UserRole.ADMIN),
            ("teacher", UserRole.TEACHER),
            ("teacher2", UserRole.TEACHER),
            ("tech", UserRole.TECHNICIAN),
        ]:
            user = User(username=username, fullname=username.title(), email=f"{username}@test.local", role=role)
            user.set_password("Password123!")
            db.session.add(user)
        db.session.commit()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def login(client):
    def do_login(username="teacher", password="Password123!"):
        return client.post("/login", data={"username": username, "password": password}, follow_redirects=True)
    return do_login

