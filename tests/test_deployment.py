from io import BytesIO

import pytest

from app import create_app
from config import TestConfig
from models import RepairImage, User


PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 32


def test_health_check_is_public_and_minimal(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_production_requires_secret_key():
    class MissingSecretConfig(TestConfig):
        PRODUCTION = True
        SECRET_KEY = None

    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        create_app(MissingSecretConfig)


def test_uploaded_image_route_uses_configured_storage_and_authorization(app, client, login):
    login("teacher")
    response = client.post(
        "/repair/create",
        data={
            "building": "3",
            "room": "301",
            "problem_type": "aircon",
            "urgency": "high",
            "description": "Air conditioner is not cold.",
            "images": (BytesIO(PNG), "before.png", "image/png"),
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 302
    with app.app_context():
        image_id = RepairImage.query.one().id

    image = client.get(f"/repair-image/{image_id}")
    assert image.status_code == 200
    assert image.mimetype == "image/png"

    client.post("/logout")
    login("teacher2")
    assert client.get(f"/repair-image/{image_id}").status_code == 403


def test_database_commands_are_idempotent_and_seed_is_explicit(app):
    runner = app.test_cli_runner()
    assert runner.invoke(args=["init-db"]).exit_code == 0
    assert runner.invoke(args=["init-db"]).exit_code == 0

    with app.app_context():
        before_seed = User.query.count()
    assert runner.invoke(args=["seed-demo"]).exit_code == 0
    with app.app_context():
        after_first_seed = User.query.count()
    assert after_first_seed >= before_seed

    assert runner.invoke(args=["seed-demo"]).exit_code == 0
    with app.app_context():
        assert User.query.count() == after_first_seed


def test_first_admin_can_be_created_with_cli(app):
    runner = app.test_cli_runner()
    result = runner.invoke(
        args=[
            "create-admin",
            "--username", "production-admin",
            "--fullname", "Production Administrator",
            "--email", "production-admin@school.local",
            "--password", "StrongPassword123!",
        ]
    )
    assert result.exit_code == 0
    with app.app_context():
        admin = User.query.filter_by(username="production-admin").one()
        assert admin.role.value == "admin"
        assert admin.check_password("StrongPassword123!")
