#!/usr/bin/env python3
"""Generate a large, deterministic fictional ExamFlow SQLite database.

Usage from repository root:
    python database/generate_mock_data.py

Creates/overwrites ./exam_system.db with fictional records. This generated database
is local runtime data and should not be committed to Git; the generator is committed.
"""
from pathlib import Path
import random
import sqlite3
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "exam_system.db"
random.seed(2401)

FIRST = ["Aarav","Aditi","Aditya","Akash","Ananya","Arjun","Avni","Diya","Ishaan","Ira","Kabir","Kavya","Krishna","Maya","Meera","Neha","Nikhil","Priya","Rahul","Riya","Rohan","Saanvi","Sahil","Sai","Sana","Tanvi","Varun","Ved","Vihaan","Zoya","Karthik","Harini","Manav","Pooja","Reyansh","Shreya","Vikram","Yash","Anika","Dev"]
LAST = ["Sharma","Reddy","Rao","Patel","Verma","Nair","Iyer","Khan","Gupta","Joshi","Das","Kapoor","Mehta","Singh","Menon","Chowdhury","Kulkarni","Naidu","Pillai","Bose","Shetty","Mishra","Jain","Fernandes","Thomas"]
DEPARTMENTS = ["Computer Science","Artificial Intelligence","Mathematics","Physics","Electronics","Humanities","Management"]
PROGRAMS = ["B.Tech AI & ML","B.Tech CSE","B.Tech ECE","BBA","BCA","M.Tech AI"]
SECTIONS = ["Rhinos","Falcons","Titans","Panthers","Wolves","Eagles","Phoenix","Cobras","Sharks","Tigers"]
SUBJECTS = [
 ("DBMS","Database Management Systems","Computer Science",4),
 ("DSA","Data Structures and Algorithms","Computer Science",4),
 ("OOPJ","Object-Oriented Programming with Java","Computer Science",3),
 ("COA","Computer Organization and Architecture","Computer Science",3),
 ("DM","Discrete Mathematics","Mathematics",4),
 ("DAA","Design and Analysis of Algorithms","Computer Science",4),
 ("OS","Operating Systems","Computer Science",4),
 ("CN","Computer Networks","Computer Science",3),
 ("AI","Artificial Intelligence","Artificial Intelligence",4),
 ("ML","Machine Learning","Artificial Intelligence",4),
 ("PY","Programming with Python","Computer Science",3),
 ("STAT","Probability and Statistics","Mathematics",3),
 ("LA","Linear Algebra","Mathematics",3),
 ("DE","Digital Electronics","Electronics",3),
 ("IOT","Internet of Things","Electronics",3),
 ("SE","Software Engineering","Computer Science",3),
 ("WT","Web Technologies","Computer Science",3),
 ("CY","Cybersecurity Fundamentals","Computer Science",3),
 ("NLP","Natural Language Processing","Artificial Intelligence",3),
 ("CV","Computer Vision","Artificial Intelligence",3),
 ("DBS","Database Systems Lab","Computer Science",2),
 ("DSAL","Data Structures Lab","Computer Science",2),
 ("JAVA","Java Programming Lab","Computer Science",2),
 ("AIML","AI and ML Lab","Artificial Intelligence",2),
 ("ENG","Technical Communication","Humanities",2),
 ("ETH","Professional Ethics","Humanities",2),
 ("ECON","Engineering Economics","Management",3),
 ("CLOUD","Cloud Computing","Computer Science",3),
 ("BIGDATA","Big Data Analytics","Computer Science",3),
 ("ROBOT","Robotics Fundamentals","Artificial Intelligence",3),
]

def person():
    return f"{random.choice(FIRST)} {random.choice(LAST)}"

