from flask import jsonify, request
from http import HTTPStatus
from io import StringIO
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized

import pandas

from flask_app import app, db
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
)
from flask_app.models import TimeReport
from flask_app import utils


@app.route("/login", methods=["POST"])
def login():
    username = request.args.get("username", None)
    if username == "test":
        raise Unauthorized("Bad username or password")

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


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
    employee_ids = dataframe["employee id"].unique()
    records = utils.prep_df_for_bulk_insert(dataframe, report_id)
    db.session.connection().execute(TimeReport.__table__.insert(), records)
    db.session.commit()

    # cache the upload timestamp
    for employee_id in employee_ids:
        utils.cache_content(str(employee_id), {}, ttl=3600)
    utils.cache_content("timestamp", {})

    return "", HTTPStatus.CREATED


@app.route("/get_payroll_report", methods=["GET"])
# @jwt_required()
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
