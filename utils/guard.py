import os
import re
import math
from urllib.parse import urlparse

from utils.log import get_logger

log = get_logger(__name__)

ALLOWED_HOSTS = {"api-uat.findmyservices.ae", "localhost", "127.0.0.1"}
LOCAL_HOSTS = {"localhost", "127.0.0.1"}
SAFE_METHODS = {"GET", "HEAD"}
DENY_PATTERNS = [
    r"/payments/webhooks",
    r"/checkout",
    r"/common/places",
    r"/customer/ai",
    r"/customer/devices/test-push",
    r"/customer/account/delete",
    r"/auth/otp/send",
]
HARD_MAX_USERS = 200
HARD_MAX_RPS = 5.0


class GuardError(Exception):
    pass


def check_base_url(url):
    parsed = urlparse(url)
    host = parsed.hostname or ""
    log.debug("checking base url host=%s scheme=%s", host, parsed.scheme)
    if host not in ALLOWED_HOSTS:
        log.error("blocked base url host: %s", host)
        raise GuardError("host not allowed: " + host)
    if host not in LOCAL_HOSTS and parsed.scheme != "https":
        raise GuardError("https required for " + host)
    log.debug("base url allowed: %s", host)


def check_request(method, path):
    path = urlparse(path).path
    log.debug("checking request method=%s path=%s", method, mask(path))
    for pattern in DENY_PATTERNS:
        if re.search(pattern, path):
            log.error("blocked route: %s %s", method, path)
            raise GuardError("route blocked: " + path)
    if method.upper() not in SAFE_METHODS and os.getenv("ALLOW_WRITES") != "1":
        log.error("blocked write method: %s %s", method, path)
        raise GuardError("write method blocked: " + method)


def check_users(count):
    log.debug("checking users count=%s", count)
    try:
        configured_limit = int(os.getenv("MAX_USERS", "100"))
    except ValueError as exc:
        raise GuardError("invalid MAX_USERS") from exc
    limit = min(configured_limit, HARD_MAX_USERS)
    if count <= 0 or count > limit:
        log.error("user count %d is above MAX_USERS %d", count, limit)
        raise GuardError("too many users: %d > %d" % (count, limit))


def get_rps_cap(default=1.5):
    try:
        cap = float(os.getenv("RPS_CAP", str(default)))
    except ValueError as exc:
        raise GuardError("invalid RPS_CAP") from exc
    if not math.isfinite(cap) or cap <= 0 or cap > HARD_MAX_RPS:
        raise GuardError("invalid RPS_CAP")
    log.debug("rps cap value=%s", cap)
    return cap


def mask(text):
    text = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "***@***", text)
    text = re.sub(r"(?<!\d)(?:\+?971)5\d{8}(?!\d)", "***", text)
    text = re.sub(r"(?i)\botp\s*[:=]\s*\d{4,8}\b", "otp ***", text)
    text = re.sub(r"(?i)bearer\s+\S+", "Bearer ***", text)
    text = re.sub(r"\b5\d{8}\b", lambda m: m.group()[:3] + "******", text)
    return text
