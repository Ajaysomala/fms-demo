import httpx


def test_login_with_fixed_otp(base_url):
    r = httpx.post(f"{base_url}/auth/verify-otp", json={"mobile": "512345678", "otp": "1234"})
    assert r.status_code == 200
    assert "token" in r.json()


def test_wrong_otp_is_rejected(base_url):
    r = httpx.post(f"{base_url}/auth/verify-otp", json={"mobile": "512345678", "otp": "0000"})
    assert r.status_code == 401


def test_mobile_must_start_with_5_and_have_9_digits(base_url):
    r = httpx.post(f"{base_url}/auth/verify-otp", json={"mobile": "12345", "otp": "1234"})
    assert r.status_code == 422


def test_providers_need_a_token(base_url):
    assert httpx.get(f"{base_url}/providers").status_code == 401
