import pandas as pd
import sqlite3

INPUT_FILE = "data/cleaned_jobs.csv"
DB_FILE = "data/job_market.db"

def main():
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} cleaned job rows")

    
    df = df.reset_index(drop=True)
    df["job_id"] = df.index + 1

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    
    cursor.execute("DROP TABLE IF EXISTS jobs")
    cursor.execute("""
        CREATE TABLE jobs (
            job_id INTEGER PRIMARY KEY,
            date_collected TEXT,
            title TEXT,
            company TEXT,
            location TEXT,
            salary_min REAL,
            salary_max REAL,
            created TEXT,
            num_skills INTEGER
        )
    """)

    jobs_cols = ["job_id", "date_collected", "title", "company", "location",
                 "salary_min", "salary_max", "created", "num_skills"]
    jobs_cols = [c for c in jobs_cols if c in df.columns]
    df[jobs_cols].to_sql("jobs", conn, if_exists="append", index=False)

    
    all_skills = set()
    for s in df["skills_found_str"].fillna(""):
        for skill in s.split(","):
            skill = skill.strip()
            if skill:
                all_skills.add(skill)

    cursor.execute("DROP TABLE IF EXISTS skills")
    cursor.execute("""
        CREATE TABLE skills (
            skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT UNIQUE
        )
    """)
    for skill in sorted(all_skills):
        cursor.execute("INSERT INTO skills (skill_name) VALUES (?)", (skill,))
    conn.commit()

    
    cursor.execute("SELECT skill_id, skill_name FROM skills")
    skill_id_map = {name: sid for sid, name in cursor.fetchall()}

    
    cursor.execute("DROP TABLE IF EXISTS job_skills")
    cursor.execute("""
        CREATE TABLE job_skills (
            job_id INTEGER,
            skill_id INTEGER,
            FOREIGN KEY (job_id) REFERENCES jobs(job_id),
            FOREIGN KEY (skill_id) REFERENCES skills(skill_id)
        )
    """)

    rows_to_insert = []
    for _, row in df.iterrows():
        job_id = row["job_id"]
        skills_str = row.get("skills_found_str", "")
        if isinstance(skills_str, str) and skills_str.strip():
            for skill in skills_str.split(","):
                skill = skill.strip()
                if skill in skill_id_map:
                    rows_to_insert.append((job_id, skill_id_map[skill]))

    cursor.executemany(
        "INSERT INTO job_skills (job_id, skill_id) VALUES (?, ?)",
        rows_to_insert
    )
    conn.commit()

    print(f"Database built: {DB_FILE}")
    print(f"  jobs table: {len(df)} rows")
    print(f"  skills table: {len(all_skills)} unique skills")
    print(f"  job_skills table: {len(rows_to_insert)} skill mentions")

    # ---- Quick sanity check query ----
    print("\nTop 10 skills by number of job postings:")
    cursor.execute("""
        SELECT s.skill_name, COUNT(*) AS job_count
        FROM job_skills js
        JOIN skills s ON js.skill_id = s.skill_id
        GROUP BY s.skill_name
        ORDER BY job_count DESC
        LIMIT 10
    """)
    for skill_name, count in cursor.fetchall():
        print(f"  {skill_name}: {count}")

    conn.close()


if __name__ == "__main__":
    main()