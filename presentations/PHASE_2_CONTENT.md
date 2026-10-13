# Phase 2 Presentation — Logical Database Design & SQL Implementation

## Slide 1 — Title
ExamFlow: Examination Scheduling and Result Processing System — Phase 2

## Slide 2 — From ER Model to Relations
- Students(student_id, roll_number, full_name, email, program, section, semester)
- Faculty(faculty_id, faculty_code, full_name, email, department)
- Subjects(subject_id, subject_code, subject_name, department, semester, credits)
- Rooms(room_id, room_code, building, capacity)
- Exams(exam_id, subject_id, exam_date, start_time, end_time, room_id, invigilator_id, section, max_marks, status)
- Results(result_id, student_id, exam_id, marks_obtained, grade, published)

## Slide 3 — Keys
- Primary keys: each table's *_id field uniquely identifies a row.
- Candidate/unique keys: roll_number, faculty_code, subject_code, room_code and relevant email fields.
- Foreign keys: Exams references Subjects, Rooms and Faculty; Results references Students and Exams.
- Results has a composite business rule enforced by UNIQUE(student_id, exam_id), preventing duplicate result rows for the same student/exam.

## Slide 4 — Integrity Constraints
- NOT NULL ensures required fields are supplied.
- UNIQUE prevents duplicate identifiers.
- CHECK constraints validate semester, credits, capacity, marks sign, status and time order where defined.
- Foreign keys prevent orphaned exam and result records.
- Application-level checks also inspect room/invigilator time overlap before inserting an exam.

## Slide 5 — Normalization
- **1NF:** each field stores one value; no repeating groups.
- **2NF:** tables use single-column surrogate primary keys; non-key fields describe the key entity rather than a partial composite key.
- **3NF:** student, faculty, subject, room, exam and result facts are separated by entity. Subject names are stored in Subjects rather than repeated as exam attributes; room details are stored in Rooms rather than repeated as exam attributes.
- Final normalization claims should be supported by the functional dependencies and schema in the submitted report.

## Slide 6 — SQL Implementation
- CREATE TABLE defines entities and relationships.
- INSERT adds records with bound parameters.
- SELECT with JOIN retrieves timetable and result information.
- UPDATE changes permitted student details.
- DELETE is subject to foreign-key integrity.
- GROUP BY produces summary reports.

## Slide 7 — Relationships
Insert the ER diagram from `documentation/ER_DIAGRAM.mmd`.
- One subject can have multiple exams.
- One room can host many exams at different times.
- One faculty member can invigilate multiple exams at different times.
- One student can have multiple results.
- One exam can produce results for multiple students.

## Slide 8 — Sample Query: Timetable
```sql
SELECT e.exam_date, e.start_time, e.end_time,
       s.subject_code, r.room_code, f.full_name AS invigilator
FROM exams e
JOIN subjects s ON s.subject_id = e.subject_id
JOIN rooms r ON r.room_id = e.room_id
JOIN faculty f ON f.faculty_id = e.invigilator_id
ORDER BY e.exam_date, e.start_time;
```

## Slide 9 — Mock Data
The generator is configured for 1,200 fictional students, 60 faculty, 180 subjects, 60 rooms, up to 900 exam records and thousands of result records. Run it to print actual counts and integrity-check output before reporting exact figures.

## Slide 10 — Transition to Phase 3
Phase 3 will present the working Streamlit application, database-backed operations, validation tests and CSV reports.
