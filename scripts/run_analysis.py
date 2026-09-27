import sqlite3
import pandas as pd

DB_FILE = "data/job_market.db"

def run_query(conn, title, query):
    print(f"\n{'=' * 60}")
    print(title)
    print('=' * 60)
    df = pd.read_sql_query(query, conn)
    print(df.to_string(index=False))
    return df


def main():
    conn = sqlite3.connect(DB_FILE)

    run_query(conn, "1. Top 10 Skills Overall", """
        SELECT s.skill_name, COUNT(*) AS job_count
        FROM job_skills js
        JOIN skills s ON js.skill_id = s.skill_id
        GROUP BY s.skill_name
        ORDER BY job_count DESC
        LIMIT 10
    """)

    run_query(conn, "2. Top Locations by Number of Postings", """
        SELECT location, COUNT(*) AS num_postings
        FROM jobs
        WHERE location IS NOT NULL AND location != ''
        GROUP BY location
        ORDER BY num_postings DESC
        LIMIT 10
    """)

    run_query(conn, "3. Top Companies Hiring Data Analysts", """
        SELECT company, COUNT(*) AS num_postings
        FROM jobs
        WHERE company IS NOT NULL AND company != ''
        GROUP BY company
        ORDER BY num_postings DESC
        LIMIT 10
    """)

    run_query(conn, "4. Top Skill Pairs (Co-occurrence)", """
        SELECT s1.skill_name AS skill_a, s2.skill_name AS skill_b, COUNT(*) AS times_together
        FROM job_skills js1
        JOIN job_skills js2 ON js1.job_id = js2.job_id AND js1.skill_id < js2.skill_id
        JOIN skills s1 ON js1.skill_id = s1.skill_id
        JOIN skills s2 ON js2.skill_id = s2.skill_id
        GROUP BY s1.skill_name, s2.skill_name
        ORDER BY times_together DESC
        LIMIT 10
    """)

    run_query(conn, "5. Average Skills Requested per Posting", """
        SELECT ROUND(AVG(num_skills), 2) AS avg_skills_per_posting
        FROM jobs
    """)

    run_query(conn, "6. Salary Data Completeness", """
        SELECT
          SUM(CASE WHEN salary_min IS NOT NULL THEN 1 ELSE 0 END) AS with_salary,
          SUM(CASE WHEN salary_min IS NULL THEN 1 ELSE 0 END) AS without_salary
        FROM jobs
    """)

    run_query(conn, "7. Average Salary Range (where available)", """
        SELECT
          ROUND(AVG(salary_min), 0) AS avg_salary_min,
          ROUND(AVG(salary_max), 0) AS avg_salary_max
        FROM jobs
        WHERE salary_min IS NOT NULL AND salary_max IS NOT NULL
    """)

    conn.close()
    print(f"\n{'=' * 60}")
    print("Done. Use these results to write your findings summary.")
    print('=' * 60)


if __name__ == "__main__":
    main()