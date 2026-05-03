import pandas as pd
from pathlib import Path

def csv_to_parquet():
    SILVER_DIR=Path("data/silver")
    GOLD_DIR=Path("data/gold")

    GOLD_DIR.mkdir(parents=True,exist_ok=True)

    csv_files=list(SILVER_DIR.glob("*.csv"))


    if not csv_files:
        print("no CSV files found in silver layer")
        return
    
    for csv_path in csv_files:
        try:
            df=pd.read_csv(csv_path)

            parquet_path=GOLD_DIR/(csv_path.stem+".parquet")
            df.to_parquet(parquet_path,index=False)

            print(f"Ok {csv_path.name} to {parquet_path}")
        except Exception as e:
            print(f"Error Failed due to {e}")


def main():
    print("converting csv to parquet")
    csv_to_parquet()



if __name__=="__main__":
    main()
                  