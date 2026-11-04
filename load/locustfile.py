import os

from locust import HttpUser, between, events, task

from utils.guard import GuardError, check_base_url, check_request, check_users


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    try:
        check_base_url(environment.host)
        check_users(environment.parsed_options.num_users)
    except GuardError:
        environment.runner.quit()


class Customer(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        check_request("POST", "/auth/verify-otp")
        r = self.client.post(
            "/auth/verify-otp",
            json={"mobile": os.getenv("TEST_MOBILE", "512345678"), "otp": os.getenv("TEST_OTP", "1234")},
        )
        self.headers = {"Authorization": f"Bearer {r.json()['token']}"}

    @task(3)
    def list_providers(self):
        check_request("GET", "/providers")
        self.client.get("/providers", headers=self.headers)

    @task(1)
    def book_weekly(self):
        check_request("POST", "/bookings")
        self.client.post(
            "/bookings",
            headers=self.headers,
            json={"provider_id": 1, "plan": "weekly", "hours_per_day": 4},
        )
