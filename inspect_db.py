import sqlite3

DB_NAME = 'ecom.db'

def inspect_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        table_name = table[0]
        print(f"Table: {table_name}")
        cursor.execute(f'PRAGMA table_info({table_name});')
        columns = cursor.fetchall()
        for col in columns:
            print(f"    {col[1]} ({col[2]})")
        print()
    conn.close()

if __name__ == '__main__':
    inspect_db(DB_NAME) 