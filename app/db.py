import os
import urllib
from sqlalchemy import create_engine
from app.config import DB_DRIVER, DB_SERVER, DB_DATABASE, DB_USERNAME, DB_PASSWORD

TESTING = os.getenv("TESTING")

if TESTING:
    # Use in-memory SQLite for tests
    engine = create_engine("sqlite:///:memory:")
else:
    DATABASE_URL = (
        f"mssql+pymssql://{DB_USERNAME}:{DB_PASSWORD}"
        f"@{DB_SERVER}:1433/{DB_DATABASE}"
    )

    engine = create_engine(DATABASE_URL)