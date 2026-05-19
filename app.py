from flask import Flask, render_template, request, redirect, url_for, session, flash
import pickle
import database
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fakenews_secret_2025")

# ── LOAD MODEL ─────────────────────────
with open("model.pkl", "rb") as f:
    data = pickle.load(f)
    model = data["model"]
    vectorizer = data["vectorizer"]

# ── DB SETUP ───────────────────────────
database.setup_db()

# ── HOME ───────────────────────────────
@app.route("/")
def index():
    return render_template("index.html",
                           logged_in="user" in session,
                           username=session.get("user"))

# ── ABOUT ──────────────────────────────
@app.route("/about")
def about():
    return render_template("about.html",
                           logged_in="user" in session,
                           username=session.get("user"))

# ── SIGNUP ─────────────────────────────
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        if password != confirm:
            flash("Passwords not match", "error")
        else:
            if database.create_user(username, password):
                flash("Signup success", "success")
                return redirect(url_for("login"))
            else:
                flash("User exists", "error")

    return render_template("signup.html")

# ── LOGIN ──────────────────────────────
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = database.verify_user(
            request.form["username"],
            request.form["password"]
        )

        if user:
            session["user"] = user["username"]
            session["user_id"] = user["id"]
            return redirect(url_for("predict"))
        else:
            flash("Invalid login", "error")

    return render_template("login.html")

# ── LOGOUT ─────────────────────────────
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# ── PREDICT ────────────────────────────
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if "user" not in session:
        return redirect(url_for("login"))

    result = ""
    confidence = 0
    news_text = ""
    source_url = None
    source_name = None

    if request.method == "POST":
        news_text = request.form["news_text"]

        X = vectorizer.transform([news_text])
        pred = model.predict(X)[0]

        # safe confidence
        try:
            prob = model.predict_proba(X)[0]
            confidence_raw = max(prob) * 100
        except:
            confidence_raw = 90

        # ── LOGIC ─────────────────────
        if confidence_raw >= 90:
            confidence = 100

            if pred == 1:
                result = "Real"
                source_url = "https://www.india.gov.in/"
                source_name = "Trusted Source"
            else:
                result = "Fake"
                source_url = None
                source_name = None
        else:
            result = "Partial"
            confidence = 40
            source_url = None
            source_name = None

        database.save_prediction(
            session["user_id"],
            news_text,
            result,
            confidence,
            "ML",
            source_name,
            source_url,
            "Model Prediction"
        )

    history_count = len(database.get_user_predictions(session["user_id"]))

    return render_template(
        "predict.html",
        result=result,
        confidence=confidence,
        news_text=news_text,
        username=session.get("user"),
        history_count=history_count
    )

# ── HISTORY ────────────────────────────
@app.route("/history")
def history():
    if "user" not in session:
        return redirect(url_for("login"))

    data = database.get_user_predictions(session["user_id"])

    return render_template(
        "history.html",
        history=data,
        username=session.get("user")
    )

# ── CLEAR HISTORY ──────────────────────
@app.route("/clear_history")
def clear_history():
    if "user" in session:
        database.clear_user_predictions(session["user_id"])
    return redirect(url_for("history"))

# ── RUN ────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)