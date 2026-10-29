# Automation plan (draft)
Goal: every staging build is tested automatically (API, mobile, admin) and a daily report goes to Basanti and Naveen.
Stack: Python, pytest, httpx, Locust, Maestro, Playwright, Azure Pipelines.
Facts: NestJS + PostgreSQL backend, Swagger at /api, Expo React Native apps, Azure Pipelines to Firebase App Distribution.
Phases: 0 setup, 1 API POC, 2 load POC, 3 Maestro Android POC, 4 admin, 5 pipeline and report, 6 expand.
Scope out for now: maps, push, live chat, pen testing, iOS automation.
Rules: staging only, a test is done after 3 green runs in a row.
Open: testIDs in the apps, Azure access, seed/reset impact on test accounts.
