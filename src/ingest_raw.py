import pandas as pd
from pathlib import Path
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "raw"
ingest_dttm = datetime.now(timezone.utc)

for file in DATA_DIR.glob("*.csv"):
    #load file to df
    filepath = file.absolute()
    df = pd.read_csv(filepath)
    df["ingest_dttm"] = ingest_dttm

    #establish output paths
    filename = file.stem
    file_date = "-".join(reversed(filename.split(' ')[1].replace('.csv','').split('-')))
    target_s3_folder = f"s3://hospital-inpatients-pipeline/bronze/episodes/snapshot_date={file_date}/episodes.parquet"

    #upload files
    df.to_parquet(    
        target_s3_folder,
        index=False)