from datetime import datetime
from io import BytesIO

from extensions import db
from models import RepairRequest


PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 32


def valid_repair_data():
    return {
        "building": "Building 3",
        "room": "301",
        "problem_type": "aircon",
        "urgency": "high",
        "description": "Air conditioner is not cold and makes a loud noise.",
    }


def test_create_repair_and_request_number(app, client, login):
    login()
    response = client.post("/repair/create", data=valid_repair_data(), follow_redirects=True)
    assert response.status_code == 200
    expected_prefix = datetime.now().strftime("RP-%Y%m-")
    assert expected_prefix.encode() in response.data
    with app.app_context():
        assert RepairRequest.query.one().request_no == expected_prefix + "001"


def test_create_requires_fields_and_valid_enum(app, client, login):
    login()
    data = valid_repair_data()
    data["building"] = ""
    response = client.post("/repair/create", data=data, follow_redirects=True)
    assert "แจ้งซ่อมใหม่".encode() in response.data
    data = valid_repair_data()
    data["problem_type"] = "spaceship"
    response = client.post("/repair/create", data=data, follow_redirects=True)
    assert "แจ้งซ่อมใหม่".encode() in response.data
    with app.app_context():
        assert RepairRequest.query.count() == 0


def test_allowed_and_invalid_upload(app, client, login):
    login()
    data = valid_repair_data()
    data["images"] = (BytesIO(PNG), "before.png", "image/png")
    response = client.post("/repair/create", data=data, content_type="multipart/form-data", follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert len(RepairRequest.query.one().images) == 1

    data = valid_repair_data()
    data["images"] = (BytesIO(b"not an executable"), "bad.exe", "application/octet-stream")
    response = client.post("/repair/create", data=data, content_type="multipart/form-data", follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert RepairRequest.query.count() == 1


def test_oversized_upload(client, login):
    login()
    data = valid_repair_data()
    data["images"] = (BytesIO(b"x" * (5 * 1024 * 1024 + 1)), "large.png", "image/png")
    assert client.post("/repair/create", data=data, content_type="multipart/form-data").status_code == 413
