import requests
import pandas as pd
import time
import os
from datetime import datetime

APP_ID = "7a21a92b"      
APP_KEY = "bde7b8ebf049b032a3fd48c03e8bf28b"   
COUNTRY = "in"                   
WHAT = "data analyst"            
NUM_PAGES = 10                 

def collect_jobs():
    all_jobs = []

    for page in range(1, NUM_PAGES + 1):
        url = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/{page}"
        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "results_per_page": 50,
            "what": WHAT,
            "content-type": "application/json"
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            if not results:
                print(f"No more results at page {page}")
                break
            all_jobs.extend(results)
            print(f"Page {page}: got {len(results)} jobs")
        else:
            print(f"Error on page {page}: {response.status_code}")
            break

        time.sleep(1)

    return pd.json_normalize(all_jobs)


def main():
    os.makedirs("data/snapshots", exist_ok=True)

    df = collect_jobs()
    today = datetime.now().strftime("%Y-%m-%d")
    df["date_collected"] = today

    
    snapshot_path = f"data/snapshots/jobs_{today}.csv"
    df.to_csv(snapshot_path, index=False)
    print(f"Saved snapshot: {snapshot_path} ({len(df)} jobs)")

    # Append to a master file that tracks everything over time
    master_path = "data/master_jobs.csv"
    if os.path.exists(master_path):
        master_df = pd.read_csv(master_path)
        combined = pd.concat([master_df, df], ignore_index=True)
        # Drop exact duplicate postings seen in multiple runs
        combined = combined.drop_duplicates(subset=["id"], keep="last")
    else:
        combined = df

    combined.to_csv(master_path, index=False)
    print(f"Master dataset updated: {master_path} ({len(combined)} total unique jobs)")

    
    with open("data/last_updated.txt", "w") as f:
        f.write(f"{today}\n{len(df)} new postings collected this run\n{len(combined)} total unique jobs tracked")


if __name__ == "__main__":
    main()


































