import os

import pytest

from utils.guard import check_base_url

pytestmark = pytest.mark.admin
ADMIN_URL = os.getenv("ADMIN_URL", "")


@pytest.mark.skipif(not ADMIN_URL, reason="Set ADMIN_URL in .env (staging admin) to run")
def test_admin_login_page_loads(page):
    check_base_url(ADMIN_URL)
    page.goto(ADMIN_URL)
    assert page.title() != ""
    # Next: fill login, open Vendor Onboarding, assert the registered email is visible
