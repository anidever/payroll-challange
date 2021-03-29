import os
from http import HTTPStatus
import requests
import pytest

SERVER_URL = "http://localhost:5000"


def test_upload_time_reports():
    file_path = os.path.join(os.path.dirname(__file__), "time-report-42.csv")

    files = {"file": open(file_path, "rb")}
    response = requests.post(f"{SERVER_URL}/post_time_report", files=files)

    # This is expected to fail starting from the second time
    assert response.status_code == HTTPStatus.CREATED


def test_upload_same_file_id():
    file_path = os.path.join(os.path.dirname(__file__), "time-report-42.csv")

    files = {"file": open(file_path, "rb")}
    response = requests.post(f"{SERVER_URL}/post_time_report", files=files)

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize("employee_id", [1, 2])
def test_payroll_report(employee_id):

    start_date, end_date = "2016-11-01", "2016-11-15"
    response = requests.get(
        f"{SERVER_URL}/get_payroll_report?employee_id={employee_id}&start_date={start_date}&end_date={end_date}"
    )

    assert response.status_code == HTTPStatus.OK
    record = response.json()["payrollReport"]["employeeReports"][0]
    pay_period = record["payPeriod"]

    assert str(employee_id) == record["employeeId"]
    assert pay_period["startDate"] == start_date
    assert pay_period["endDate"] == end_date
    if employee_id == 1:
        assert record["amountPaid"] == "$150.00"
    elif employee_id == 2:
        assert record["amountPaid"] == "$930.00"
