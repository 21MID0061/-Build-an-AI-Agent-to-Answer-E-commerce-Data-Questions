import os
import pandas as pd
import sqlite3

DATA_DIR = 'data'
DB_NAME = 'ecom.db'

def csvs_to_sqlite(data_dir, db_name):
    conn = sqlite3.connect(db_name)
    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            table_name = os.path.splitext(filename)[0]
            csv_path = os.path.join(data_dir, filename)
            df = pd.read_csv(csv_path)
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"Loaded {filename} into table '{table_name}'")
    conn.close()

if __name__ == '__main__':
    csvs_to_sqlite(DATA_DIR, DB_NAME)
    print('All CSVs loaded into SQLite database.') 