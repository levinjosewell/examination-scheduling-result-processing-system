# Mock Database Dataset

This folder contains a deterministic generator for a large, fictional ExamFlow dataset.

## Generate the local SQLite database

From the repository root:

```bash
python database/generate_mock_data.py
```

This creates/replaces `exam_system.db` in the repository root. The generated database is deliberately ignored by Git because it is runtime data; commit the generator and schema, not the mutable database binary.

## Dataset scale

The generator creates:
- 1,200 students
- 60 faculty members
- 180 subjects
- 60 rooms
- Up to 900 exam schedule records, with room/invigilator collision checks during generation
- Thousands of student result records (up to 24 results per non-cancelled exam)

Exact counts are printed when the script runs. The generated data is fictional, deterministic and for academic demonstration only.

## Important note about the current application

The current Streamlit app initializes a small demo database automatically. Run this generator after installing dependencies and before starting the app to replace it with the large dataset. The app must be stopped while regenerating the database. If the application schema and generator schema change later, update both together.

## Privacy and academic honesty

All names, rolls and example.edu addresses are synthetic. Do not describe mock records as real university data.
