import pandas as pd
import re

INPUT_FILE = "data/master_jobs.csv"
OUTPUT_FILE = "data/cleaned_jobs.csv"


SKILLS = [
    "SQL", "Python", "Excel", "Power BI", "Tableau", "R", "SAS",
    "Java", "Scala", "Spark", "Hadoop", "AWS", "Azure", "GCP",
    "Machine Learning", "Statistics", "A/B Testing", "ETL",
    "Data Visualization", "Looker", "Google Analytics", "VBA",
    "PowerPoint", "NoSQL", "MongoDB", "Snowflake", "Airflow",
    "PostgreSQL", "MySQL", "Git", "Alteryx", "Oracle"
]

def extract_skills(description, skills_list):
    """Return a list of skills found in the description text."""
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
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} rows")

    
    df = df.dropna(subset=["description", "title"])

    
    if "id" in df.columns:
        df = df.drop_duplicates(subset=["id"], keep="last")

   
    df["title"] = df["title"].astype(str).str.strip()

    
    if "company.display_name" in df.columns:
        df["company"] = df["company.display_name"]
    else:
        df["company"] = "Unknown"

   
    if "location.display_name" in df.columns:
        df["location"] = df["location.display_name"]
    else:
        df["location"] = "Unknown"

    
    for col in ["salary_min", "salary_max"]:
        if col not in df.columns:
            df[col] = None

    
    df["skills_found"] = df["description"].apply(lambda d: extract_skills(d, SKILLS))
    df["num_skills"] = df["skills_found"].apply(len)
    df["skills_found_str"] = df["skills_found"].apply(lambda s: ", ".join(s))

    
    keep_cols = [
        "date_collected", "title", "company", "location",
        "salary_min", "salary_max", "created",
        "skills_found_str", "num_skills", "description"
    ]
    keep_cols = [c for c in keep_cols if c in df.columns]
    cleaned = df[keep_cols]

    cleaned.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved cleaned data to {OUTPUT_FILE} ({len(cleaned)} rows)")

    
    all_skills = [s for row in df["skills_found"] for s in row]
    skill_counts = pd.Series(all_skills).value_counts()
    print("\nTop skills mentioned:")
    print(skill_counts.head(15))


if __name__ == "__main__":
    main()