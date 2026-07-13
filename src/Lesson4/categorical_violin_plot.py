import pandas as pd

import matplotlib.pyplot as plt

from pathlib import Path

 

 

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

DATA_DIR.mkdir(exist_ok=True)

 

CASES_FILE = PROJECT_ROOT / "data" / "taco_cases.csv"

OUTPUT_FILE = DATA_DIR / "domain_uso_bar_english.png"

SUMMARY_FILE = DATA_DIR / "domain_summary.csv"

 

 

if not CASES_FILE.exists():

    print("Cannot find taco_cases.csv:")

    print(CASES_FILE)

 

else:

    df = pd.read_csv(CASES_FILE, parse_dates=["date"], encoding="utf-8-sig")