import os
import socket
import subprocess
import sys
import time
from urllib.parse import urlparse

import httpx
import pytest

from utils.guard import check_base_url
from utils.log import get_logger

log = get_logger(__name__)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def base_url():
    url = os.getenv("BASE_URL", "").strip()
    if url:
        base_url = url.rstrip("/")
        check_base_url(base_url)
        log.debug("api tests base url host=%s", urlparse(base_url).hostname)
        yield base_url
        return
    port = _free_port()
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "demo_server.main:app", "--port", str(port), "--log-level", "warning"],
        cwd=ROOT,
    )
    url = f"http://127.0.0.1:{port}"
    check_base_url(url)
    log.debug("api tests base url host=%s", urlparse(url).hostname)
    for _ in range(50):
        try:
            if httpx.get(f"{url}/health", timeout=1).status_code == 200:
                break
        except httpx.HTTPError:
            time.sleep(0.2)
    yield url
    proc.terminate()


@pytest.fixture(scope="session")
def token(base_url):
    mobile = os.getenv("TEST_MOBILE", "512345678")
    otp = os.getenv("TEST_OTP", "1234")
    r = httpx.post(f"{base_url}/auth/verify-otp", json={"mobile": mobile, "otp": otp})
    assert r.status_code == 200
    return r.json()["token"]


@pytest.fixture()
def auth(token):
    return {"Authorization": f"Bearer {token}"}
