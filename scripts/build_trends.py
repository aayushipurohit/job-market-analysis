import pandas as pd
import os
import re
import glob

SNAPSHOTS_DIR = "data/snapshots"
OUTPUT_FILE = "data/skill_trends.csv"

SKILLS = [
    "SQL", "Python", "Excel", "Power BI", "Tableau", "R", "SAS",
    "Java", "Scala", "Spark", "Hadoop", "AWS", "Azure", "GCP",
    "Machine Learning", "Statistics", "A/B Testing", "ETL",
    "Data Visualization", "Looker", "Google Analytics", "VBA",
    "PowerPoint", "NoSQL", "MongoDB", "Snowflake", "Airflow",
    "PostgreSQL", "MySQL", "Git", "Alteryx", "Oracle"
]

def extract_skills(description, skills_list):
    if not isinstance(description, str):
        return []
    found = []
    text = description.lower()
    for skill in skills_list:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text):
            found.append(skill)
    return found


def main():
    snapshot_files = sorted(glob.glob(os.path.join(SNAPSHOTS_DIR, "jobs_*.csv")))

    if not snapshot_files:
        print("No snapshots found yet. Run collect_data.py a few times over different days first.")
        return

    print(f"Found {len(snapshot_files)} snapshot(s): {[os.path.basename(f) for f in snapshot_files]}")

    trend_rows = []

    for file_path in snapshot_files:
        filename = os.path.basename(file_path)
        # filename format: jobs_YYYY-MM-DD.csv
        date_str = filename.replace("jobs_", "").replace(".csv", "")

        df = pd.read_csv(file_path)
        if "description" not in df.columns:
            continue

        total_jobs = len(df)
        skill_counts = {skill: 0 for skill in SKILLS}

        for desc in df["description"]:
            found = extract_skills(desc, SKILLS)
            for skill in found:
                skill_counts[skill] += 1

        for skill, count in skill_counts.items():
            pct = round((count / total_jobs) * 100, 1) if total_jobs > 0 else 0
            trend_rows.append({
                "date": date_str,
                "skill": skill,
                "count": count,
                "total_postings": total_jobs,
                "pct_of_postings": pct
            })

    trend_df = pd.DataFrame(trend_rows)
    trend_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved trend data to {OUTPUT_FILE} ({len(trend_df)} rows)")

    # Print a quick preview: how top skills have moved, if more than 1 date exists
    dates = trend_df["date"].unique()
    if len(dates) > 1:
        print("\nSkill demand change (first snapshot vs latest):")
        first_date, last_date = dates[0], dates[-1]
        pivot = trend_df.pivot(index="skill", columns="date", values="pct_of_postings")
        pivot["change"] = pivot[last_date] - pivot[first_date]
        top_movers = pivot.sort_values("change", ascending=False).head(10)
        print(top_movers[[first_date, last_date, "change"]])
    else:
        print(f"\nOnly one snapshot date so far ({dates[0]}). "
              f"Run collect_data.py again on a later date to start seeing trends.")


if __name__ == "__main__":
    main()