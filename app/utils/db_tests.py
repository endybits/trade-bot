import sys
import mariadb

from app.config.fconfig import get_db_credentials as DB

db = DB()
HOST = db.get('host')
USER = db.get('user')
PASSWORD = db.get('password')
DATABASE = db.get('database')
TARGET_TABLE = db.get('target_table')
TEST_USER_ID = db.get('test_user_id')

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

query3 = f"""SELECT portfolio_id, COUNT(portfolio_id)
FROM {TARGET_TABLE}
WHERE user_id = 4359
GROUP BY portfolio_id"""
query4 = f"""SHOW TABLES FROM {DATABASE}"""
query5 = f"""DESCRIBE portfolio"""
query6 = f"""SELECT COUNT(*) AS total_trades,
SUM(CASE WHEN {TARGET_TABLE}.is_win_loss_be = 'win' THEN 1 ELSE 0 END) AS total_wins,
(SUM(CASE WHEN {TARGET_TABLE}.is_win_loss_be = 'win' THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS winning_percentage
FROM {TARGET_TABLE}
LEFT JOIN portfolio ON {TARGET_TABLE}.portfolio_id = portfolio.portfolio_id
WHERE {TARGET_TABLE}.user_id = {TEST_USER_ID} 
AND portfolio.name IN ('Account 1', 'Account 2')
"""
query7 = f"""SELECT {TARGET_TABLE}.portfolio_id AS portfolio_id, portfolio.name AS name, {TARGET_TABLE}.portfolio_value
FROM {TARGET_TABLE}
LEFT JOIN portfolio ON {TARGET_TABLE}.portfolio_id = portfolio.portfolio_id
WHERE {TARGET_TABLE}.user_id = {TEST_USER_ID}

"""

def db_querier(query: str):
    # Find a good sql validator

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

    db_response_list = []
    for row in cursor:
        db_response_list.append(row)
        print(row)
    cursor.close()
    return db_response_list

#db_querier(query7)