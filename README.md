# fms-automation
Automated tests for FMS (API, load, mobile UI, admin). Staging only, never Production.

## Demo (runs locally, no FMS access needed)
The repo includes a MOCK server (demo_server) that mimics login, providers and weekly/monthly bookings.

### Setup
```
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Mac/Linux
pip install -r requirements.txt
```

### 1. API tests (all green)
```
pytest tests/api
```
Open `reports/report.html` for the report.

### 2. Catch a bug on purpose
```
set DEMO_BUG=1                  # Windows (cmd)
$env:DEMO_BUG="1"               # Windows (PowerShell)
export DEMO_BUG=1               # Mac/Linux
pytest tests/api
```
The monthly total test fails: that is how a real mismatch bug shows up.

### 3. Load test
Terminal A: `uvicorn demo_server.main:app --port 8000`
Terminal B: `locust -f load/locustfile.py --host http://127.0.0.1:8000`
Open http://localhost:8089, try 10 users, then 50.
Never point this at a shared environment without telling the devs.

### 4. Mobile (Maestro, needs an emulator and the staging APK)
```
maestro test flows/login.yaml
```
Flow texts are placeholders until checked against the real app.

### 5. Admin (Playwright)
```
playwright install chromium
set ADMIN_URL=<staging admin url>
pytest tests/admin -m admin
```

## Run against FMS staging
Copy `.env.example` to `.env`, fill BASE_URL, then update endpoint paths from Swagger (/api).
