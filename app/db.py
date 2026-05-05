import os
import urllib
from sqlalchemy import create_engine
from app.config import DB_DRIVER, DB_SERVER, DB_DATABASE, DB_USERNAME, DB_PASSWORD

TESTING = os.getenv("TESTING")

if TESTING:
    # Use in-memory SQLite for tests
    engine = create_engine("sqlite:///:memory:")
else:
    connection_string = (
        f"Driver={{{DB_DRIVER}}};"
        f"Server=tcp:{DB_SERVER},1433;"
        f"Database={DB_DATABASE};"
        f"Uid={DB_USERNAME};"
        f"Pwd={DB_PASSWORD};"
        "Encrypt=yes;"
    )

    params = urllib.parse.quote_plus(connection_string)

    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")