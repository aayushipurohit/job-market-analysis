

-- 1. Top skills overall
SELECT s.skill_name, COUNT(*) AS job_count
FROM job_skills js
JOIN skills s ON js.skill_id = s.skill_id
GROUP BY s.skill_name
ORDER BY job_count DESC
LIMIT 10;


-- 2. Top skills by location (e.g. Bangalore, Mumbai, etc.)
SELECT j.location, s.skill_name, COUNT(*) AS job_count
FROM job_skills js
JOIN skills s ON js.skill_id = s.skill_id
JOIN jobs j ON js.job_id = j.job_id
WHERE j.location IS NOT NULL AND j.location != ''
GROUP BY j.location, s.skill_name
ORDER BY j.location, job_count DESC;


-- 3. Which locations have the most job postings overall
SELECT location, COUNT(*) AS num_postings
FROM jobs
WHERE location IS NOT NULL AND location != ''
GROUP BY location
ORDER BY num_postings DESC
LIMIT 10;


-- 4. Which companies are hiring the most Data Analysts
SELECT company, COUNT(*) AS num_postings
FROM jobs
WHERE company IS NOT NULL AND company != ''
GROUP BY company
ORDER BY num_postings DESC
LIMIT 10;


-- 5. Skill co-occurrence: which skill pairs appear together most often
SELECT s1.skill_name AS skill_a, s2.skill_name AS skill_b, COUNT(*) AS times_together
FROM job_skills js1
JOIN job_skills js2 ON js1.job_id = js2.job_id AND js1.skill_id < js2.skill_id
JOIN skills s1 ON js1.skill_id = s1.skill_id
JOIN skills s2 ON js2.skill_id = s2.skill_id
GROUP BY s1.skill_name, s2.skill_name
ORDER BY times_together DESC
LIMIT 10;


-- 6. Average number of skills requested per job posting
SELECT AVG(num_skills) AS avg_skills_per_posting
FROM jobs;


-- 7. Postings with salary info vs without (data completeness check)
SELECT
  SUM(CASE WHEN salary_min IS NOT NULL THEN 1 ELSE 0 END) AS with_salary,
  SUM(CASE WHEN salary_min IS NULL THEN 1 ELSE 0 END) AS without_salary
FROM jobs;


-- 8. Average salary range where available
SELECT
  ROUND(AVG(salary_min), 0) AS avg_salary_min,
  ROUND(AVG(salary_max), 0) AS avg_salary_max
FROM jobs
WHERE salary_min IS NOT NULL AND salary_max IS NOT NULL;