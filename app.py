from flask import Flask, render_template, request, redirect, session, url_for
from detector import analyze_logs
import os

app = Flask(__name__)

# Secret key for session
app.secret_key = "securevision_secret_key"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -----------------------------
# LOGIN
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":

            session["user"] = username
            return redirect(url_for("dashboard"))

        else:

            return render_template(
                "login.html",
                error="Invalid Username or Password"
            )

    return render_template("login.html")


# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect(url_for("login"))


# -----------------------------
# DASHBOARD
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def dashboard():

    # User not logged in
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