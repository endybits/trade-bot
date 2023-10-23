import sys
import mariadb

from app.config.fconfig import get_db_credentials as DB

db = DB()
HOST = db.get('host')
USER = db.get('user')
PASSWORD = db.get('password')
DATABASE = db.get('database')
TARGET_TABLE = db.get('target_table')

query = f"""SELECT 
    COUNT(*) AS total_trades,
    SUM(CASE WHEN is_win_loss_be = 'win' THEN 1 ELSE 0 END) AS total_wins,
    (SUM(CASE WHEN is_win_loss_be = 'win' THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS winning_percentage
FROM 
    {TARGET_TABLE}
WHERE 
    user_id < 10000
    AND portfolio_id IN ('Account 1', 'Account 2')
ORDER BY 
    open_date DESC
LIMIT 50;"""

query1 = f"""SELECT symbol, close_datetime, gross_total_return_on_trade AS pnl
FROM {TARGET_TABLE}
WHERE user_id = 3
ORDER BY pnl DESC
LIMIT 1"""

query2 = f"""SELECT HOUR(transaction_datetime) AS hour_of_day, SUM(gross_total_return_on_trade) AS pnl
FROM {TARGET_TABLE}
WHERE user_id = 191
    AND DAYOFWEEK(transaction_datetime) = 3 -- Tuesday
    AND YEAR(transaction_datetime) = 2023
GROUP BY hour_of_day
ORDER BY pnl DESC"""

query3 = f"""SELECT COUNT(id)
FROM users"""
# query = "SELECT id FROM users WHERE id < 1000"

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
cursor.execute(query2)

for row in cursor:
    print(row)

cursor.close()