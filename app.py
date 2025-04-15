from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# --- Initialize Database ---
def init_db():
    with sqlite3.connect('school.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT, age INTEGER, class_level TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id INTEGER,
                        date TEXT,
                        status TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS timetable (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        class_level TEXT,
                        day TEXT,
                        subject TEXT,
                        time TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS staff (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT, role TEXT, contact TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS parents (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id INTEGER,
                        name TEXT, phone TEXT)''')

# --- Fetch all data ---
def fetch_all():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()

    c.execute("SELECT * FROM students")
    students = c.fetchall()

    c.execute("SELECT s.name, a.date, a.status FROM attendance a JOIN students s ON a.student_id = s.id")
    attendance = c.fetchall()

    c.execute("SELECT * FROM timetable")
    timetable = c.fetchall()

    c.execute("SELECT * FROM staff")
    staff = c.fetchall()

    c.execute("SELECT s.name, p.name, p.phone FROM parents p JOIN students s ON p.student_id = s.id")
    parents = c.fetchall()

    return students, attendance, timetable, staff, parents

# --- Chart data helpers ---
def get_student_chart_data():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    c.execute("SELECT class_level, COUNT(*) FROM students GROUP BY class_level")
    data = c.fetchall()
    labels = [row[0] for row in data]
    counts = [row[1] for row in data]
    return {'labels': labels, 'data': counts}

def get_attendance_summary():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    c.execute("SELECT status, COUNT(*) FROM attendance GROUP BY status")
    result = dict(c.fetchall())
    return {
        'present': result.get('Present', 0),
        'absent': result.get('Absent', 0)
    }

# --- Routes ---
@app.route('/')
def index():
    students, attendance, timetable, staff, parents = fetch_all()
    student_chart_data = get_student_chart_data()
    attendance_chart_data = get_attendance_summary()
    return render_template('index.html',
                           students=students,
                           attendance=attendance,
                           timetable=timetable,
                           staff=staff,
                           parents=parents,
                           student_chart_data=student_chart_data,
                           attendance_chart_data=attendance_chart_data)

# --- Add student ---
@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    age = request.form['age']
    class_level = request.form['class_level']
    conn = sqlite3.connect('school.db')
    conn.execute("INSERT INTO students (name, age, class_level) VALUES (?, ?, ?)", (name, age, class_level))
    conn.commit()
    return redirect('/')

# --- Add attendance ---
@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    student_id = request.form['student_id']
    date = request.form['date']
    status = request.form['status']
    conn = sqlite3.connect('school.db')
    conn.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)", (student_id, date, status))
    conn.commit()
    return redirect('/')

# --- Add timetable ---
@app.route('/add_timetable', methods=['POST'])
def add_timetable():
    class_level = request.form['class_level']
    day = request.form['day']
    subject = request.form['subject']
    time = request.form['time']
    conn = sqlite3.connect('school.db')
    conn.execute("INSERT INTO timetable (class_level, day, subject, time) VALUES (?, ?, ?, ?)",
                 (class_level, day, subject, time))
    conn.commit()
    return redirect('/')

# --- Add staff ---
@app.route('/add_staff', methods=['POST'])
def add_staff():
    name = request.form['name']
    role = request.form['role']
    contact = request.form['contact']
    conn = sqlite3.connect('school.db')
    conn.execute("INSERT INTO staff (name, role, contact) VALUES (?, ?, ?)", (name, role, contact))
    conn.commit()
    return redirect('/')

# --- Add parent ---
@app.route('/add_parent', methods=['POST'])
def add_parent():
    student_id = request.form['student_id']
    name = request.form['name']
    phone = request.form['phone']
    conn = sqlite3.connect('school.db')
    conn.execute("INSERT INTO parents (student_id, name, phone) VALUES (?, ?, ?)", (student_id, name, phone))
    conn.commit()
    return redirect('/')

# --- Logout (Dummy for now) ---
@app.route('/logout')
def logout():
    return redirect('/')

# --- Run App ---
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
