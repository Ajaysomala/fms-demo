import httpx
import pytest

DAYS = {"weekly": 7, "monthly": 30}
FEE = 10


@pytest.mark.parametrize("plan", ["weekly", "monthly"])
@pytest.mark.parametrize("provider_id", [1, 2])
def test_total_matches_rate_hours_days_plus_fee(base_url, auth, plan, provider_id):
    providers = httpx.get(f"{base_url}/providers", headers=auth).json()
    rate = next(p["hourly_rate"] for p in providers if p["id"] == provider_id)
    hours = 4
    r = httpx.post(
        f"{base_url}/bookings",
        headers=auth,
        json={"provider_id": provider_id, "plan": plan, "hours_per_day": hours},
    )
    assert r.status_code == 200
    body = r.json()
    expected = rate * hours * DAYS[plan] + FEE
    assert body["total"] == expected, f"{plan}: expected {expected}, got {body['total']}"


def test_unknown_plan_is_rejected(base_url, auth):
    r = httpx.post(f"{base_url}/bookings", headers=auth, json={"provider_id": 1, "plan": "yearly", "hours_per_day": 4})
    assert r.status_code == 400
