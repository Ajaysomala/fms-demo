import csv

from fastapi.testclient import TestClient


def _client(monkeypatch, tmp_path):
    reports = tmp_path / "reports"
    reports.mkdir()
    monkeypatch.setenv("REPORTS_DIR", str(reports))
    monkeypatch.setenv("LOG_FILE", str(tmp_path / "automation.log"))
    from ui.app import app

    return TestClient(app), reports


def test_home_page(monkeypatch, tmp_path):
    client, _ = _client(monkeypatch, tmp_path)
    response = client.get("/")
    assert response.status_code == 200
    assert "FMS Automation Viewer" in response.text


def test_home_page_preserves_javascript_newline_escape(monkeypatch, tmp_path):
    client, _ = _client(monkeypatch, tmp_path)
    body = client.get("/").text
    assert r'logs.join("\n")' in body
    assert not any(line.endswith('logs.join("') for line in body.splitlines())
    assert not any(line.startswith('") ||') for line in body.splitlines())


def test_summary_without_csv(monkeypatch, tmp_path):
    client, _ = _client(monkeypatch, tmp_path)
    assert client.get("/api/summary").json() == {"has_data": False}


def test_summary_reads_locust_csv(monkeypatch, tmp_path):
    client, reports = _client(monkeypatch, tmp_path)
    fields = ["Name", "Request Count", "Failure Count", "Median Response Time", "Average Response Time", "95%", "99%", "Requests/s", "Failures/s"]
    with (reports / "load_public_stats.csv").open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        writer.writerow({"Name": "Aggregated", "Request Count": "7", "Failure Count": "1", "Median Response Time": "10", "Average Response Time": "12", "95%": "20", "99%": "30", "Requests/s": "1.5", "Failures/s": "0.2"})
    body = client.get("/api/summary").json()
    assert body["has_data"] is True
    assert body["total"]["Request Count"] == 7


def test_reports_reject_unsafe_names(monkeypatch, tmp_path):
    client, reports = _client(monkeypatch, tmp_path)
    (reports / ".env").write_text("secret", encoding="utf-8")
    (reports / "secret.txt").write_text("secret", encoding="utf-8")
    assert client.get("/reports/..%2f.env").status_code == 404
    assert client.get("/reports/.env").status_code == 404
    assert client.get("/reports/secret.txt").status_code == 404


def test_summary_post_is_not_allowed(monkeypatch, tmp_path):
    client, _ = _client(monkeypatch, tmp_path)
    assert client.post("/api/summary").status_code == 405


def test_log_masks_secrets(monkeypatch, tmp_path):
    client, _ = _client(monkeypatch, tmp_path)
    (tmp_path / "automation.log").write_text("Bearer abc123 call 555111555\n", encoding="utf-8")
    body = client.get("/api/log").json()
    assert "abc123" not in body[0]
    assert "555111555" not in body[0]


def test_guard_has_staging_host(monkeypatch, tmp_path):
    client, _ = _client(monkeypatch, tmp_path)
    assert "api-uat.findmyservices.ae" in client.get("/api/guard").json()["allowed_hosts"]
