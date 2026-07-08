from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Incident(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    event = db.Column(db.String(300), nullable=False)

    severity = db.Column(db.String(30), nullable=False)

    status = db.Column(db.String(30), nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class ScanHistory(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    filename = db.Column(db.String(200), nullable=False)

    total_logs = db.Column(db.Integer)

    failed_logins = db.Column(db.Integer)

    risk_score = db.Column(db.Integer)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )