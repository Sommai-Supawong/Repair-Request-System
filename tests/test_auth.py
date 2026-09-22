def test_successful_login_and_logout(client, login):
    response = login("admin")
    assert response.status_code == 200
    assert "ภาพรวมระบบ".encode() in response.data
    response = client.post("/logout", follow_redirects=True)
    assert "เข้าสู่ระบบ".encode() in response.data


def test_failed_login(client, login):
    response = login("admin", "wrong")
    assert "เข้าสู่ระบบ".encode() in response.data


def test_protected_route_redirects(client):
    response = client.get("/dashboard")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]
