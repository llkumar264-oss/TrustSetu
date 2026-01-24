from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import joblib
import json
import os

from trust_engine import trust_badge

MODEL_PATH = "scam_model.joblib"
REPORTS_PATH = "db/reports.json"

app = FastAPI(title="TRUSTSETU Prototype", version="2.1")

# ------------------------
# UI Setup (Templates + Static)
# ------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ------------------------
# Startup Setup
# ------------------------
os.makedirs("db", exist_ok=True)

if not os.path.exists(REPORTS_PATH):
    with open(REPORTS_PATH, "w", encoding="utf-8") as f:
        json.dump({"reported_numbers": {}}, f, indent=2)

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("❌ scam_model.joblib not found. Run: python scam_model.py")

model = joblib.load(MODEL_PATH)


def load_reports():
    with open(REPORTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_reports(data):
    with open(REPORTS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ------------------------
# Request Models
# ------------------------
class ScamCheckRequest(BaseModel):
    text: str
    phone_number: str | None = None
    language: str = "en"  # "en" or "hi"


class ReportRequest(BaseModel):
    phone_number: str
    reason: str


class TrustBadgeRequest(BaseModel):
    sim_age_months: int
    bank_account_age_months: int
    digilocker_verified: bool


# ------------------------
# Helper Functions
# ------------------------
def explain_warning(prob: float, lang: str = "en"):
    if prob >= 0.80:
        return "🔴 High Risk Scam" if lang == "en" else "🔴 Bahut khatarnak scam"
    if prob >= 0.50:
        return "🟡 Suspicious / Unverified" if lang == "en" else "🟡 Suspected / verify karo"
    return "🟢 Likely Safe" if lang == "en" else "🟢 Safe lag raha hai"


def action_suggestion(prob: float):
    if prob >= 0.80:
        return "Freeze & Report"
    if prob >= 0.50:
        return "Proceed with caution"
    return "Safe"


# ------------------------
# Routes
# ------------------------
@app.get("/")
def home():
    return {"message": "✅ TRUSTSETU API running", "ui": "/ui", "docs": "/docs"}


# ✅ Fix: favicon 404 not found
@app.get("/favicon.ico")
def favicon():
    return {}


@app.get("/ui", response_class=HTMLResponse)
def ui(request: Request):
    return templates.TemplateResponse("ui.html", {"request": request})


@app.post("/scam-check")
def scam_check(req: ScamCheckRequest):
    prob_scam = float(model.predict_proba([req.text])[0][1])
    reports = load_reports()

    # Extra risk if number is reported
    extra = 0.0
    if req.phone_number and req.phone_number in reports["reported_numbers"]:
        count = reports["reported_numbers"][req.phone_number]["count"]
        extra = min(0.25, 0.05 * count)

    final_prob = min(1.0, prob_scam + extra)

    return {
        "input_text": req.text,
        "phone_number": req.phone_number,
        "base_scam_probability": round(prob_scam, 3),
        "extra_risk_from_reports": round(extra, 3),
        "final_risk_probability": round(final_prob, 3),
        "warning": explain_warning(final_prob, req.language),
        "suggested_action": action_suggestion(final_prob),
    }


@app.post("/report")
def report_number(req: ReportRequest):
    reports = load_reports()

    if req.phone_number not in reports["reported_numbers"]:
        reports["reported_numbers"][req.phone_number] = {"count": 0, "reasons": []}

    reports["reported_numbers"][req.phone_number]["count"] += 1
    reports["reported_numbers"][req.phone_number]["reasons"].append(req.reason)

    save_reports(reports)

    return {
        "status": "✅ Report saved",
        "phone_number": req.phone_number,
        "total_reports": reports["reported_numbers"][req.phone_number]["count"],
        "recent_reasons": reports["reported_numbers"][req.phone_number]["reasons"][-3:],
    }


@app.post("/trust-badge")
def get_trust_badge(req: TrustBadgeRequest):
    return trust_badge(
        req.sim_age_months,
        req.bank_account_age_months,
        req.digilocker_verified
    )
