import os
import socket
import subprocess
import sys
import time

import httpx
import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def base_url():
    url = os.getenv("BASE_URL", "").strip()
    if url:
        yield url.rstrip("/")
        return
    port = _free_port()
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "demo_server.main:app", "--port", str(port), "--log-level", "warning"],
        cwd=ROOT,
    )
    url = f"http://127.0.0.1:{port}"
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
