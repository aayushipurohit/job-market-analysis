# 📊 Data Analyst Job Market Analysis

A live, automated pipeline that tracks the Data Analyst job market in India — scraping real job postings, extracting in-demand skills, and visualizing findings through an interactive dashboard.

**Live Dashboard:** *https://job-market-analysis-upnk5jjtfsewswn7mhqiit.streamlit.app/*

---

## Why I Built This

As a final-year student preparing to enter the data analytics job market, I wanted a project that actually answers a question I care about: **what skills should I be learning right now to be competitive?**

Instead of using a static Kaggle dataset, I built a pipeline that pulls **live job postings** from a real job search API, so the analysis reflects the current market rather than a moment frozen in time.

---

## What It Does

1. **Collects** live "Data Analyst" job postings via the Adzuna API
2. **Cleans** the data and extracts mentioned skills from each job description using pattern matching
3. **Stores** everything in a structured SQLite database (`jobs`, `skills`, `job_skills` tables)
4. **Analyzes** the data with SQL to answer:
   - Which skills are most in-demand?
   - Which skills tend to appear together?
   - Where are most jobs located, and who's hiring the most?
   - What's the average salary range where disclosed?
5. **Visualizes** everything in an interactive Streamlit dashboard
6. **Automates** the whole pipeline to run weekly via GitHub Actions, so the data — and the skill demand trend chart — updates on its own over time

---

## Key Findings (from 500 postings analyzed)

| Skill | Postings | % of Jobs |
|---|---|---|
| SQL | 108 | 21.6% |
| Python | 58 | 11.6% |
| Power BI | 43 | 8.6% |
| Excel | 36 | 7.2% |
| Tableau | 30 | 6.0% |

- **SQL appears in nearly 2x as many postings as Python** — the single most consistently requested skill for Data Analyst roles.
- **Power BI + Tableau combined rival Python** in demand, showing that BI tool fluency matters roughly as much as programming ability for this role.
- Only **~22% of postings disclose salary**, a real limitation of the dataset worth noting rather than hiding.
- Where disclosed, average salary ranged from **₹5.8L to ₹11.7L** per year.

---

## Tech Stack

- **Python** (pandas, requests) — data collection & cleaning
- **SQL** (SQLite) — structured storage & analysis queries
- **Streamlit** — interactive dashboard
- **GitHub Actions** — weekly automated data refresh

---

## Project Structure

```
job-market-analysis/
├── data/
│   ├── snapshots/          # dated raw data pulls
│   ├── master_jobs.csv     # all unique jobs collected over time
│   ├── cleaned_jobs.csv    # cleaned data with extracted skills
│   ├── job_market.db       # SQLite database
│   └── skill_trends.csv    # skill demand over time
├── scripts/
│   ├── collect_data.py     # pulls data from Adzuna API
│   ├── clean_data.py       # cleans data & extracts skills
│   ├── build_database.py   # builds the SQLite database
│   ├── run_analysis.py     # runs core SQL analysis queries
│   ├── build_trends.py     # builds skill demand trend data
│   ├── dashboard.py        # Streamlit dashboard
│   └── queries.sql         # raw SQL queries used
├── .github/workflows/
│   └── update_data.yml     # weekly automation
└── README.md
```

---

## Running It Locally

```bash
pip install -r requirements.txt   # or install pandas, requests, streamlit individually

python scripts/collect_data.py    # collect fresh data (needs Adzuna API keys)
python scripts/clean_data.py      # clean & extract skills
python scripts/build_database.py  # build SQL database
python scripts/run_analysis.py    # print analysis results
streamlit run scripts/dashboard.py  # launch the dashboard
```

You'll need your own free Adzuna API credentials — set them as environment variables or in `scripts/collect_data.py`.

---

## What I'd Improve With More Time

- Expand beyond one job title to compare Data Analyst vs. Business Analyst vs. Data Scientist demand
- Use NLP (e.g. spaCy) instead of keyword matching for more robust skill extraction
- Add a simple salary prediction model based on skills and location

---

*Built by Aayushi Purohit — final-year student, data analytics.*
