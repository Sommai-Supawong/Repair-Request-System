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
        },
        follow_redirects=False,
    )
    assert response.status_code == 302
    detail_url = response.headers["Location"]
    repair_id = int(detail_url.rstrip("/").rsplit("/", 1)[1])

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
    response = client.post(
        f"/repair/{repair_id}/complete",
        data={"result": "Cleaned and recharged the unit.", "cost": "1500"},
        follow_redirects=True,
    )
    assert "ซ่อมเสร็จแล้ว".encode() in response.data

    client.post("/logout")
    login("teacher")
    assert b"Cleaned and recharged" in client.get(detail_url).data
    assert client.get(f"/repair/{repair_id}/print").status_code == 200

    client.post("/logout")
    login("admin")
    export = client.get("/repairs/export.csv")
    assert export.status_code == 200
    assert b"Building 3" in export.data
