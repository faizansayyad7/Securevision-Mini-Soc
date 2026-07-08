from flask import Flask, render_template, request, redirect, session, url_for
from detector import analyze_logs
from database import db, ScanHistory, Incident
import os

app = Flask(__name__)

app.secret_key = "securevision_secret_key"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# SQLite Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///securevision.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create Database Tables
with app.app_context():
    db.create_all()


# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":

            session["user"] = username

            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid Username or Password"
        )

    return render_template("login.html")


# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect(url_for("login"))


# ---------------- DASHBOARD ---------------- #

@app.route("/", methods=["GET", "POST"])
def dashboard():

    if "user" not in session:

        return redirect(url_for("login"))

    if request.method == "POST":

        file = request.files["logfile"]

        if file and file.filename.endswith(".txt"):

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                "logs.txt"
            )

            file.save(filepath)

            data = analyze_logs(filepath)
            # Save Scan History
            scan = ScanHistory(
               filename=file.filename,
                 total_logs=data["total"],
                  failed_logins=data["failed"],
                   risk_score=min(data["failed"] * 10, 100)
                )

            db.session.add(scan)

                # Save Incidents
            for item in data["incidents"]:

             incident = Incident(
              event=item["event"],
              severity=item["severity"],
              status=item["status"]
             )

            db.session.add(incident)

            db.session.commit()

        else:

            data = analyze_logs("logs.txt")

    else:

        if os.path.exists("uploads/logs.txt"):

            data = analyze_logs("uploads/logs.txt")

        else:

            data = analyze_logs("logs.txt")

    risk = min(data["failed"] * 10, 100)

    health = max(100 - risk, 0)

    return render_template(
        "dashboard.html",
        logs=data["logs"],
        incidents=data["incidents"],
        failed=data["failed"],
        total=data["total"],
        alert=data["alert"],
        low=data["low"],
        medium=data["medium"],
        critical=data["critical"],
        risk=risk,
        health=health
    )


if __name__ == "__main__":
    app.run(debug=True)