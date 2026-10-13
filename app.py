import sqlite3
from pathlib import Path
from datetime import date
import pandas as pd
import streamlit as st

DB = Path(__file__).with_name("exam_system.db")
st.set_page_config(page_title="ExamFlow | DBMS Project 24", page_icon="🎓", layout="wide")

SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS students(
 student_id INTEGER PRIMARY KEY AUTOINCREMENT, roll_number TEXT NOT NULL UNIQUE,
 full_name TEXT NOT NULL, email TEXT UNIQUE, program TEXT NOT NULL DEFAULT 'B.Tech',
 section TEXT NOT NULL, semester INTEGER NOT NULL CHECK(semester BETWEEN 1 AND 12));
CREATE TABLE IF NOT EXISTS faculty(
 faculty_id INTEGER PRIMARY KEY AUTOINCREMENT, faculty_code TEXT NOT NULL UNIQUE,
 full_name TEXT NOT NULL, email TEXT UNIQUE, department TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS subjects(
 subject_id INTEGER PRIMARY KEY AUTOINCREMENT, subject_code TEXT NOT NULL UNIQUE,
 subject_name TEXT NOT NULL, semester INTEGER NOT NULL CHECK(semester BETWEEN 1 AND 12),
 credits INTEGER NOT NULL DEFAULT 3 CHECK(credits BETWEEN 1 AND 10));
CREATE TABLE IF NOT EXISTS rooms(
 room_id INTEGER PRIMARY KEY AUTOINCREMENT, room_code TEXT NOT NULL UNIQUE,
 building TEXT NOT NULL, capacity INTEGER NOT NULL CHECK(capacity > 0));
CREATE TABLE IF NOT EXISTS exams(
 exam_id INTEGER PRIMARY KEY AUTOINCREMENT, subject_id INTEGER NOT NULL REFERENCES subjects(subject_id),
 exam_date TEXT NOT NULL, start_time TEXT NOT NULL, end_time TEXT NOT NULL,
 room_id INTEGER NOT NULL REFERENCES rooms(room_id), invigilator_id INTEGER NOT NULL REFERENCES faculty(faculty_id),
 section TEXT NOT NULL, max_marks REAL NOT NULL DEFAULT 100 CHECK(max_marks > 0),
 status TEXT NOT NULL DEFAULT 'Scheduled' CHECK(status IN ('Scheduled','Completed','Cancelled')),
 CHECK(start_time < end_time));
CREATE TABLE IF NOT EXISTS results(
 result_id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL REFERENCES students(student_id),
 exam_id INTEGER NOT NULL REFERENCES exams(exam_id), marks_obtained REAL NOT NULL CHECK(marks_obtained >= 0),
 grade TEXT NOT NULL, published INTEGER NOT NULL DEFAULT 0 CHECK(published IN (0,1)),
 UNIQUE(student_id, exam_id));
"""

def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys=ON")
    return c

def init():
    with conn() as c:
        c.executescript(SCHEMA)
        if c.execute("SELECT COUNT(*) FROM students").fetchone()[0] == 0:
            c.execute("INSERT INTO students(roll_number,full_name,email,program,section,semester) VALUES(?,?,?,?,?,?)",
                      ("DEMO001","Aarav Sharma","aarav@example.edu","B.Tech AI & ML","Rhinos",3))
            c.execute("INSERT INTO students(roll_number,full_name,email,program,section,semester) VALUES(?,?,?,?,?,?)",
                      ("DEMO002","Maya Reddy","maya@example.edu","B.Tech AI & ML","Rhinos",3))
            c.execute("INSERT INTO faculty(faculty_code,full_name,email,department) VALUES(?,?,?,?)",
                      ("FAC001","Dr. Priya Nair","priya@example.edu","Computer Science"))
            c.execute("INSERT INTO subjects(subject_code,subject_name,semester,credits) VALUES(?,?,?,?)",
                      ("DBMS301","Database Management Systems",3,4))
            c.execute("INSERT INTO rooms(room_code,building,capacity) VALUES(?,?,?)",("A-101","Academic Block A",40))
init()

def df(sql, params=()):
    with conn() as c:
        return pd.read_sql_query(sql, c, params=params)

def run(sql, params=()):
    with conn() as c:
        c.execute(sql, params)

def grade(marks, maximum):
    p = 100 * marks / maximum
    return "A+" if p >= 90 else "A" if p >= 80 else "B" if p >= 70 else "C" if p >= 60 else "D" if p >= 40 else "F"

def safe_run(sql, params):
    try:
        run(sql, params)
        st.success("Saved successfully.")
        st.rerun()
    except sqlite3.IntegrityError as e:
        st.error(f"Database rule prevented this operation: {e}")
    except Exception as e:
        st.error(f"Operation failed: {e}")

st.markdown("""
<style>
.block-container{padding-top:1.5rem;max-width:1450px}
[data-testid="stSidebar"]{background:#172744}
[data-testid="stSidebar"] *{color:#f4f7fb}
.hero{padding:1.5rem;border-radius:16px;background:linear-gradient(120deg,#172744,#285b83);color:white}
.hero h1{color:white;margin:0}.muted{color:#8290a6}
</style>
<div class="hero"><h1>🎓 ExamFlow</h1><p>Examination Scheduling & Result Processing System · DBMS Project 24</p></div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("EXAMFLOW")
    page = st.radio("NAVIGATION", ["Dashboard","Students","Faculty","Subjects","Rooms","Exam Scheduling","Results","Reports","Database Explorer"])
    st.caption("Academic prototype · fictional sample data")

if page == "Dashboard":
    st.subheader("Dashboard overview")
    metrics = [
        ("Students","SELECT COUNT(*) n FROM students"),
        ("Faculty","SELECT COUNT(*) n FROM faculty"),
        ("Subjects","SELECT COUNT(*) n FROM subjects"),
        ("Scheduled exams","SELECT COUNT(*) n FROM exams WHERE status='Scheduled'"),
        ("Results entered","SELECT COUNT(*) n FROM results"),
    ]
    cols=st.columns(len(metrics))
    for col,(label,sql) in zip(cols,metrics):
        col.metric(label,int(df(sql).iloc[0,0]))
    st.subheader("Upcoming / scheduled examinations")
    st.dataframe(df("""SELECT e.exam_date Date,e.start_time Start,e.end_time End,s.subject_code Code,
      s.subject_name Subject,r.room_code Room,f.full_name Invigilator,e.section Section,e.status Status
      FROM exams e JOIN subjects s USING(subject_id) JOIN rooms r USING(room_id)
      JOIN faculty f ON f.faculty_id=e.invigilator_id ORDER BY e.exam_date,e.start_time"""),use_container_width=True,hide_index=True)
    st.info("Use the sidebar to manage academic records, schedule exams, process results, and export reports.")

elif page == "Students":
    st.subheader("Student records")
    with st.expander("Add student",expanded=True):
        with st.form("student_form"):
            a,b,c=st.columns(3)
            roll=a.text_input("Roll number *").strip()
            name=b.text_input("Full name *").strip()
            email=c.text_input("Email").strip() or None
            program=a.text_input("Programme",value="B.Tech AI & ML").strip()
            section=b.text_input("Section",value="Rhinos").strip()
            semester=c.number_input("Semester",1,12,3)
            submit=st.form_submit_button("Save student",type="primary")
            if submit:
                if not roll or not name or not program or not section: st.error("Complete all required fields.")
                else: safe_run("INSERT INTO students(roll_number,full_name,email,program,section,semester) VALUES(?,?,?,?,?,?)",(roll,name,email,program,section,semester))
    data=df("SELECT student_id ID,roll_number Roll,full_name Name,email Email,program Programme,section Section,semester Semester FROM students ORDER BY roll_number")
    st.dataframe(data,use_container_width=True,hide_index=True)
    if not data.empty:
        with st.expander("Update student name / section"):
            sid=st.selectbox("Student",data["ID"].tolist(),format_func=lambda x:f'{data.loc[data.ID==x,"Roll"].iloc[0]} — {data.loc[data.ID==x,"Name"].iloc[0]}')
            old=data[data.ID==sid].iloc[0]
            nm=st.text_input("Name",str(old["Name"]),key="student_name_update")
            sec=st.text_input("Section",str(old["Section"]),key="student_section_update")
            if st.button("Update student"): safe_run("UPDATE students SET full_name=?,section=? WHERE student_id=?",(nm.strip(),sec.strip(),int(sid)))
        with st.expander("Delete student"):
            st.caption("Deletion is blocked by foreign-key rules if the student has results.")
            did=st.selectbox("Student to delete",data["ID"].tolist(),format_func=lambda x:f'{data.loc[data.ID==x,"Roll"].iloc[0]}',key="delete_student")
            if st.button("Delete selected student",type="secondary"): safe_run("DELETE FROM students WHERE student_id=?",(int(did),))

elif page == "Faculty":
    st.subheader("Faculty and invigilators")
    with st.form("faculty_form"):
        a,b,c=st.columns(3); code=a.text_input("Faculty code *"); name=b.text_input("Full name *"); email=c.text_input("Email *"); dept=a.text_input("Department *")
        if st.form_submit_button("Add faculty",type="primary"):
            if not all(x.strip() for x in [code,name,email,dept]): st.error("All fields are required.")
            else: safe_run("INSERT INTO faculty(faculty_code,full_name,email,department) VALUES(?,?,?,?)",(code.strip(),name.strip(),email.strip(),dept.strip()))
    st.dataframe(df("SELECT faculty_id ID,faculty_code Code,full_name Name,email Email,department Department FROM faculty"),use_container_width=True,hide_index=True)

elif page == "Subjects":
    st.subheader("Subject catalogue")
    with st.form("subject_form"):
        a,b,c=st.columns(3); code=a.text_input("Subject code *"); name=b.text_input("Subject name *"); sem=c.number_input("Semester",1,12,3); credits=a.number_input("Credits",1,10,3)
        if st.form_submit_button("Add subject",type="primary"):
            if not code.strip() or not name.strip(): st.error("Subject code and name are required.")
            else: safe_run("INSERT INTO subjects(subject_code,subject_name,semester,credits) VALUES(?,?,?,?)",(code.strip(),name.strip(),sem,credits))
    st.dataframe(df("SELECT subject_id ID,subject_code Code,subject_name Subject,semester Semester,credits Credits FROM subjects"),use_container_width=True,hide_index=True)

elif page == "Rooms":
    st.subheader("Examination rooms")
    with st.form("room_form"):
        a,b,c=st.columns(3); code=a.text_input("Room code *"); building=b.text_input("Building *"); cap=c.number_input("Capacity",1,1000,40)
        if st.form_submit_button("Add room",type="primary"):
            if not code.strip() or not building.strip(): st.error("Room code and building are required.")
            else: safe_run("INSERT INTO rooms(room_code,building,capacity) VALUES(?,?,?)",(code.strip(),building.strip(),cap))
    st.dataframe(df("SELECT room_id ID,room_code Room,building Building,capacity Capacity FROM rooms"),use_container_width=True,hide_index=True)

elif page == "Exam Scheduling":
    st.subheader("Examination timetable")
    subs=df("SELECT subject_id,subject_code,subject_name FROM subjects ORDER BY subject_code")
    rooms=df("SELECT room_id,room_code,capacity FROM rooms ORDER BY room_code")
    fac=df("SELECT faculty_id,full_name FROM faculty ORDER BY full_name")
    if subs.empty or rooms.empty or fac.empty:
        st.warning("Add at least one subject, room, and faculty member before scheduling.")
    else:
        with st.form("exam_form"):
            a,b,c=st.columns(3)
            subject=a.selectbox("Subject",subs.subject_id.tolist(),format_func=lambda x:f'{subs[subs.subject_id==x].iloc[0].subject_code} — {subs[subs.subject_id==x].iloc[0].subject_name}')
            exam_date=b.date_input("Exam date",date.today())
            section=c.text_input("Section",value="Rhinos")
            start=a.time_input("Start time",value=__import__("datetime").time(9,0))
            end=b.time_input("End time",value=__import__("datetime").time(11,0))
            room=c.selectbox("Room",rooms.room_id.tolist(),format_func=lambda x:f'{rooms[rooms.room_id==x].iloc[0].room_code} (capacity {rooms[rooms.room_id==x].iloc[0].capacity})')
            inv=a.selectbox("Invigilator",fac.faculty_id.tolist(),format_func=lambda x:fac[fac.faculty_id==x].iloc[0].full_name)
            maximum=b.number_input("Maximum marks",1.0,1000.0,100.0)
            submit=st.form_submit_button("Validate and schedule",type="primary")
            if submit:
                if end<=start: st.error("End time must be later than start time.")
                else:
                    existing=df("""SELECT COUNT(*) n FROM exams WHERE exam_date=? AND start_time < ? AND end_time > ?
                        AND (room_id=? OR invigilator_id=?)""",(exam_date.isoformat(),end.strftime("%H:%M"),start.strftime("%H:%M"),room,inv)).iloc[0,0]
                    capacity=int(rooms[rooms.room_id==room].iloc[0].capacity)
                    if existing: st.error("Conflict: room or invigilator already has an overlapping exam.")
                    else:
                        safe_run("INSERT INTO exams(subject_id,exam_date,start_time,end_time,room_id,invigilator_id,section,max_marks) VALUES(?,?,?,?,?,?,?,?)",
                                 (subject,exam_date.isoformat(),start.strftime("%H:%M"),end.strftime("%H:%M"),room,inv,section.strip(),maximum))
    st.dataframe(df("""SELECT e.exam_id ID,e.exam_date Date,e.start_time Start,e.end_time End,s.subject_code Subject,r.room_code Room,r.capacity Capacity,
      f.full_name Invigilator,e.section Section,e.max_marks MaxMarks,e.status Status FROM exams e JOIN subjects s USING(subject_id)
      JOIN rooms r USING(room_id) JOIN faculty f ON f.faculty_id=e.invigilator_id ORDER BY e.exam_date,e.start_time"""),use_container_width=True,hide_index=True)

elif page == "Results":
    st.subheader("Marks entry and result processing")
    exams=df("SELECT e.exam_id,s.subject_code,e.exam_date,e.max_marks FROM exams e JOIN subjects s USING(subject_id) ORDER BY e.exam_date")
    students=df("SELECT student_id,roll_number,full_name FROM students ORDER BY roll_number")
    if exams.empty or students.empty: st.warning("Add students and schedule an exam before entering results.")
    else:
        with st.form("result_form"):
            exam=st.selectbox("Examination",exams.exam_id.tolist(),format_func=lambda x:f'{exams[exams.exam_id==x].iloc[0].subject_code} · {exams[exams.exam_id==x].iloc[0].exam_date}')
            student=st.selectbox("Student",students.student_id.tolist(),format_func=lambda x:f'{students[students.student_id==x].iloc[0].roll_number} — {students[students.student_id==x].iloc[0].full_name}')
            maximum=float(exams[exams.exam_id==exam].iloc[0].max_marks)
            marks=st.number_input(f"Marks (0–{maximum:g})",0.0,maximum,0.0,step=1.0)
            published=st.checkbox("Publish result")
            if st.form_submit_button("Save result",type="primary"):
                safe_run("INSERT INTO results(student_id,exam_id,marks_obtained,grade,published) VALUES(?,?,?,?,?)",(student,exam,marks,grade(marks,maximum),int(published)))
    results=df("""SELECT r.result_id ID,s.roll_number Roll,s.full_name Student,sub.subject_code Subject,e.exam_date Date,
       r.marks_obtained Marks,e.max_marks Maximum,r.grade Grade,CASE r.published WHEN 1 THEN 'Published' ELSE 'Draft' END Status
       FROM results r JOIN students s USING(student_id) JOIN exams e USING(exam_id) JOIN subjects sub USING(subject_id)
       ORDER BY s.roll_number,e.exam_date""")
    st.dataframe(results,use_container_width=True,hide_index=True)
    if not results.empty:
        st.download_button("Download results CSV",results.to_csv(index=False).encode("utf-8"),"examination_results.csv","text/csv")

elif page == "Reports":
    st.subheader("SQL reports and exports")
    choice=st.selectbox("Report",["Examination timetable","Results register","Student count by section","Room utilisation","Pass/fail summary"])
    sql={
    "Examination timetable":"""SELECT e.exam_date Date,e.start_time Start,e.end_time End,sub.subject_code Subject,r.room_code Room,f.full_name Invigilator,e.section Section FROM exams e JOIN subjects sub USING(subject_id) JOIN rooms r USING(room_id) JOIN faculty f ON f.faculty_id=e.invigilator_id ORDER BY e.exam_date,e.start_time""",
    "Results register":"""SELECT s.roll_number Roll,s.full_name Student,sub.subject_code Subject,r.marks_obtained Marks,e.max_marks Maximum,r.grade Grade,r.published Published FROM results r JOIN students s USING(student_id) JOIN exams e USING(exam_id) JOIN subjects sub USING(subject_id) ORDER BY s.roll_number""",
    "Student count by section":"SELECT section Section,semester Semester,COUNT(*) Students FROM students GROUP BY section,semester ORDER BY section,semester",
    "Room utilisation":"""SELECT rm.room_code Room,rm.capacity Capacity,e.exam_date Date,e.start_time Start,e.end_time End,sub.subject_code Subject FROM rooms rm LEFT JOIN exams e USING(room_id) LEFT JOIN subjects sub USING(subject_id) ORDER BY rm.room_code,e.exam_date""",
    "Pass/fail summary":"""SELECT sub.subject_code Subject,COUNT(*) Total,SUM(CASE WHEN r.marks_obtained*100/e.max_marks>=40 THEN 1 ELSE 0 END) Pass,SUM(CASE WHEN r.marks_obtained*100/e.max_marks<40 THEN 1 ELSE 0 END) Fail FROM results r JOIN exams e USING(exam_id) JOIN subjects sub USING(subject_id) GROUP BY sub.subject_code"""
    }[choice]
    data=df(sql); st.dataframe(data,use_container_width=True,hide_index=True)
    st.download_button("Export report CSV",data.to_csv(index=False).encode("utf-8"),choice.lower().replace(" ","_")+".csv","text/csv")

elif page == "Database Explorer":
    st.subheader("Read-only database explorer")
    table=st.selectbox("Table",["students","faculty","subjects","rooms","exams","results"])
    st.dataframe(df(f"SELECT * FROM {table} LIMIT 500"),use_container_width=True,hide_index=True)
    sql=st.text_area("Custom SELECT query","SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    if st.button("Run SELECT"):
        if not sql.strip().lower().startswith(("select","with")): st.error("Only SELECT/WITH queries are permitted.")
        else:
            try: st.dataframe(df(sql),use_container_width=True,hide_index=True)
            except Exception as e: st.error(f"Query failed: {e}")

st.divider()
st.caption("ExamFlow · Project 24 · Demonstration uses fictional sample data. Confirm grading rules with course faculty before academic submission.")
