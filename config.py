# config.py - Configuration
# Built by: Manikandan J.A.
import os

# Anthropic API Key - Set in Render Dashboard → Environment Variables
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# MySQL - for LOCAL development only
# On Render, DATABASE_URL env variable is used automatically (db.py handles it)
DB_HOST     = "localhost"
DB_USER     = "root"
DB_PASSWORD = "root"   # Change for local
DB_NAME     = "fakenews_db"
