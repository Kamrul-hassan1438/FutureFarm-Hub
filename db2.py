
from flask import Flask
import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='',
    database='futurefarm hub'
)

def conversations(user_id):
    # Fetch users involved in conversations with the specified user
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT u.id, u.username,u.ActualID 
        FROM users u
        JOIN (
            SELECT user_id_1 AS user_id FROM conversations WHERE user_id_2 = %s 
            UNION 
            SELECT user_id_2 AS user_id FROM conversations WHERE user_id_1 = %s
        ) AS c ON u.id = c.user_id
    """, (user_id, user_id))
    users = cursor.fetchall()
    print(f"in conversation user id{user_id}")
    
    return users