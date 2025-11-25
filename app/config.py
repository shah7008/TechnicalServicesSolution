import os

# Prefer environment variables; fallback to hardcoded defaults for dev
SQL_SERVER = os.getenv("SQL_SERVER", r"DESKTOP-SNKKUPV\SQLEXPRESS")  # e.g., "YOUR-SERVER\\SQLEXPRESS" or IP
SQL_DATABASE = os.getenv("SQL_DATABASE", "AbidBilalServices")
SQL_USERNAME = os.getenv("SQL_USERNAME", r"DESKTOP-SNKKUPV\Ali Haider")
SQL_PASSWORD = os.getenv("SQL_PASSWORD", "pkk096006")
SQL_DRIVER = os.getenv("SQL_DRIVER", "ODBC Driver 18 for SQL Server")  # or "ODBC Driver 18 for SQL Server"

# UI constants
APP_TITLE = "AbidBilal Technical Services - AC Service Desk"
DEFAULT_PAGE_SIZE = 100

# Domain constants
VALID_STATUSES = ["Pending", "Assigned", "In Progress", "Completed", "Canceled"]
SERVICE_TYPES = ["Repair", "Tuning", "Installation"]
