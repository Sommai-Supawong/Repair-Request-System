from decimal import Decimal

import pytest

from enums import ProblemType, RequestStatus, Urgency
from extensions import db
from models import RepairRequest, User


@pytest.fixture()
def repair_and_tech(app):
    with app.app_context():
        teacher = User.query.filter_by(username="teacher").one()
        tech = User.query.filter_by(username="tech").one()
        repair = RepairRequest(
            request_no="RP-202609-001", reporter=teacher, building="3", room="301",
            problem_type=ProblemType.AIRCON, description="No cooling", urgency=Urgency.HIGH,
        )
        db.session.add(repair)
        db.session.commit()
        yield repair, tech


def test_valid_workflow(app, repair_and_tech):
    with app.app_context():
        repair, tech = repair_and_tech
        repair.assign_to(tech)
        assert repair.status == RequestStatus.ACCEPTED
        repair.start_repair()
        assert repair.status == RequestStatus.IN_PROGRESS
        repair.complete_repair(Decimal("1500"), "Cleaned and recharged")
        assert repair.status == RequestStatus.COMPLETED
        assert repair.completion_date is not None


def test_pending_cannot_complete(app, repair_and_tech):
    with app.app_context():
        repair, _ = repair_and_tech
        with pytest.raises(ValueError):
            repair.complete_repair(Decimal("1"), "Invalid")


def test_only_assigned_technician_can_start(app, client, login, repair_and_tech):
    with app.app_context():
        repair, tech = repair_and_tech
        repair.assign_to(tech)
        db.session.commit()
        repair_id = repair.id
    login("teacher")
    assert client.post(f"/repair/{repair_id}/start").status_code == 403

