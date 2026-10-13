# ExamFlow — Examination Scheduling and Result Processing System

**Project 24 | Database Management Systems | Woxsen University, School of Technology**

A database-backed academic prototype for managing student records, faculty, subjects, examination timetables, room and invigilator allocation, marks, grades, and reports.

## Features
- Dashboard with database-backed summary metrics
- Student, faculty, subject, and room CRUD
- Examination scheduling with room, invigilator, and student-group overlap checks
- Room-capacity validation
- Result entry with marks validation and configurable grade bands
- Searchable records and downloadable CSV reports
- SQLite database initialized automatically on first run
- Parameterized SQL statements and database constraints

## Run locally
Requires Python 3.10 or newer.

```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

The app opens at http://localhost:8501. The database file is created locally as `exam_system.db` and is excluded from Git.

## Repository layout
- `app.py` — Streamlit application
- `schema.sql` — relational schema reference
- `requirements.txt` — Python dependencies
- `presentations/` — Phase 1, Phase 2, and Phase 3 presentation deliverables
- `documentation/` — ERD, testing evidence, demo-video link document
- `report/` — final report deliverables

## Academic integrity and evidence
Sample data is fictional and intended for demonstration. Confirm grading policy and institutional rules with the course faculty. Record test results only after executing the tests; add actual screenshots and final presentation files before submission.

## Project title
Design and Implementation of a Database Management System for Examination Scheduling and Result Processing System.
