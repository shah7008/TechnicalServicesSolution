# app/model/db.py
import pyodbc
from app.config import SQL_SERVER, SQL_DATABASE, SQL_USERNAME, SQL_PASSWORD, SQL_DRIVER


# def get_connection():
#     """
#     Establish a connection to SQL Server with comprehensive error handling
#     """
#     try:
#         # Build connection string more cleanly
#         conn_str = (
#             f"DRIVER={{{SQL_DRIVER}}};"
#             f"SERVER={SQL_SERVER};"
#             f"DATABASE={SQL_DATABASE};"
#             f"UID={SQL_USERNAME};"
#             f"PWD={SQL_PASSWORD};"
#             f"TrustServerCertificate=yes;"
#             f"Connection Timeout=30;"  # Added timeout
#         )
#
#         # Remove the need for replace by building string directly
#         conn_str = f"DRIVER={SQL_DRIVER};SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};UID={SQL_USERNAME};PWD={SQL_PASSWORD};TrustServerCertificate=yes;Connection Timeout=30;"
#
#         # Establish connection
#         cnxn = pyodbc.connect(conn_str, autocommit=False)
#         cnxn.fast_executemany = True
#
#         print("✅ Database connection established successfully!")
#         return cnxn
#
#     except pyodbc.InterfaceError as e:
#         print(f"❌ Interface Error: Invalid connection parameters - {e}")
#         return None
#     except pyodbc.OperationalError as e:
#         print(f"❌ Operational Error: Cannot connect to server - {e}")
#         return None
#     except pyodbc.DatabaseError as e:
#         print(f"❌ Database Error: Issue with database - {e}")
#         return None
#     except Exception as e:
#         print(f"❌ Unexpected error: {e}")
#         return None

def get_connection():
    try:
        SQL_DRIVER = 'ODBC Driver 18 for SQL Server'
        SQL_SERVER = r"DESKTOP-SNKKUPV\SQLEXPRESS"  # or your server name
        SQL_DATABASE = 'AbidBilalServices'

        # Windows Authentication connection string
        conn_str = (
            f"DRIVER={{{SQL_DRIVER}}};"
            f"SERVER={SQL_SERVER};"
            f"DATABASE={SQL_DATABASE};"
            f"Trusted_Connection=yes;"
            f"TrustServerCertificate=yes;"
        )

        cnxn = pyodbc.connect(conn_str, autocommit=False)
        #cnxn.fast_executemany = True
        print("✅ Windows Authentication connection successful!")
        return cnxn

    except pyodbc.Error as e:
        print(f"❌ Connection failed: {e}")
        return None


#get_connection()