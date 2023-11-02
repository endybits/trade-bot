import os
from app.config.fconfig import get_db_credentials

db_credentials = get_db_credentials()
HOST = db_credentials.get("host")
USER = db_credentials.get("user")
PASSWORD = db_credentials.get("password")
DATABASE = db_credentials.get("database")
TARGET_TABLE = db_credentials.get("target_table")

MARIADB_URI = f"mariadb+mariadbconnector://{USER}:{PASSWORD}@{HOST}/{DATABASE}"
