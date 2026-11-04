import pytest

from utils.guard import GuardError, check_base_url, check_request, check_users, get_rps_cap, mask


def test_check_base_url_allows_staging_and_local():
    check_base_url("https://api-uat.findmyservices.ae")
    check_base_url("http://localhost:8000")


@pytest.mark.parametrize("url", ["https://example.com", "http://api-uat.findmyservices.ae"])
def test_check_base_url_rejects_disallowed_urls(url):
    with pytest.raises(GuardError):
        check_base_url(url)


def test_check_request_allows_get():
    check_request("GET", "/common/banners")


@pytest.mark.parametrize(
    ("method", "path"),
    [
        ("POST", "/common/banners"),
        ("GET", "/common/places/autocomplete"),
        ("POST", "/payments/webhooks/stripe"),
        ("GET", "/customer/ai/search/chat"),
    ],
)
def test_check_request_rejects_blocked_requests(monkeypatch, method, path):
    monkeypatch.delenv("ALLOW_WRITES", raising=False)
    with pytest.raises(GuardError):
        check_request(method, path)


def test_check_users_default_limit(monkeypatch):
    monkeypatch.delenv("MAX_USERS", raising=False)
    check_users(100)
    with pytest.raises(GuardError):
        check_users(101)


def test_check_users_hard_limit(monkeypatch):
    monkeypatch.setenv("MAX_USERS", "500")
    with pytest.raises(GuardError):
        check_users(201)


@pytest.mark.parametrize("value", ["0", "-1", "nan", "6"])
def test_get_rps_cap_rejects_unsafe_values(monkeypatch, value):
    monkeypatch.setenv("RPS_CAP", value)
    with pytest.raises(GuardError):
        get_rps_cap()


def test_get_rps_cap_default(monkeypatch):
    monkeypatch.delenv("RPS_CAP", raising=False)
    assert get_rps_cap() == 1.5


def test_mask_hides_bearer_token_and_mobile():
    masked = mask("Bearer abc123 call 555111555")
    assert "abc123" not in masked
    assert "555111555" not in masked


def test_mask_hides_email_otp_and_international_mobile():
    masked = mask("email user@example.com otp: 1234 +971555111555")
    assert "user@example.com" not in masked
    assert "otp: 1234" not in masked
    assert "+971555111555" not in masked
