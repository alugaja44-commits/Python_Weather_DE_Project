import pandas as pd
import sqlite3
from pathlib import Path

SILVER_DIR=Path("data/silver")
DB_PATH=Path("database/weather.db")

def load_latest_csv_sqlite():
    DB_PATH.parent.mkdir(parents=True,exist_ok=True)
    csv_files=list(SILVER_DIR.glob("*.csv"))
    if not csv_files:
        print("csv files not found")
        return
    latest_file=max(csv_files,key=lambda f:f.stat().st_mtime)
    print(f"using file {latest_file}")

    df=pd.read_csv(latest_file)
    df=df.drop_duplicates()

    conn=sqlite3.connect(DB_PATH)

    try:
        conn.execute("""CREATE TABLE IF NOT EXISTS weather(
                     timestamp TEXT,
                     temp Real,
                     city TEXT)
                     """)
        df.to_sql("weather",conn,if_exists="append",index=False)

        print(f"rows inserted {len(df)}")
        result=pd.read_sql("SELECT COUNT(*) as count FROM weather",conn)
        print(f"total rows in table {result['count'][0]}")

    except Exception as e:
        print(f"error {e}")
    finally:
        conn.close()
        print("DB connection closed")

if __name__=="__main__":
    print("loading csv to sqlite")
    load_latest_csv_sqlite()









