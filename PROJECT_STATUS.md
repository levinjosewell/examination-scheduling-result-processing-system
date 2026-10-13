# ExamFlow — Submission Tracker

Last updated: 13 October 2026

## Current project status

- [x] Streamlit prototype implemented in `app.py`.
- [x] SQLite schema and mock-data generator committed.
- [x] ER diagram and relational-schema diagram source files committed under `documentation/` (check repository for the current filenames).
- [x] Phase 1, Phase 2, and Phase 3 slide content drafts committed under `presentations/`.
- [x] User-reported prototype checks: dashboard/data counts, student creation and persistence, subject insertion compatibility, room-overlap validation, results and CSV export.
- [ ] Final `.pptx` files committed to this repository.
- [ ] Add genuine screenshots from the running application to the presentations and final report.
- [ ] Complete the test plan with outcomes and evidence for every test case.
- [ ] Verify schema, ERD, and normalization claims are consistent, including 3NF.
- [ ] Complete the final report and export a submission-ready copy.
- [ ] Record the five-minute demo and upload it to Google Drive with public-view access.
- [ ] Add the public demo-video URL to `documentation/VIDEO_LINK_TEMPLATE.md`.
- [ ] Final clean-clone test and submission checklist.

## Next tasks — recommended order

### 1. Commit the presentation files
Place the generated presentations in `presentations/` using these names:
- `PHASE_1_Problem_Analysis.pptx`
- `PHASE_2_Database_Design.pptx`
- `PHASE_3_Implementation_and_Demo.pptx`

The files were generated as downloadable artifacts in the conversation, but their binary contents have **not yet been committed to this GitHub repository**.

### 2. Insert genuine application screenshots
Use screenshots captured from the actual running app: dashboard, students, faculty, subjects, rooms, exam scheduling, results, reports/export, and database explorer. Avoid mock or AI-generated screenshots as implementation evidence.

### 3. Finish testing evidence
Update `documentation/TEST_PLAN.md` only with tests actually executed. Capture evidence for duplicate roll numbers, invigilator conflicts, room capacity, invalid marks, duplicate results, and CSV export where applicable.

### 4. Reconcile database design
Check that `schema.sql`, the database created by the app, the ERD, and the report agree on all entities, attributes, PKs, FKs, uniqueness rules, and business constraints. Document any limitations honestly.

### 5. Final report and video
Prepare the report after screenshots and test evidence are ready. Record a concise five-minute walkthrough, upload it to Drive, set access to anyone with the link (if permitted by course policy), and paste the link into the video-link template.

### 6. Final submission audit
- [ ] Repository README has correct setup instructions.
- [ ] App runs from a clean clone.
- [ ] No database files, credentials, or personal data are committed.
- [ ] Three presentations and final report are present.
- [ ] Public video link opens in a private/incognito window.
- [ ] Required hardcopy and submission format confirmed with faculty.

## Evidence note

Prototype checks listed as user-reported are not independently verified by this tracker. Pending tests must not be described as passed until executed.
