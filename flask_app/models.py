from enum import Enum
from flask_app import db
from sqlalchemy.orm import validates


class JobGroup(Enum):
    A = 20
    B = 30


class TimeReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, nullable=False)
    employee_id = db.Column(db.Integer, index=True, nullable=False)
    date = db.Column(db.Date, index=True, nullable=False)
    hours_worked = db.Column(db.Float, nullable=False)
    job_group = db.Column(db.Enum(JobGroup), nullable=False)

    @validates("hours_worked")
    def validate_hours(self, key, value):
        assert 24 >= value > 0
        return value
