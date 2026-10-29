"""Tiny MOCK backend for the demo. It is NOT the FMS backend.
Set DEMO_BUG=1 to make the monthly total wrong, so the tests catch it."""
import os
import re
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Demo mock API")
PROVIDERS = [
    {"id": 1, "name": "Caregiver A", "hourly_rate": 40},
    {"id": 2, "name": "Caregiver B", "hourly_rate": 60},
]
DAYS = {"weekly": 7, "monthly": 30}
FEE = 10


class OtpIn(BaseModel):
    mobile: str
    otp: str


class BookingIn(BaseModel):
    provider_id: int
    plan: str
    hours_per_day: int


def check_auth(authorization: str | None):
    if authorization != "Bearer demo-token":
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/auth/verify-otp")
def verify_otp(body: OtpIn):
    if not re.fullmatch(r"5\d{8}", body.mobile):
        raise HTTPException(status_code=422, detail="Invalid mobile")
    if body.otp != "1234":
        raise HTTPException(status_code=401, detail="Wrong OTP")
    return {"token": "demo-token"}


@app.get("/providers")
def providers(authorization: str | None = Header(default=None)):
    check_auth(authorization)
    return PROVIDERS


@app.post("/bookings")
def create_booking(body: BookingIn, authorization: str | None = Header(default=None)):
    check_auth(authorization)
    provider = next((p for p in PROVIDERS if p["id"] == body.provider_id), None)
    if provider is None or body.plan not in DAYS:
        raise HTTPException(status_code=400, detail="Bad request")
    days = DAYS[body.plan]
    subtotal = provider["hourly_rate"] * body.hours_per_day * days
    if os.getenv("DEMO_BUG") == "1" and body.plan == "monthly":
        subtotal = int(subtotal * 2.3)
    return {"plan": body.plan, "days": days, "subtotal": subtotal, "fees": FEE, "total": subtotal + FEE}
