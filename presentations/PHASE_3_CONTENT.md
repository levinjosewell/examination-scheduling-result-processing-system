# Phase 3 Presentation — Prototype, Testing & Results

## Slide 1 — Title
ExamFlow: Examination Scheduling and Result Processing System — Phase 3

## Slide 2 — Application Architecture
- Front end: Streamlit interactive web interface.
- Application logic: Python.
- Database engine: SQLite.
- Data analysis/export: pandas and CSV.
- Local runtime database: exam_system.db, generated from the committed mock-data script.

## Slide 3 — Dashboard
Add a genuine screenshot of the running dashboard.
Explain the database-backed summary counts and timetable view. Record the actual counts shown by the current generated database.

## Slide 4 — Academic Record Management
Add genuine screenshots of Students, Faculty, Subjects and Rooms pages.
Explain record insertion and student update/delete behavior. Show that the database retains valid records after refresh/restart.

## Slide 5 — Examination Scheduling
Add genuine screenshot of the schedule form and timetable.
Explain start/end-time validation and overlapping room/invigilator checks. Do not claim the room-capacity rule is complete until it is implemented and tested against the relevant cohort size.

## Slide 6 — Result Processing
Add genuine screenshot of marks entry and results table.
Explain the marks range, illustrative grade calculation, draft/published flag and duplicate-result prevention.

## Slide 7 — Reports and Database Explorer
Add genuine screenshots of CSV export and read-only table explorer.
Describe timetable, results register, student-count, room-utilisation and pass/fail reports.

## Slide 8 — Testing Evidence
The developer/user-reported checks currently marked as passed are:
- Dashboard and large dataset counts
- Add student and persistence
- Add subject compatibility
- Overlapping room scheduling validation
- Results and CSV exports

Add dated screenshots or reproducible steps for each check. These are user-reported outcomes; attach evidence captured during actual testing. Do not claim independent automated test execution unless performed.

## Slide 9 — Limitations and Future Work
- Validate room capacity against the number of students in the exam section.
- Enforce maximum marks at database level and across every write path.
- Add authentication and role-based permissions.
- Confirm grade bands with faculty.
- Consider migration to MySQL/PostgreSQL if required by the course.
- Add automated unit/integration tests and backup/export procedures.

## Slide 10 — Conclusion
- Demonstrated a local relational database-backed prototype.
- Connected academic entities through primary and foreign keys.
- Implemented schedule-conflict checks, result entry and CSV reporting.
- Future work focuses on stronger validation, security, tests and institutional deployment.

## Video demonstration flow (approximately 5 minutes)
- 0:00–0:25 — Project title and problem
- 0:25–1:00 — Dashboard and dataset scale
- 1:00–1:40 — Students/subjects/rooms management
- 1:40–2:30 — Schedule an exam and demonstrate conflict rejection
- 2:30–3:20 — Enter marks and show grade/result
- 3:20–4:00 — Reports and CSV export
- 4:00–4:35 — Database tables/ER model and constraints
- 4:35–5:00 — Results, limitations and conclusion
