import pandas as pd
from pathlib import Path
import pyarrow


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "raw"
 
print(__file__)

date_cols = ["Patient DOB","Episode Start Date","Episode_End_Date","dicharge_dttm","last_updated_ts"]

for file in DATA_DIR.iterdir():
    filepath = file.absolute()
    df = pd.read_csv(filepath)

    for col in date_cols:
        df[col] = pd.to_datetime(df[col],errors='raise')

    print(df.info())
    

    filename = file.name
    file_date = "-".join(reversed(filename.split(' ')[1].replace('.csv','').split('-')))
    target_s3_folder = f"s3://hospital-inpatients-pipeline/bronze/episodes/{file_date}/episodes.parquet"
    df.to_parquet(    
        target_s3_folder,
        index=False)