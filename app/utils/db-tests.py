import sys
import mariadb

from app.config.fconfig import get_db_credentials as DB

db = DB()
HOST = db.get('host')
USER = db.get('user')
PASSWORD = db.get('password')
DATABASE = db.get('database')
TARGET_TABLE = db.get('target_table')

#query = f"""SELECT COUNT(id) FROM {TARGET_TABLE}"""
query = f"""SELECT * FROM {TARGET_TABLE} ORDER BY id LIMIT 1"""

## Connect to MariaDB
try:
    conn = mariadb.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        database=DATABASE
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

## Get cursor
cursor = conn.cursor()
cursor.execute(query)
for row in cursor:
    print(row)