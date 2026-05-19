=====================================
  FAKE NEWS PREDICTION SYSTEM v3.1
=====================================
Built by : Manikandan J.A.
Tech     : Python, Flask, ML + Claude AI + MySQL

============================
SETUP STEPS
============================

STEP 1 - Install dependencies:
  pip install -r requirements.txt

STEP 2 - Setup MySQL DB:
  Open config.py and set:
    DB_HOST     = "localhost"
    DB_USER     = "root"
    DB_PASSWORD = "your_mysql_password"
    DB_NAME     = "fakenews_db"
  
  Tables are created AUTOMATICALLY when you run app.py!

STEP 3 - Setup Anthropic API Key (optional, for AI fact-check):
  Open config.py and set:
    ANTHROPIC_API_KEY = "sk-ant-xxxxxx"
  Get free key: https://console.anthropic.com/

STEP 4 - Train the ML model (first time only):
  python train_model.py

STEP 5 - Run the app:
  python app.py

STEP 6 - Open browser:
  http://127.0.0.1:5000

============================
MYSQL TABLES CREATED
============================
users
  - id, username, password, created_at

predictions
  - id, user_id, news_text, verdict,
    confidence, method, source_name,
    source_url, reason, created_at

============================
BUG FIXES in v3.1
============================
✅ Fixed false positive: "Google CEO is Mani" now correctly
   goes to AI/ML instead of returning "Real (Verified)"
✅ MySQL login/signup - accounts saved to database
✅ Prediction history saved to MySQL (not session)
