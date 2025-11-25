# app/model/db.py
import pyodbc
from app.config import SQL_SERVER, SQL_DATABASE, SQL_USERNAME, SQL_PASSWORD, SQL_DRIVER

def get_connection():
    conn_str = (
        f"DRIVER={{{SQL_DRIVER}}};"
        f"SERVER={SQL_SERVER};"
        f"DATABASE={SQL_DATABASE};"
        f"UID={SQL_USERNAME};"
        f"PWD={SQL_PASSWORD};"
        f"TrustServerCertificate=Yes;"
    )
    # Fill in driver placeholder
    conn_str = conn_str.replace("{SQL_DRIVER}", SQL_DRIVER)
    cnxn = pyodbc.connect(conn_str, autocommit=False)
    cnxn.fast_executemany = True
    return cnxn