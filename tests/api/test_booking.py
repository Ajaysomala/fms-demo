import httpx
import pytest

DAYS = {"weekly": 7, "monthly": 30}
FEE = 10


@pytest.mark.parametrize("plan", ["weekly", "monthly"])
@pytest.mark.parametrize("provider_id", [1, 2])
def test_total_matches_rate_hours_days_plus_fee(base_url, auth, plan, provider_id, steps):
    """Booking total must equal hourly rate x 4 hours x plan days + 10 service fee."""
    steps("Logged in with OTP 1234 and got a token")
    providers = httpx.get(f"{base_url}/providers", headers=auth).json()
    rate = next(p["hourly_rate"] for p in providers if p["id"] == provider_id)
    steps(f"Fetched providers: provider {provider_id} hourly rate = {rate}")
    hours = 4
    r = httpx.post(
        f"{base_url}/bookings",
        headers=auth,
        json={"provider_id": provider_id, "plan": plan, "hours_per_day": hours},
    )
    steps(f"Booked provider {provider_id}, plan={plan}, {hours} hours/day. Status: {r.status_code}")
    assert r.status_code == 200
    body = r.json()
    expected = rate * hours * DAYS[plan] + FEE
    steps(f"Expected total = {rate} x {hours} x {DAYS[plan]} + {FEE} = {expected}")
    steps(f"Actual total from API = {body['total']}")
    assert body["total"] == expected, f"{plan}: expected {expected}, got {body['total']}"


def test_unknown_plan_is_rejected(base_url, auth, steps):
    """A plan that doesn't exist (yearly) must be rejected with HTTP 400."""
    r = httpx.post(f"{base_url}/bookings", headers=auth, json={"provider_id": 1, "plan": "yearly", "hours_per_day": 4})
    steps(f"Booked with invalid plan 'yearly'. Status: {r.status_code} (expected 400)")
    assert r.status_code == 400