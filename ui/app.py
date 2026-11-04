import csv
import os
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, HTMLResponse

from utils.guard import (
    ALLOWED_HOSTS,
    DENY_PATTERNS,
    HARD_MAX_RPS,
    HARD_MAX_USERS,
    SAFE_METHODS,
    GuardError,
    get_rps_cap,
    mask,
)

app = FastAPI(title="FMS Automation Viewer")

SUMMARY_COLUMNS = {
    "Name",
    "Request Count",
    "Failure Count",
    "Median Response Time",
    "Average Response Time",
    "95%",
    "99%",
    "Requests/s",
    "Failures/s",
}


def _reports_dir():
    return Path(os.getenv("REPORTS_DIR", "reports"))


def _log_file():
    return Path(os.getenv("LOG_FILE", "logs/automation.log"))


def _number(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return value
    return int(number) if number.is_integer() else number


@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    if request.url.path == "/" or request.url.path.startswith("/api/"):
        response.headers["Content-Security-Policy"] = (
            "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; "
            "connect-src 'self'; img-src data:"
        )
    return response


@app.get("/api/summary")
def summary():
    path = _reports_dir() / f"{os.getenv('STATS_PREFIX', 'load_public')}_stats.csv"
    if not path.is_file():
        return {"has_data": False}
    try:
        with path.open(newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            if not reader.fieldnames or not SUMMARY_COLUMNS.issubset(reader.fieldnames):
                return {"has_data": False}
            rows = list(reader)
    except (OSError, csv.Error, UnicodeError):
        return {"has_data": False}
    total = next((row for row in rows if row.get("Name") == "Aggregated"), None)
    if total is None:
        return {"has_data": False}
    total_values = {key: _number(total[key]) for key in SUMMARY_COLUMNS if key != "Name"}
    routes = []
    for row in rows:
        if row.get("Name") == "Aggregated":
            continue
        routes.append(
            {
                "name": row["Name"],
                "requests": _number(row["Request Count"]),
                "failures": _number(row["Failure Count"]),
                "median": _number(row["Median Response Time"]),
                "p95": _number(row["95%"]),
                "rps": _number(row["Requests/s"]),
            }
        )
    return {"has_data": True, "total": total_values, "routes": routes}


@app.get("/api/log")
def log_tail(lines: int = Query(default=50)):
    count = max(1, min(lines, 200))
    path = _log_file()
    if not path.is_file():
        return []
    try:
        content = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return []
    return [mask(line) for line in content[-count:]]


@app.get("/api/guard")
def guard_status():
    raw_users = os.getenv("MAX_USERS", "100")
    try:
        effective_users = min(int(raw_users), HARD_MAX_USERS)
    except ValueError:
        effective_users = "invalid"
    try:
        rps_cap = get_rps_cap()
    except GuardError:
        rps_cap = "invalid"
    return {
        "allowed_hosts": sorted(ALLOWED_HOSTS),
        "deny_patterns": DENY_PATTERNS,
        "safe_methods": sorted(SAFE_METHODS),
        "hard_max_users": HARD_MAX_USERS,
        "hard_max_rps": HARD_MAX_RPS,
        "max_users": effective_users,
        "allow_writes": os.getenv("ALLOW_WRITES") == "1",
        "rps_cap": rps_cap,
    }


@app.get("/api/reports")
def reports():
    directory = _reports_dir()
    if not directory.is_dir():
        return []
    return sorted(
        file.name
        for file in directory.iterdir()
        if file.is_file() and file.suffix.lower() in {".html", ".csv"}
    )


@app.get("/reports/{name}")
def report(name: str):
    if (
        not name
        or any(separator in name for separator in ("/", "\\"))
        or name == ".."
        or not name.lower().endswith((".html", ".csv"))
    ):
        return HTMLResponse(status_code=404, content="Not found")
    directory = _reports_dir().resolve()
    path = (directory / name).resolve()
    if directory not in path.parents or not path.is_file():
        return HTMLResponse(status_code=404, content="Not found")
    response = FileResponse(path)
    if path.suffix.lower() == ".html":
        response.headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline' data: blob:"
    return response


PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FMS Automation Viewer</title>
<style>
:root { color-scheme: light; --bg:#f4f7fb; --card:#fff; --text:#172033; --muted:#667085; --line:#dbe2ea; --accent:#2563eb; --good:#15803d; --bad:#b42318; }
@media (prefers-color-scheme: dark) { :root { color-scheme: dark; --bg:#101827; --card:#182235; --text:#edf2f7; --muted:#aab5c5; --line:#344054; --accent:#8ab4ff; --good:#7ee2a8; --bad:#ff9b91; } }
* { box-sizing:border-box; } body { margin:0; background:var(--bg); color:var(--text); font:14px system-ui,sans-serif; }
main { max-width:1200px; margin:auto; padding:32px 20px; } header { margin-bottom:24px; } h1 { margin:0 0 6px; font-size:30px; } h2 { margin:0 0 14px; font-size:18px; } .subtitle { color:var(--muted); }
.cards { display:grid; grid-template-columns:repeat(6,1fr); gap:12px; margin-bottom:20px; } .card,.panel { background:var(--card); border:1px solid var(--line); border-radius:14px; padding:16px; }
.label { color:var(--muted); font-size:12px; } .value { display:block; margin-top:7px; font-size:24px; font-weight:700; } .grid { display:grid; grid-template-columns:2fr 1fr; gap:20px; } table { width:100%; border-collapse:collapse; } th,td { padding:11px 8px; border-bottom:1px solid var(--line); text-align:left; } th { color:var(--muted); font-size:12px; }
.pill { border-radius:999px; padding:3px 9px; font-size:12px; } .ok { color:var(--good); background:color-mix(in srgb,var(--good) 15%,transparent); } .fail { color:var(--bad); background:color-mix(in srgb,var(--bad) 15%,transparent); }
.chips { display:flex; flex-wrap:wrap; gap:7px; margin-bottom:14px; } .chip { border:1px solid var(--line); border-radius:999px; padding:5px 9px; font-size:12px; } ul { margin:8px 0 0; padding-left:20px; } a { color:var(--accent); } .log { min-height:100px; white-space:pre-wrap; overflow:auto; font:12px ui-monospace,Consolas,monospace; color:var(--muted); }
@media (max-width:900px) { .cards { grid-template-columns:repeat(3,1fr); } .grid { grid-template-columns:1fr; } } @media (max-width:560px) { .cards { grid-template-columns:repeat(2,1fr); } }
</style>
</head>
<body><main>
<header><h1>FMS Automation Viewer</h1><div class="subtitle">read-only, localhost only</div></header>
<section class="cards" id="cards"></section>
<div class="grid">
<section class="panel"><h2>Routes</h2><div id="routes"></div></section>
<section class="panel"><h2>Guard status</h2><div id="guard"></div></section>
</div>
<section class="panel" style="margin-top:20px"><h2>Reports</h2><ul id="reports"></ul></section>
<section class="panel" style="margin-top:20px"><h2>Log tail</h2><div class="log" id="logs"></div></section>
</main>
<script>
const text = (element, value) => { element.textContent = value == null ? "" : String(value); };
const node = (tag, value, className) => { const element = document.createElement(tag); text(element, value); if (className) element.className = className; return element; };
async function load() {
  const [summary, guard, reports, logs] = await Promise.all([
    fetch("/api/summary").then(response => response.json()),
    fetch("/api/guard").then(response => response.json()),
    fetch("/api/reports").then(response => response.json()),
    fetch("/api/log?lines=50").then(response => response.json())
  ]);
  const cards = document.getElementById("cards"); cards.replaceChildren();
  const total = summary.total || {};
  const failureRate = total["Request Count"] ? (100 * total["Failure Count"] / total["Request Count"]).toFixed(2) + "%" : "0%";
  [["Requests", total["Request Count"]], ["Failures", total["Failure Count"]], ["Failure rate", failureRate], ["Median ms", total["Median Response Time"]], ["p95 ms", total["95%"]], ["Requests/s", total["Requests/s"]]].forEach(item => { const card = document.createElement("div"); card.className = "card"; card.append(node("span", item[0], "label"), node("span", summary.has_data ? item[1] : "No run yet", "value")); cards.append(card); });
  const routes = document.getElementById("routes"); routes.replaceChildren();
  if (!summary.has_data) routes.append(node("p", "No run yet"));
  else { const table = document.createElement("table"); const head = document.createElement("tr"); ["Route","Requests","Failures","Median","p95","RPS"].forEach(value => head.append(node("th", value))); table.append(head); (summary.routes || []).forEach(route => { const row = document.createElement("tr"); [route.name, route.requests, route.failures, route.median, route.p95, route.rps].forEach(value => row.append(node("td", value))); const pill = node("span", route.failures ? "failures" : "ok", "pill " + (route.failures ? "fail" : "ok")); row.children[2].replaceChildren(pill); table.append(row); }); routes.append(table); }
  const guardBox = document.getElementById("guard"); guardBox.replaceChildren(); const chips = document.createElement("div"); chips.className = "chips"; [...guard.allowed_hosts.map(value => "host: " + value), "MAX_USERS: " + guard.max_users, "RPS cap: " + guard.rps_cap, "writes blocked: " + (!guard.allow_writes ? "yes" : "no")].forEach(value => chips.append(node("span", value, "chip"))); guardBox.append(chips, node("strong", "Blocked routes")); const blocked = document.createElement("ul"); guard.deny_patterns.forEach(value => blocked.append(node("li", value))); guardBox.append(blocked);
  const reportList = document.getElementById("reports"); reportList.replaceChildren(); reports.forEach(value => { const item = document.createElement("li"); const link = document.createElement("a"); link.href = "/reports/" + encodeURIComponent(value); text(link, value); item.append(link); reportList.append(item); }); if (!reports.length) reportList.append(node("li", "No reports"));
  text(document.getElementById("logs"), logs.join("\n") || "No log entries");
}
load(); setInterval(load, 5000);
</script>
</body></html>"""


@app.get("/")
def home():
    return HTMLResponse(PAGE)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8765)
