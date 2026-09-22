from datetime import date, datetime

from localization import problem_type_label, role_label, status_label, thai_date, urgency_label


def test_thai_label_helpers_keep_internal_values_separate():
    assert status_label("pending") == "รอรับเรื่อง"
    assert status_label("in_progress") == "กำลังดำเนินการ"
    assert urgency_label("high") == "สูง"
    assert problem_type_label("aircon") == "เครื่องปรับอากาศ"
    assert role_label("technician") == "เจ้าหน้าที่ซ่อม"


def test_thai_date_format():
    assert thai_date(date(2026, 9, 22)) == "22/09/2026"
    assert thai_date(datetime(2026, 9, 22, 10, 21), True) == "22/09/2026 10:21"


def test_pages_default_to_thai(client):
    response = client.get("/login")
    assert b'<html lang="th">' in response.data
    assert "ระบบแจ้งซ่อมภายในโรงเรียน".encode() in response.data


def test_admin_and_error_pages_are_thai(client, login):
    login("admin")
    assert "จัดการผู้ใช้งาน".encode() in client.get("/admin/users").data
    assert "ไม่พบหน้าที่ต้องการ".encode() in client.get("/missing-page").data
