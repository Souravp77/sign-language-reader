from .connection import get_db_connection

def execute_query(query, params=None, fetch=False, fetch_one=False):
    """
    Universal function to execute database queries
    """
    conn = get_db_connection()
    if not conn:
        return None
    
    cursor = conn.cursor(dictionary=True)
    result = None
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            result = cursor.fetchall()
        elif fetch_one:
            result = cursor.fetchone()
        else:
            conn.commit()
            result = cursor.lastrowid
        
        return result
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()