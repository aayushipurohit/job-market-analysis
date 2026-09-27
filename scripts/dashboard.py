import streamlit as st
import pandas as pd
import sqlite3
import os

DB_FILE = "data/job_market.db"
TRENDS_FILE = "data/skill_trends.csv"

st.set_page_config(page_title="Data Analyst Job Market Dashboard", layout="wide")

st.title("📊 Data Analyst Job Market Dashboard")
st.caption("Live analysis of real job postings scraped from Adzuna")

# Show last updated info if available
status_file = "data/last_updated.txt"
if os.path.exists(status_file):
    with open(status_file) as f:
        st.info(f.read().replace("\n", " | "))

conn = sqlite3.connect(DB_FILE)

# ---- Top skills ----
st.header("Most In-Demand Skills")
skills_df = pd.read_sql_query("""
    SELECT s.skill_name AS Skill, COUNT(*) AS Postings
    FROM job_skills js
    JOIN skills s ON js.skill_id = s.skill_id
    GROUP BY s.skill_name
    ORDER BY Postings DESC
    LIMIT 15
""", conn)

col1, col2 = st.columns([2, 1])
with col1:
    st.bar_chart(skills_df.set_index("Skill"))
with col2:
    st.dataframe(skills_df, hide_index=True, use_container_width=True)

# ---- NEW: Skill demand trend over time ----
st.header("📈 Skill Demand Trend Over Time")
if os.path.exists(TRENDS_FILE):
    trends_df = pd.read_csv(TRENDS_FILE)
    dates_available = sorted(trends_df["date"].unique())

    if len(dates_available) > 1:
        # Let user pick which skills to compare
        top_skills_list = skills_df["Skill"].tolist()
        default_selection = top_skills_list[:5] if len(top_skills_list) >= 5 else top_skills_list

        selected_skills = st.multiselect(
            "Select skills to compare",
            options=sorted(trends_df["skill"].unique()),
            default=default_selection
        )

        if selected_skills:
            filtered = trends_df[trends_df["skill"].isin(selected_skills)]
            pivot = filtered.pivot(index="date", columns="skill", values="pct_of_postings")
            st.line_chart(pivot)
            st.caption("Values shown as % of job postings mentioning each skill, by collection date")
        else:
            st.write("Select at least one skill above to see its trend.")
    else:
        st.info(
            f"Only one data collection so far ({dates_available[0]}). "
            "Trends will appear automatically once the pipeline runs again on a later date "
            "(this happens weekly via the GitHub Actions automation)."
        )
else:
    st.info("Trend data not generated yet. Run `scripts/build_trends.py` to build it.")

# ---- Top locations ----
st.header("Top Locations by Postings")
locations_df = pd.read_sql_query("""
    SELECT location AS Location, COUNT(*) AS Postings
    FROM jobs
    WHERE location IS NOT NULL AND location != ''
    GROUP BY location
    ORDER BY Postings DESC
    LIMIT 10
""", conn)
st.bar_chart(locations_df.set_index("Location"))

# ---- Top companies ----
st.header("Top Hiring Companies")
companies_df = pd.read_sql_query("""
    SELECT company AS Company, COUNT(*) AS Postings
    FROM jobs
    WHERE company IS NOT NULL AND company != ''
    GROUP BY company
    ORDER BY Postings DESC
    LIMIT 10
""", conn)
st.dataframe(companies_df, hide_index=True, use_container_width=True)


st.header("Skills That Appear Together Most Often")
pairs_df = pd.read_sql_query("""
    SELECT s1.skill_name AS "Skill A", s2.skill_name AS "Skill B", COUNT(*) AS "Times Together"
    FROM job_skills js1
    JOIN job_skills js2 ON js1.job_id = js2.job_id AND js1.skill_id < js2.skill_id
    JOIN skills s1 ON js1.skill_id = s1.skill_id
    JOIN skills s2 ON js2.skill_id = s2.skill_id
    GROUP BY s1.skill_name, s2.skill_name
    ORDER BY "Times Together" DESC
    LIMIT 10
""", conn)
st.dataframe(pairs_df, hide_index=True, use_container_width=True)


st.header("Salary Overview")
salary_df = pd.read_sql_query("""
    SELECT
      ROUND(AVG(salary_min), 0) AS avg_min,
      ROUND(AVG(salary_max), 0) AS avg_max,
      SUM(CASE WHEN salary_min IS NOT NULL THEN 1 ELSE 0 END) AS with_salary,
      COUNT(*) AS total
    FROM jobs
""", conn)
row = salary_df.iloc[0]
c1, c2, c3 = st.columns(3)
c1.metric("Avg Min Salary", f"₹{row['avg_min']:,.0f}")
c2.metric("Avg Max Salary", f"₹{row['avg_max']:,.0f}")
c3.metric("Postings w/ Salary Disclosed", f"{int(row['with_salary'])}/{int(row['total'])}")

with st.expander("🔍 Explore raw job postings"):
    raw_df = pd.read_sql_query("""
        SELECT title, company, location, salary_min, salary_max, num_skills
        FROM jobs
        ORDER BY job_id DESC
        LIMIT 100
    """, conn)
    st.dataframe(raw_df, hide_index=True, use_container_width=True)

conn.close()

st.caption("Built with Python, SQL, and Streamlit · Data source: Adzuna API")