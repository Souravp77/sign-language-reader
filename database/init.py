from .connection import get_db_connection

def init_database():
    """Initialize database with required data"""
    conn = get_db_connection()
    if not conn:
        print("❌ Failed to connect to database")
        return False
    
    cursor = conn.cursor()
    
    try:
        print("📊 Checking and inserting default categories...")
        
        cursor.execute("SELECT COUNT(*) FROM categories WHERE user_id IS NULL")
        count = cursor.fetchone()[0]
        
        if count == 0:
            default_categories = [
                ('Food & Dining', 'expense'),
                ('Transportation', 'expense'),
                ('Shopping', 'expense'),
                ('Entertainment', 'expense'),
                ('Bills & Utilities', 'expense'),
                ('Healthcare', 'expense'),
                ('Education', 'expense'),
                ('Rent/Mortgage', 'expense'),
                ('Travel', 'expense'),
                ('Gifts & Donations', 'expense'),
                ('Insurance', 'expense'),
                ('Other Expenses', 'expense'),
                ('Salary', 'income'),
                ('Freelance', 'income'),
                ('Business Income', 'income'),
                ('Investments', 'income'),
                ('Gifts Received', 'income'),
                ('Rental Income', 'income'),
                ('Refunds', 'income'),
                ('Other Income', 'income')
            ]
            
            sql = "INSERT INTO categories (category_name, type) VALUES (%s, %s)"
            cursor.executemany(sql, default_categories)
            conn.commit()
            print(f"✅ Inserted {len(default_categories)} default categories")
        else:
            print("✅ Default categories already exist")
        
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        if user_count == 0:
            print("👤 Creating a test user...")
            test_user_sql = """
            INSERT INTO users (username, email, password_hash) 
            VALUES (%s, %s, %s)
            """
            cursor.execute(test_user_sql, ('Test User', 'test@example.com', 'test123'))
            conn.commit()
            print("✅ Created test user (email: test@example.com, password: test123)")
        
        print("🎉 Database initialization complete!")
        return True
        
    except Error as e:
        print(f"❌ Error during database initialization: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()