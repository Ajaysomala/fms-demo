import os

from locust import HttpUser, between, task


class Customer(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        r = self.client.post(
            "/auth/verify-otp",
            json={"mobile": os.getenv("TEST_MOBILE", "512345678"), "otp": os.getenv("TEST_OTP", "1234")},
        )
        self.headers = {"Authorization": f"Bearer {r.json()['token']}"}

    @task(3)
    def list_providers(self):
        self.client.get("/providers", headers=self.headers)

    @task(1)
    def book_weekly(self):
        self.client.post(
            "/bookings",
            headers=self.headers,
            json={"provider_id": 1, "plan": "weekly", "hours_per_day": 4},
        )
