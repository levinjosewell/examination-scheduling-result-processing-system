# Test Plan

Record actual outcomes only after running the prototype. Keep screenshots or query output as evidence. The following five checks were reported by the project owner as passed; remaining cases are still pending independent evidence.

| ID | Scenario | Expected outcome | Actual outcome / status |
|---|---|---|---|
| TC-01 | Dashboard loads and large mock dataset counts display | Dashboard metrics load from database | Reported passed by project owner; evidence to attach |
| TC-02 | Add a student with valid unique roll number and verify persistence | Student is saved and remains after refresh | Reported passed by project owner; evidence to attach |
| TC-03 | Add a subject using the generated mock-data schema | Subject is saved without schema compatibility error | Reported passed by project owner; evidence to attach |
| TC-04 | Schedule overlapping exams in the same room | Conflict is rejected | Reported passed by project owner; evidence to attach |
| TC-05 | Enter results and export a CSV report | Results save and CSV download is generated | Reported passed by project owner; evidence to attach |
| TC-06 | Add a duplicate roll number | Duplicate is rejected | Pending execution |
| TC-07 | Schedule an exam in a room whose capacity is insufficient | Schedule is rejected | Pending execution |
| TC-08 | Assign one invigilator to overlapping exams | Conflict is rejected | Pending execution |
| TC-09 | Enter marks below zero or above maximum marks | Invalid marks are rejected | Pending execution |
| TC-10 | Enter the same student/exam result twice | Duplicate result is rejected | Pending execution |

**Evidence status:** No screenshots or logs have yet been attached to this test plan. “Reported passed” means the project owner stated that the check worked; it is not independent verification.
