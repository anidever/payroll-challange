### Project Structure
```
│─── README.md            # Challenge specific README
│─── .gitignore
│─── Pipfile
│─── Pipfile.lock
│─── .env.example         # Environment variables for configs
│─── config.py
│─── test_routes.py       # Unit tests for endpoints
│─── time-report-42.csv   # Mock csv data used by unit tests
└─── flask_app
    |─── models.py        # Data models
    |─── routes.py        # API endpoints
    |─── README.md        # Project specific README
    └─── __init__.py      # FLASK_APP entry point
```