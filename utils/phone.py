import os
import random
import re
import threading
from pathlib import Path

from utils.log import get_logger

log = get_logger(__name__)

PHONE_RE = re.compile(r"^5\d{8}$")
USED_FILE = Path(os.getenv("USED_MOBILES_FILE", "data/used_mobiles.txt"))
_lock = threading.Lock()


def _load_used():
    if not USED_FILE.exists():
        return set()
    return {line.strip() for line in USED_FILE.read_text(encoding="utf-8").splitlines() if line.strip()}


def random_uae_mobile():
    return "5" + "".join(random.choices("0123456789", k=8))


def is_valid_uae_mobile(number):
    return bool(PHONE_RE.fullmatch(number))


def unique_mobiles(count):
    """Return `count` fresh numbers never handed out before and record them in USED_FILE."""
    log.debug("generating unique mobiles count=%s", count)
    with _lock:
        used = _load_used()
        log.debug("loaded %d previously used numbers from %s", len(used), USED_FILE)
        fresh = []
        while len(fresh) < count:
            number = random_uae_mobile()
            if number in used:
                log.debug("skipped already used number")
                continue
            used.add(number)
            fresh.append(number)
        USED_FILE.parent.mkdir(parents=True, exist_ok=True)
        with USED_FILE.open("a", encoding="utf-8") as f:
            f.write("\n".join(fresh) + "\n")
        log.info("reserved %d new mobile numbers", len(fresh))
        return fresh


def new_mobile():
    return unique_mobiles(1)[0]


EXISTING_FILE = Path(os.getenv("EXISTING_MOBILES_FILE", "data/existing_mobiles.txt"))


def load_existing_mobiles():
    """Read already-created test accounts, one number per line. Blank lines and # comments are ignored."""
    log.debug("existing mobiles file exists=%s", EXISTING_FILE.exists())
    if not EXISTING_FILE.exists():
        log.warning("no existing-accounts file at %s", EXISTING_FILE)
        return []
    numbers = []
    for line in EXISTING_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if not is_valid_uae_mobile(line):
            log.warning("ignored invalid existing number with length %d", len(line))
            continue
        if line in numbers:
            log.debug("ignored duplicate existing number")
            continue
        numbers.append(line)
    log.debug("loaded %d existing numbers from %s", len(numbers), EXISTING_FILE)
    return numbers


def mobile_pool(total, existing_count=0):
    """Return a list of (mobile, kind) with kind 'existing' or 'new'. Existing accounts are never repeated inside one pool."""
    log.debug("creating mobile pool total=%s existing_count=%s", total, existing_count)
    existing = load_existing_mobiles()
    take = min(existing_count, len(existing), total)
    if take < existing_count:
        log.warning("asked for %d existing accounts but only %d usable", existing_count, take)
    pool = [(n, "existing") for n in existing[:take]]
    fresh = unique_mobiles(total - take) if total > take else []
    pool += [(n, "new") for n in fresh]
    log.info("mobile pool ready: %d existing + %d new", take, len(fresh))
    return pool
