from flask import Flask, render_template
from detector import analyze_logs
from flask import Flask, render_template, request, redirect, url_for
from detector import analyze_logs
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def dashboard():

    if request.method == "POST":

        file = request.files["logfile"]

        if file and file.filename.endswith(".txt"):

            filepath = os.path.join(app.config["UPLOAD_FOLDER"], "logs.txt")

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