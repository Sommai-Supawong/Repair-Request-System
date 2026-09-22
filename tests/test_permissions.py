from enums import ProblemType, Urgency
from extensions import db
from models import RepairRequest, User


def test_non_admin_roles_cannot_manage_users(client, login):
    login("teacher")
    assert client.get("/admin/users").status_code == 403
    client.post("/logout")
    login("tech")
    assert client.get("/admin/users").status_code == 403


def test_teacher_cannot_view_another_teachers_repair(app, client, login):
    with app.app_context():
        owner = User.query.filter_by(username="teacher2").one()
        repair = RepairRequest(
            request_no="RP-202609-001", reporter=owner, building="B", room="1",
            problem_type=ProblemType.OTHER, description="Private", urgency=Urgency.LOW,
        )
        db.session.add(repair)
        db.session.commit()
        repair_id = repair.id
    login("teacher")
    assert client.get(f"/repair/{repair_id}").status_code == 403

