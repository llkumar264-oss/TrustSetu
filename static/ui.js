// --------------------
// Theme (Dark/Light)
// --------------------
const root = document.documentElement;
const themeBtn = document.getElementById("themeBtn");
const themeIcon = document.getElementById("themeIcon");

function setTheme(mode) {
  if (mode === "dark") {
    root.classList.add("dark");
    localStorage.setItem("trustsetu_theme", "dark");
    themeIcon.textContent = "☀️";
  } else {
    root.classList.remove("dark");
    localStorage.setItem("trustsetu_theme", "light");
    themeIcon.textContent = "🌙";
  }
}

const saved = localStorage.getItem("trustsetu_theme");
setTheme(saved ? saved : "dark");

themeBtn.addEventListener("click", () => {
  const isDark = root.classList.contains("dark");
  setTheme(isDark ? "light" : "dark");
});

// --------------------
// Helpers
// --------------------
function pretty(obj) {
  return JSON.stringify(obj, null, 2);
}

function pct(prob) {
  return Math.round(prob * 100);
}

function setRiskUI(finalProb, warning, action, baseProb, extraProb) {
  const riskBar = document.getElementById("riskBar");
  const riskValue = document.getElementById("riskValue");
  const warningText = document.getElementById("warningText");

  const baseEl = document.getElementById("baseProb");
  const extraEl = document.getElementById("extraProb");
  const actionEl = document.getElementById("suggestedAction");

  riskBar.style.width = `${pct(finalProb)}%`;
  riskValue.textContent = `${pct(finalProb)}%`;
  warningText.textContent = warning;

  baseEl.textContent = baseProb;
  extraEl.textContent = extraProb;
  actionEl.textContent = action;
}

// --------------------
// Scam Check
// --------------------
document.getElementById("btnScamCheck").addEventListener("click", async () => {
  const text = document.getElementById("scamText").value.trim();
  const phone = document.getElementById("phoneNumber").value.trim();
  const lang = document.getElementById("lang").value;

  if (!text) {
    alert("Enter some message text to analyze!");
    return;
  }

  const payload = {
    text: text,
    phone_number: phone ? phone : null,
    language: lang
  };

  const rawResult = document.getElementById("rawResult");
  rawResult.textContent = "⏳ Analyzing...";

  try {
    const res = await fetch("/scam-check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    rawResult.textContent = pretty(data);

    setRiskUI(
      data.final_risk_probability,
      data.warning,
      data.suggested_action,
      data.base_scam_probability,
      data.extra_risk_from_reports
    );
  } catch (e) {
    rawResult.textContent = "❌ Error connecting to API";
  }
});

// --------------------
// Report Number
// --------------------
document.getElementById("btnReport").addEventListener("click", async () => {
  const num = document.getElementById("reportNumber").value.trim();
  const reason = document.getElementById("reportReason").value.trim();

  if (!num || !reason) {
    alert("Enter phone number and reason!");
    return;
  }

  const payload = { phone_number: num, reason: reason };
  const box = document.getElementById("reportResult");
  box.textContent = "⏳ Submitting report...";

  try {
    const res = await fetch("/report", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    box.textContent = pretty(data);
  } catch (e) {
    box.textContent = "❌ Error connecting to API";
  }
});

// --------------------
// Trust Badge
// --------------------
document.getElementById("btnBadge").addEventListener("click", async () => {
  const simAge = parseInt(document.getElementById("simAge").value || "0");
  const bankAge = parseInt(document.getElementById("bankAge").value || "0");
  const digilocker = document.getElementById("digilocker").checked;

  const payload = {
    sim_age_months: simAge,
    bank_account_age_months: bankAge,
    digilocker_verified: digilocker
  };

  const box = document.getElementById("badgeResult");
  box.textContent = "⏳ Generating badge...";

  try {
    const res = await fetch("/trust-badge", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    box.textContent = pretty(data);

    document.getElementById("trustScore").textContent = data.trust_score;
    document.getElementById("trustBadge").textContent = data.badge;
  } catch (e) {
    box.textContent = "❌ Error connecting to API";
  }
});
