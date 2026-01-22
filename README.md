# TRUSTSETU   
## Verify once. Transact safely everywhere.

TRUSTSETU is a hackathon prototype built for **PROMETEO (E-CONCLAVE’26, IIT Jodhpur)** to address a critical challenge in India’s digital economy:

> *First-time and rural users often cannot trust online systems due to scams, fake identities, and lack of transparent verification, leading to financial loss and reduced digital adoption.**

This project demonstrates a scalable, infrastructure-style solution that combines **Digital Trust**, **Access & Inclusion**, and **Economic Empowerment**.

---

# Key Modules

### 1) ScamShield (Digital Trust)
- Detects scam-like messages/call texts using ML-based risk scoring  
- Outputs **final scam probability (0–1)**  
- Provides **simple, explainable warnings** (Hindi/English)  
- Suggests actions like **Freeze & Report**

### 2) Crowd Reporting Layer (Trust + Transparency)
- Users can report suspicious phone numbers  
- Reported numbers increase future risk scores automatically  
- Builds a community-powered reputation system

### 3) TrustBadge (Access + Economic Empowerment)
- Generates a proof-based verification badge:
  - **Bronze / Silver / Gold**
- Based on simple trust signals (SIM age, bank age, DigiLocker verification)
- Helps verified sellers/gig workers gain confidence & conversion

---

##  Live Demo UI (Dark + Light Mode)
TRUSTSETU includes a modern glassmorphism UI with:
- Scam Risk Meter  
- Report Number Panel  
- TrustBadge Generator  
- Dark / Light theme toggle  

### UI Link:
 `http://127.0.0.1:8000/ui`

### API Docs:
 `http://127.0.0.1:8000/docs`

---

##  Tech Stack
- **FastAPI** (backend APIs)
- **Scikit-learn** (ML text classification)
- **Pandas** (dataset handling)
- **Jinja2** (HTML templating)
- **TailwindCSS CDN** (UI styling)

---

## How It Works
1. A user enters suspicious text (from a call/SMS/chat)
2. ScamShield predicts risk score using ML
3. Reported numbers add extra risk weight
4. Output is shown as:
   - 🔴 High Risk Scam  
   - 🟡 Suspicious  
   - 🟢 Likely Safe  
5. TrustBadge system helps verify trusted users/businesses

---

##  Setup Instructions

### 1) Install dependencies
```bash
pip install -r requirements.txt
