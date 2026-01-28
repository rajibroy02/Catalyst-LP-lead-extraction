# Lead Extraction & Qualification Pipeline

## Overview

This project is a production-oriented data extraction and qualification pipeline built to identify high-intent, senior decision-makers from dynamically rendered web sources. It reliably converts JavaScript-heavy pages into a clean, structured, and outreach-ready lead dataset by combining automated scraping with multi-stage filtering logic.

The system prioritizes **precision, role relevance, and data quality over raw volume**, making it suitable for real-world sales, partnerships, and marketing workflows.

---

## What This Pipeline Does

- Extracts profiles from dynamically loaded web pages (infinite scroll, JS-rendered DOMs)
- Converts unstructured page text into structured lead records
- Eliminates duplicates, malformed entries, and low-signal data
- Applies strict seniority qualification (SVP+ and C-level)
- Outputs a clean, production-ready CSV for downstream use

---

## Pipeline Stages

### 1. Dynamic Extraction

- Renders JavaScript-heavy pages using Selenium
- Handles lazy loading via controlled scrolling
- Performs full-page text extraction
- Heuristically parses names, roles, and organizations

**Output:** Raw, high-recall lead list

---

### 2. Baseline Cleaning

- Removes obvious noise and malformed rows
- Filters out former or inactive roles
- Drops broken or ambiguous domains
- Removes academic and non-operational titles

**Goal:** Data hygiene without over-filtering

---

### 3. Seniority Qualification

- Enforces SVP / EVP / C-level / President / Founder roles only
- Explicitly removes Directors, Heads, Advisors, Consultants, and standard VPs
- Designed to favor decision-makers over influencers

**Goal:** High-intent leadership focus

---

### 4. Production Hardening

- Applies industrial blocklists for titles and domains
- Removes consulting, advisory, and non-operating entities
- Normalizes schema and column order
- Adds fields required for operational workflows

**Final Output:** Outreach-ready lead dataset

---

## Tech Stack

- Python
- Selenium WebDriver
- Pandas
- Regex-based parsing
- Chrome WebDriver

---

## Project Structure

├── 1_Stage2_scraping_script.py
├── 2_catalystLPs_secondScreening_script.py
├── 3_strict_cleaner.py
├── 4_final.py
├── stage2_final_list.csv
├── catalyst_lps_final_submission.csv
├── catalyst_lps_strict_final.csv
├── catalyst_lps_ready_for_production.csv
└── README.md

---

## Running the Pipeline

### Requirements

- Python 3.9+
- Google Chrome
- Compatible ChromeDriver in PATH

---

### Install Dependencies

```bash
pip install selenium pandas
```
---

### Run Sequentially

```bash
python 1_Stage2_scraping_script.py
python 2_catalystLPs_secondScreening_script.py
python 3_strict_cleaner.py
python 4_final.py
```
---

### Final Output Schema
| Column Name     | Description                  |
| --------------- | ---------------------------- |
| first_name      | First name                   |
| last_name       | Last name                    |
| company_domain  | Normalized company domain    |
| title           | Current senior role          |
| source_of_truth | Verification source          |
| notes           | Reserved for ops annotations |

---

### Future Improvements
- ML-based role classification
- Pipeline orchestration (Airflow / Perfect)

---

### Disclaimer
This project is intended for **educational, research and internal data processing purposes only**. Ensure compliance with applicable terms of service and data usage policies when deploying or extending this pipeline.
