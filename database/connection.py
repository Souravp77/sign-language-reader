import mysql.connector
from mysql.connector import Error
from config import Config

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def test_connection():
    """Test if database connection works"""
    conn = get_db_connection()
    if conn:
        conn.close()
        return True
    return False