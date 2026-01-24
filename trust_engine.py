def trust_badge(sim_age_months: int, bank_account_age_months: int, digilocker_verified: bool):
    """
    Simple Proof-based Trust Score (0-100)
    TRUSTSETU Hackathon Prototype
    """

    score = 0

    # SIM tenure (0-35)
    if sim_age_months >= 24:
        score += 35
    elif sim_age_months >= 6:
        score += 20
    else:
        score += 5

    # Bank account tenure (0-35)
    if bank_account_age_months >= 36:
        score += 35
    elif bank_account_age_months >= 12:
        score += 20
    else:
        score += 5

    # DigiLocker proof (0-30)
    score += 30 if digilocker_verified else 0

    # Badge mapping
    if score >= 80:
        badge = "Gold Verified"
    elif score >= 50:
        badge = "Silver Verified"
    else:
        badge = "Bronze Verified"

    return {"trust_score": score, "badge": badge}
