from config import HOT_THRESHOLD


def calculate_score(lead):
    score = 0

    if lead.company:
        score += 30

    if lead.message and len(lead.message) > 50:
        score += 40

    if lead.email.endswith(".com"):
        score += 30

    return score


def classify_lead(score):
    if score >= HOT_THRESHOLD:
        return "hot"
    if score >= 50:
        return "warm"
    return "cold"
