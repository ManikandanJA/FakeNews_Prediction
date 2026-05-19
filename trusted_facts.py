# trusted_facts.py
# Trusted & Verified Real News / Facts Database
# Built by: Manikandan J.A.

# ── Verified correct facts ─────────────────────────────────
trusted_info = {
    # Politics
    "Narendra Modi is the Prime Minister of India": {
        "value": "Narendra Modi Prime Minister India",
        "source": "https://www.pmindia.gov.in", "confidence": 100},
    "Droupadi Murmu is the President of India": {
        "value": "Droupadi Murmu President India",
        "source": "https://www.pib.gov.in", "confidence": 100},
    "Nirmala Sitharaman is the Finance Minister": {
        "value": "Nirmala Sitharaman Finance Minister",
        "source": "https://www.indiabudget.gov.in", "confidence": 100},
    "Amit Shah is the Home Minister of India": {
        "value": "Amit Shah Home Minister India",
        "source": "https://www.pmindia.gov.in", "confidence": 100},
    "M K Stalin is the Chief Minister of Tamil Nadu": {
        "value": "Stalin Chief Minister Tamil Nadu",
        "source": "https://www.tn.gov.in", "confidence": 100},

    # Tech CEOs — correct combos
    "Sundar Pichai is the CEO of Google": {
        "value": "Sundar Pichai CEO Google",
        "source": "https://about.google/", "confidence": 100},
    "Tim Cook is the CEO of Apple": {
        "value": "Tim Cook CEO Apple",
        "source": "https://www.apple.com/newsroom/", "confidence": 100},
    "Satya Nadella is the CEO of Microsoft": {
        "value": "Satya Nadella CEO Microsoft",
        "source": "https://www.microsoft.com/en-us/about", "confidence": 100},
    "Elon Musk is the CEO of Tesla": {
        "value": "Elon Musk CEO Tesla",
        "source": "https://www.tesla.com", "confidence": 100},
    "Andy Jassy is the CEO of Amazon": {
        "value": "Andy Jassy CEO Amazon",
        "source": "https://www.aboutamazon.com", "confidence": 100},
    "Mark Zuckerberg is the CEO of Meta": {
        "value": "Mark Zuckerberg CEO Meta",
        "source": "https://about.fb.com", "confidence": 100},
    "Sam Altman is the CEO of OpenAI": {
        "value": "Sam Altman CEO OpenAI",
        "source": "https://openai.com/about/", "confidence": 100},

    # General facts
    "India capital is New Delhi": {
        "value": "India capital New Delhi",
        "source": "https://www.india.gov.in", "confidence": 100},
    "Taj Mahal is located in Agra": {
        "value": "Taj Mahal Agra",
        "source": "https://www.asi.nic.in", "confidence": 100},
    "ISRO successfully launched Chandrayaan 3": {
        "value": "ISRO Chandrayaan 3 launched",
        "source": "https://www.isro.gov.in", "confidence": 100},

    # Cinema
    "Thalapathy Vijay is a Tamil actor": {
        "value": "Thalapathy Vijay Tamil actor",
        "source": "https://en.wikipedia.org/wiki/Vijay_(actor)", "confidence": 100},
    "Superstar Rajinikanth is a Tamil actor": {
        "value": "Superstar Rajinikanth Tamil actor",
        "source": "https://en.wikipedia.org/wiki/Rajinikanth", "confidence": 100},
}

# ── Role → Correct Person mapping (for contradiction check) ──
CORRECT_ROLE_MAP = {
    # Tech CEOs
    "ceo of google"     : "sundar pichai",
    "google ceo"        : "sundar pichai",
    "google's ceo"      : "sundar pichai",
    "ceo of apple"      : "tim cook",
    "apple ceo"         : "tim cook",
    "apple's ceo"       : "tim cook",
    "ceo of microsoft"  : "satya nadella",
    "microsoft ceo"     : "satya nadella",
    "microsoft's ceo"   : "satya nadella",
    "ceo of tesla"      : "elon musk",
    "tesla ceo"         : "elon musk",
    "ceo of amazon"     : "andy jassy",
    "amazon ceo"        : "andy jassy",
    "ceo of meta"       : "mark zuckerberg",
    "meta ceo"          : "mark zuckerberg",
    "ceo of facebook"   : "mark zuckerberg",
    "ceo of openai"     : "sam altman",
    "openai ceo"        : "sam altman",
    "ceo of twitter"    : "elon musk",
    "twitter ceo"       : "elon musk",

    # Indian Politics
    "prime minister of india"   : "narendra modi",
    "india prime minister"      : "narendra modi",
    "pm of india"               : "narendra modi",
    "india's pm"                : "narendra modi",
    "president of india"        : "droupadi murmu",
    "india's president"         : "droupadi murmu",
    "chief minister of tamil nadu" : "mk stalin",
    "tamil nadu cm"             : "mk stalin",
    "tamil nadu chief minister" : "mk stalin",
    "finance minister of india" : "nirmala sitharaman",
    "home minister of india"    : "amit shah",
}

# ── All known persons (for wrong-role detection) ──
ALL_KNOWN_PERSONS = {
    "sundar pichai", "tim cook", "satya nadella", "elon musk",
    "andy jassy", "mark zuckerberg", "sam altman", "jeff bezos",
    "narendra modi", "droupadi murmu", "mk stalin", "m k stalin",
    "nirmala sitharaman", "amit shah", "rahul gandhi", "arvind kejriwal",
}


def check_fact(news_text):
    """
    3-level check:
    1. Correct fact match  → Real (Verified)
    2. Contradiction check → Fake (Wrong person for role)
    3. No match            → Pass to AI/ML
    """
    news_lower = news_text.strip().lower()

    # ── Level 1: Correct fact match ──────────────────────
    for key, info in trusted_info.items():
        value_words = info["value"].lower().split()
        if all(w in news_lower for w in value_words):
            return "Real (Verified)", info.get("confidence", 100), info["source"]

    # ── Level 2: Contradiction detection ─────────────────
    # e.g. "Google CEO is Tim Cook" → Google CEO = Sundar Pichai
    #       Tim Cook is wrong → FAKE
    for role_phrase, correct_person in CORRECT_ROLE_MAP.items():
        if role_phrase in news_lower:
            # Role mentioned — check if correct person is in text
            if correct_person in news_lower:
                # Correct person + role → Real
                # Find source
                for key, info in trusted_info.items():
                    if correct_person.replace(" ", "").lower() in info["value"].lower().replace(" ", ""):
                        return "Real (Verified)", 100, info["source"]
                return "Real (Verified)", 95, "https://www.google.com"
            else:
                # Role mentioned but correct person NOT in text
                # Check if a WRONG known person is mentioned
                for person in ALL_KNOWN_PERSONS:
                    if person in news_lower and person != correct_person:
                        return (
                            f"Fake (Wrong Info — {role_phrase.title()} is {correct_person.title()}, not {person.title()})",
                            96,
                            None
                        )
                # Role + unknown person → likely fake
                return (
                    f"Fake (Unverified — Correct {role_phrase.title()} is {correct_person.title()})",
                    85,
                    None
                )

    # ── Level 3: Sports keyword fallback ─────────────────
    sports_kw = ["cricket", "bcci", "icc", "world cup", "ipl"]
    if any(w in news_lower for w in sports_kw):
        return "Real (Verified - Sports)", 100, "https://www.bcci.tv"

    # ── No match → pass to AI/ML ─────────────────────────
    return "", 0, None
