import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "raw"
 
print(__file__)

for file in DATA_DIR.iterdir():
    filepath = file.absolute()
    df = pd.read_csv(filepath)
    # print(df)
    print(df)
