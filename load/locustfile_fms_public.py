import os
from collections import deque
from urllib.parse import urlparse

from locust import HttpUser, events, task

from utils.guard import GuardError, check_base_url, check_request, check_users, get_rps_cap, mask
from utils.log import get_logger

log = get_logger(__name__)

RPS_CAP = get_rps_cap()
KILL_WINDOW = 20
KILL_RATIO = 0.5
COUNTRY = "AE"
HEADERS = {"x-country-iso-code-2": COUNTRY, "x-client-platform": "android"}
_kill_results = deque(maxlen=KILL_WINDOW)
_runner = None


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    global _runner
    _runner = environment.runner
    try:
        check_base_url(environment.host)
        users = environment.parsed_options.num_users
        if users is None:
            log.error("run headless with -u <users>; web UI mode is not allowed")
            environment.runner.quit()
            return
        check_users(users)
        log.info(
            "test start host=%s users=%s rps_cap=%s",
            urlparse(environment.host).hostname,
            users,
            RPS_CAP,
        )
    except GuardError as exc:
        log.error("%s", exc)
        environment.runner.quit()


@events.request.add_listener
def on_request(request_type, name, response, exception=None, **kwargs):
    status_code = getattr(response, "status_code", None)
    path = urlparse(getattr(response, "url", name)).path
    log.info("%s %s %s", request_type, mask(path), status_code)
    bad = (
        exception is not None
        or status_code is None
        or status_code == 403
        or status_code == 429
        or status_code >= 500
    )
    _kill_results.append(bad)
    if len(_kill_results) == KILL_WINDOW and sum(_kill_results) / len(_kill_results) >= KILL_RATIO:
        log.error("kill switch tripped")
        if _runner is not None:
            _runner.quit()


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    log.info(
        "test stop requests=%d failures=%d",
        environment.stats.total.num_requests,
        environment.stats.total.num_failures,
    )


class FmsPublicUser(HttpUser):
    def wait_time(self):
        seconds = max(self.environment.runner.user_count, 1) / RPS_CAP
        return seconds

    def get(self, path, name):
        check_request("GET", path)
        log.debug("get path=%s name=%s", urlparse(path).path, name)
        with self.client.get(path, headers=HEADERS, name=name, catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"status {response.status_code}")

    @task
    def service_categories(self):
        self.get("/common/service-categories", "service-categories")

    @task
    def region(self):
        self.get("/common/region", "region")

    @task
    def country_config(self):
        self.get("/common/country-config", "country-config")

    @task
    def enums(self):
        self.get("/common/enums", "enums")

    @task
    def vehicle_makes(self):
        self.get("/common/vehicle-makes", "vehicle-makes")

    @task
    def customer_home(self):
        self.get("/customer/home", "customer-home")
