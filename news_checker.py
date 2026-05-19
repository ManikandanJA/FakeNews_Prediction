# news_checker.py
# Uses Claude AI (Anthropic API) to verify news against trusted sources
# Built by: Manikandan J.A.
# NOTE: API key இல்லாமலும் app work aagum — ML Model fallback use aagum

import requests
import json

try:
    from config import ANTHROPIC_API_KEY
except ImportError:
    ANTHROPIC_API_KEY = ""

SYSTEM_PROMPT = """You are a professional news fact-checker.

When given a news headline or article text:
1. Verify if it is REAL or FAKE based on verifiable facts
2. If REAL: provide the best trusted source URL
3. Respond ONLY in valid JSON format — no markdown, no extra text

Response format (strict JSON only):
{
  "verdict": "Real" or "Fake" or "Unverified",
  "confidence": number between 50 and 100,
  "reason": "brief 1-2 sentence explanation",
  "source_name": "Trusted source name" or null,
  "source_url": "https://exact-url.com" or null
}

Trusted sources:
- Indian Govt: pmindia.gov.in, pib.gov.in, india.gov.in, tn.gov.in, isro.gov.in
- News: ndtv.com, thehindu.com, timesofindia.indiatimes.com, indianexpress.com
- International: bbc.com, reuters.com, apnews.com
- Sports: bcci.tv, icc-cricket.com, espncricinfo.com
- Tech: google.com/about, apple.com, microsoft.com

Rules:
- Clearly fake/impossible: verdict=Fake, confidence=90+, source_url=null
- Clearly real verifiable: verdict=Real, confidence=85+, include source_url
- Uncertain: verdict=Unverified, confidence=50-70, source_url=null
- ONLY return JSON, nothing else"""


def is_api_key_configured():
    """Check if a valid API key is set."""
    key = (ANTHROPIC_API_KEY or "").strip()
    return bool(key) and key not in ("your_api_key_here", "your_anthropic_api_key_here", "")


def check_news_with_ai(news_text):
    """
    Uses Claude AI to fact-check news.
    Returns: (verdict, confidence, reason, source_name, source_url)
    If no API key → returns None (falls back to ML model)
    """
    if not is_api_key_configured():
        return None, 0, "", None, None

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 300,
                "system": SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": f"Fact-check this news:\n\n{news_text}"}]
            },
            timeout=20
        )

        if response.status_code != 200:
            return None, 0, "", None, None

        data     = response.json()
        raw_text = data["content"][0]["text"].strip()
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()

        result      = json.loads(raw_text)
        verdict     = result.get("verdict", "Unverified")
        confidence  = float(result.get("confidence", 50))
        reason      = result.get("reason", "")
        source_name = result.get("source_name") or None
        source_url  = result.get("source_url") or None

        return verdict, confidence, reason, source_name, source_url

    except Exception:
        return None, 0, "", None, None
