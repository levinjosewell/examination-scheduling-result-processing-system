# Phase 1 Presentation — Problem Definition & Conceptual Design

**Project:** Design and Implementation of a Database Management System for Examination Scheduling and Result Processing System  
**Prototype name:** ExamFlow  
**Course:** Database Management Systems  
**Student:** Levin Josewell Kadasi

> This is slide-ready content. Transfer it into the university's required presentation template and add the ER diagram from `documentation/ER_DIAGRAM.mmd`. Update personal/course details as needed.

## Slide 1 — Title
- Design and Implementation of a Database Management System for Examination Scheduling and Result Processing System
- ExamFlow | DBMS Project 24
- Student name, class/section, faculty name, university

## Slide 2 — Background
- Examination administration involves students, subjects, rooms, faculty invigilators, timetables and results.
- Managing these records independently can cause duplication, scheduling clashes and errors in result processing.
- A relational database provides a consistent place to store connected academic records.

## Slide 3 — Problem Statement
- Manual or disconnected records make it difficult to maintain accurate examination information.
- Room and invigilator conflicts may occur when schedules are not checked centrally.
- Result entry requires validation so marks remain within the permitted range.
- The project explores a database-backed system for organizing these operations.

## Slide 4 — Aim and Objectives
**Aim:** Design and implement a relational database-supported application for examination scheduling and result processing.
- Maintain student, faculty, subject and room records.
- Schedule examinations with time-conflict checks.
- Record marks and calculate illustrative grades.
- Produce searchable tables and CSV reports.
- Apply primary keys, foreign keys, uniqueness and validation constraints.

## Slide 5 — Scope
**Included in the prototype**
- Student, faculty, subject and room records
- Examination timetable management
- Invigilator and room conflict checking
- Marks entry, grade calculation and publication status
- Dashboard, database explorer and CSV exports

**Outside the current prototype scope**
- Live integration with university SIS/LMS
- Authentication/role-based permissions
- Email/SMS notifications
- Production deployment and institutional data migration

## Slide 6 — Stakeholders and Requirements
- Administrator/exam coordinator: maintain records and schedule examinations.
- Faculty/invigilator: support exam administration and result entry.
- Academic management: review timetable and result reports.
- Functional requirements: CRUD records, schedule exams, process results, export reports.
- Non-functional requirements: data integrity, understandable interface, repeatable local setup.

## Slide 7 — Proposed System Workflow
1. Register students, faculty, subjects and rooms.
2. Create examination schedules.
3. Validate time ranges and check room/invigilator clashes.
4. Enter marks for students against examinations.
5. Calculate a grade using the prototype's illustrative bands.
6. Review and export timetable/result reports.

## Slide 8 — Conceptual ER Model
Insert `documentation/ER_DIAGRAM.mmd` rendered as an ER diagram.
- Students and exams are linked through Results.
- Each result belongs to one student and one exam.
- Each exam references one subject, one room and one faculty invigilator.
- Primary keys identify rows; foreign keys maintain referential links.

## Slide 9 — Expected Benefits
- Centralized academic records
- Reduced duplicate entries through unique constraints
- Early detection of room/invigilator scheduling conflicts
- Consistent marks validation and result reporting
- Easier inspection and export of data

## Slide 10 — Conclusion and Next Phase
- Phase 1 defines the problem, scope, requirements and conceptual data model.
- Phase 2 will develop the relational schema, keys, normalization and SQL implementation.
- Phase 3 will demonstrate the running prototype and test evidence.

## Presenter notes
Keep slide text concise. Use an ERD visual rather than paragraphs on Slide 8. State that the records are synthetic mock data and that grading thresholds are illustrative until approved by the course faculty.
