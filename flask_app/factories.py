from random import randint, choices
from flask_app import models, db

import pandas
import factory
from factory.alchemy import SQLAlchemyModelFactory


class BaseMeta:
    sqlalchemy_session = db.session
    sqlalchemy_session_persistence = "flush"


class TimeReportFactory(SQLAlchemyModelFactory):
    class Meta(BaseMeta):
        model = models.TimeReport

    report_id = randint()
    employee_id = randint()
    date = pandas.Timestamp.now().datetime().date
    hours_worked = randint(1, 23)
    job_group = choices(["A", "B"])
