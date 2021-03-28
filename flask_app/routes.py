from flask import jsonify, request
from http import HTTPStatus
from io import StringIO
from werkzeug.exceptions import BadRequest, NotFound

import pandas

from flask_app import app, db
from flask_app.models import TimeReport
from flask_app import utils


@app.route("/post_time_report", methods=["POST"])
def upload_time_report():
    """
    Endpoint to upload csv time sheet records
    """
    try:
        file = request.files["file"]
        filename = file.filename
    except FileNotFoundError:
        raise NotFound("No file found in request")

    if not utils.is_file_allowed(filename):
        raise BadRequest("File format not supported")

    report_id = int("".join(filter(str.isdigit, filename)))
    stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
    dataframe = pandas.read_csv(stream)
    for record in dataframe.itertuples():
        data = {
            "report_id": report_id,
            "date": pandas.to_datetime(record.date, dayfirst=True).date(),
            "hours_worked": record[2],
            "employee_id": record[3],
            "job_group": record[4],
        }
        db.session.add(TimeReport(**data))
    db.session.commit()

    # cache the upload timestamp
    utils.cache_content("timestamp", {})

    return "", HTTPStatus.CREATED


@app.route("/get_payroll_report", methods=["GET"])
def get_payroll_report():
    """
    Retrieve payroll report
    Optional params: employee_id, start_date, end_date
    """
    employee_id = request.args.get("employee_id", None)
    start_date = request.args.get("start_date", None)
    if start_date:
        start_date = pandas.to_datetime(start_date).date()
    end_date = request.args.get("end_date", None)
    if end_date:
        end_date = pandas.to_datetime(end_date).date()

    payload = utils.get_payload(employee_id, start_date, end_date)

    return jsonify(payload)
