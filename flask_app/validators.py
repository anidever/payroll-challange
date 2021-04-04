from marshmallow import fields, validate, ValidationError
from flask_app import models, marshmallow


class TimeReportSchema(marshmallow.SQLAlchemySchema):
    class Meta:
        model = models.TimeReport