def main():
    if DB_PATH.exists():
        DB_PATH.unlink()
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys=ON")
    con.executescript("""
    CREATE TABLE students(
      student_id INTEGER PRIMARY KEY AUTOINCREMENT, roll_number TEXT NOT NULL UNIQUE,
      full_name TEXT NOT NULL, email TEXT UNIQUE, program TEXT NOT NULL,
      section TEXT NOT NULL, semester INTEGER NOT NULL CHECK(semester BETWEEN 1 AND 12));
    CREATE TABLE faculty(
      faculty_id INTEGER PRIMARY KEY AUTOINCREMENT, faculty_code TEXT NOT NULL UNIQUE,
      full_name TEXT NOT NULL, email TEXT UNIQUE, department TEXT NOT NULL);
    CREATE TABLE subjects(
      subject_id INTEGER PRIMARY KEY AUTOINCREMENT, subject_code TEXT NOT NULL UNIQUE,
      subject_name TEXT NOT NULL, department TEXT NOT NULL, semester INTEGER NOT NULL CHECK(semester BETWEEN 1 AND 12),
      credits INTEGER NOT NULL CHECK(credits BETWEEN 1 AND 10));
    CREATE TABLE rooms(
      room_id INTEGER PRIMARY KEY AUTOINCREMENT, room_code TEXT NOT NULL UNIQUE,
      building TEXT NOT NULL, capacity INTEGER NOT NULL CHECK(capacity > 0));
    CREATE TABLE exams(
      exam_id INTEGER PRIMARY KEY AUTOINCREMENT, subject_id INTEGER NOT NULL REFERENCES subjects(subject_id),
      exam_date TEXT NOT NULL, start_time TEXT NOT NULL, end_time TEXT NOT NULL,
      room_id INTEGER NOT NULL REFERENCES rooms(room_id), invigilator_id INTEGER NOT NULL REFERENCES faculty(faculty_id),
      section TEXT NOT NULL, max_marks REAL NOT NULL DEFAULT 100 CHECK(max_marks > 0),
      status TEXT NOT NULL CHECK(status IN ('Scheduled','Completed','Cancelled')),
      CHECK(start_time < end_time));
    CREATE TABLE results(
      result_id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL REFERENCES students(student_id),
      exam_id INTEGER NOT NULL REFERENCES exams(exam_id), marks_obtained REAL NOT NULL CHECK(marks_obtained >= 0),
      grade TEXT NOT NULL, published INTEGER NOT NULL DEFAULT 0 CHECK(published IN (0,1)),
      UNIQUE(student_id, exam_id));
    CREATE INDEX idx_exams_date ON exams(exam_date);
    CREATE INDEX idx_results_student ON results(student_id);
    CREATE INDEX idx_students_section ON students(section, semester);
    """)
    cur = con.cursor()

    # 1,200 fictional students: 6 programs x 10 sections x 20 students on average.
    for i in range(1, 1201):
        full = person()
        section = SECTIONS[((i-1)//20) % len(SECTIONS)]
        semester = ((i-1)//200) % 8 + 1
        cur.execute("INSERT INTO students(roll_number,full_name,email,program,section,semester) VALUES(?,?,?,?,?,?)",
                    (f"STU{i:04d}", full, f"student{i:04d}@example.edu", PROGRAMS[(i-1)%len(PROGRAMS)], section, semester))

    for i in range(1, 61):
        cur.execute("INSERT INTO faculty(faculty_code,full_name,email,department) VALUES(?,?,?,?)",
                    (f"FAC{i:03d}", person(), f"faculty{i:03d}@example.edu", DEPARTMENTS[(i-1)%len(DEPARTMENTS)]))

    for i in range(1, 181):
        base = SUBJECTS[(i-1)%len(SUBJECTS)]
        code = base[0] if i <= len(SUBJECTS) else f"{base[0]}{(i-1)//len(SUBJECTS)+1}"
        cur.execute("INSERT INTO subjects(subject_code,subject_name,department,semester,credits) VALUES(?,?,?,?,?)",
                    (code, base[1], base[2], (i-1)%8+1, base[3]))

    for i in range(1, 61):
        cap = random.choice([30, 40, 50, 60, 80, 100, 120])
        cur.execute("INSERT INTO rooms(room_code,building,capacity) VALUES(?,?,?)",
                    (f"{random.choice(['A','B','C','D'])}-{100+i}", f"Academic Block {random.choice(['A','B','C','D'])}", cap))

    con.commit()
    students = cur.execute("SELECT student_id,section,semester FROM students").fetchall()
    subjects = cur.execute("SELECT subject_id,semester FROM subjects").fetchall()
    rooms = cur.execute("SELECT room_id,capacity FROM rooms").fetchall()
    faculty = [r[0] for r in cur.execute("SELECT faculty_id FROM faculty").fetchall()]

    # Exams use non-overlapping fixed slots for each room and invigilator on a given day.
    dates = [date.today() + timedelta(days=offset) for offset in range(-120, 240)]
    slots = [("09:00","11:00"),("11:30","13:30"),("14:00","16:00")]
    used_room = set()
    used_faculty = set()
    exam_rows = []
    attempts = 0
    while len(exam_rows) < 900 and attempts < 50000:
        attempts += 1
        d = random.choice(dates).isoformat()
        slot_idx = random.randrange(len(slots))
        start, end = slots[slot_idx]
        room_id, cap = random.choice(rooms)
        faculty_id = random.choice(faculty)
        if (d, slot_idx, room_id) in used_room or (d, slot_idx, faculty_id) in used_faculty:
            continue
        section = random.choice(SECTIONS)
        # A section's typical cohort is ~120; choose rooms that can hold a full section.
        if cap < 30:
            continue
        subject_id, sem = random.choice(subjects)
        status = random.choices(["Completed","Scheduled","Cancelled"], weights=[65,32,3])[0]
        cur.execute("""INSERT INTO exams(subject_id,exam_date,start_time,end_time,room_id,invigilator_id,section,max_marks,status)
                       VALUES(?,?,?,?,?,?,?,?,?)""",
                    (subject_id,d,start,end,room_id,faculty_id,section,100.0,status))
        exam_rows.append((cur.lastrowid, section, sem, 100.0, status))
        used_room.add((d, slot_idx, room_id))
        used_faculty.add((d, slot_idx, faculty_id))

    # Results: up to 24 students per exam, section-matched and unique per exam.
    for exam_id, section, sem, maximum, status in exam_rows:
        if status == "Cancelled":
            continue
        candidates = [s[0] for s in students if s[1] == section and s[2] == sem]
        if not candidates:
            candidates = [s[0] for s in students if s[1] == section]
        random.shuffle(candidates)
        for student_id in candidates[:min(24, len(candidates))]:
            marks = round(random.triangular(18, 100, 72), 1)
            pct = marks / maximum * 100
            grade = "A+" if pct >= 90 else "A" if pct >= 80 else "B" if pct >= 70 else "C" if pct >= 60 else "D" if pct >= 40 else "F"
            cur.execute("INSERT INTO results(student_id,exam_id,marks_obtained,grade,published) VALUES(?,?,?,?,?)",
                        (student_id, exam_id, marks, grade, int(status == "Completed")))

    con.commit()
    counts = {table: cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
              for table in ["students","faculty","subjects","rooms","exams","results"]}
    integrity = cur.execute("PRAGMA integrity_check").fetchone()[0]
    con.close()
    print(f"Created {DB_PATH}")
    print("Row counts:")
    for table, count in counts.items():
        print(f"  {table}: {count:,}")
    print(f"SQLite integrity_check: {integrity}")
    print("All names and email addresses are fictional example data.")
    print("NOTE: this database is local runtime data; do not commit exam_system.db.")

if __name__ == "__main__":
    main()
