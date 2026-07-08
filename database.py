from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Incident(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    event = db.Column(db.String(300))

    severity = db.Column(db.String(30))

    status = db.Column(db.String(30))


class ScanHistory(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    filename = db.Column(db.String(200))

    total_logs = db.Column(db.Integer)

    failed_logins = db.Column(db.Integer)

    risk_score = db.Column(db.Integer)