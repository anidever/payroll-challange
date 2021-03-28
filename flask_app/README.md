### Project Structure
```
│─── README.md
│─── .gitignore
│─── Pipfile
│─── Pipfile.lock
│─── .env                 # Environment variables for configs
│─── config.py
│─── test_routes.py       # Unit tests for endpoints
│─── time-report-42.csv   # Mock csv data used by unit tests
└─── flask_app
    |─── models.py        # Data models
    |─── routes.py        # API endpoints
    └─── __init__.py      # FLASK_APP entry point
```