from io import BytesIO


PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 32


def test_complete_demo_flow_and_exports(app, client, login):
    login("teacher")
    response = client.post(
        "/repair/create",
        data={
            "building": "Building 3",
            "room": "301",
            "problem_type": "aircon",
            "urgency": "high",
            "description": "Air conditioner is not cold and makes a loud noise.",
            "images": (BytesIO(PNG), "before.png", "image/png"),
        },
        content_type="multipart/form-data",
        follow_redirects=False,
    )
    assert response.status_code == 302
    detail_url = response.headers["Location"]
    repair_id = int(detail_url.rstrip("/").rsplit("/", 1)[1])
    assert client.post(
        f"/repair/{repair_id}/comments", data={"comment": "Please check before class."}
    ).status_code == 302

    client.post("/logout")
    login("admin")
    from models import User
    with app.app_context():
        tech_id = User.query.filter_by(username="tech").one().id
    response = client.post(
        f"/repair/{repair_id}/assign",
        data={"technician_id": tech_id, "due_date": "2026-09-25"},
        follow_redirects=True,
    )
    assert "รับเรื่องแล้ว".encode() in response.data

    client.post("/logout")
    login("tech")
    assert b"Building 3" in client.get("/repairs").data
    assert "กำลังดำเนินการ".encode() in client.post(f"/repair/{repair_id}/start", follow_redirects=True).data
    assert client.post(
        f"/repair/{repair_id}/comments", data={"comment": "Inspection completed."}
    ).status_code == 302
    response = client.post(
        f"/repair/{repair_id}/complete",
        data={
            "result": "Cleaned and recharged the unit.",
            "cost": "1500",
            "images": (BytesIO(PNG), "after.png", "image/png"),
        },
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert "ซ่อมเสร็จแล้ว".encode() in response.data

    client.post("/logout")
    login("teacher")
    assert b"Cleaned and recharged" in client.get(detail_url).data
    assert client.get(f"/repair/{repair_id}/print").status_code == 200
    pdf = client.get(f"/repair/{repair_id}/pdf")
    assert pdf.status_code in (200, 302)
    assert pdf.mimetype == "application/pdf" or "/print" in pdf.headers.get("Location", "")
    with app.app_context():
        from extensions import db
        from models import RepairRequest

        image_ids = [image.id for image in db.session.get(RepairRequest, repair_id).images]
    assert len(image_ids) == 2
    assert all(client.get(f"/repair-image/{image_id}").status_code == 200 for image_id in image_ids)

    client.post("/logout")
    login("admin")
    export = client.get("/repairs/export.csv")
    assert export.status_code == 200
    assert b"Building 3" in export.data
    assert client.get("/admin/users").status_code == 200
    created_user = client.post(
        "/admin/users",
        data={
            "username": "staff-new",
            "password": "Password123!",
            "fullname": "New Staff",
            "email": "staff-new@test.local",
            "role": "teacher",
        },
        follow_redirects=True,
    )
    assert created_user.status_code == 200
    assert b"staff-new" in created_user.data
