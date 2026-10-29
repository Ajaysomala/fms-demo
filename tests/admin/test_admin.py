import os

import pytest

pytestmark = pytest.mark.admin
ADMIN_URL = os.getenv("ADMIN_URL", "")


@pytest.mark.skipif(not ADMIN_URL, reason="Set ADMIN_URL in .env (staging admin) to run")
def test_admin_login_page_loads(page):
    page.goto(ADMIN_URL)
    assert page.title() != ""
    # Next: fill login, open Vendor Onboarding, assert the registered email is visible
