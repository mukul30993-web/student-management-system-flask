from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

app.secret_key = "student_secret_key"

DATABASE = os.path.join(BASE_DIR, "database.db")

# ---------------------------
# Database Connection
# ---------------------------
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------
# Create Table
# ---------------------------
def create_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            course TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


create_table()


# ---------------------------
# Home Page
# ---------------------------
@app.route("/")
def index():

    conn = get_db_connection()

    search = request.args.get("search")

    if search:
        students = conn.execute(
            """
            SELECT * FROM students
            WHERE name LIKE ?
            OR course LIKE ?
            OR email LIKE ?
            """,
            (f"%{search}%", f"%{search}%", f"%{search}%")
        ).fetchall()

    else:
        students = conn.execute(
            "SELECT * FROM students ORDER BY id DESC"
        ).fetchall()

    conn.close()

    return render_template("index.html", students=students)


# ---------------------------
# Add Student
# ---------------------------
@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        course = request.form["course"]
        email = request.form["email"]

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO students
            (name, age, course, email)
            VALUES (?, ?, ?, ?)
            """,
            (name, age, course, email)
        )

        conn.commit()
        conn.close()

        flash("Student Added Successfully!")

        return redirect(url_for("index"))

    return render_template("add_student.html")


# ---------------------------
# Edit Student
# ---------------------------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    ).fetchone()

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        course = request.form["course"]
        email = request.form["email"]

        conn.execute(
            """
            UPDATE students
            SET
                name=?,
                age=?,
                course=?,
                email=?
            WHERE id=?
            """,
            (name, age, course, email, id)
        )

        conn.commit()
        conn.close()

        flash("Student Updated Successfully!")

        return redirect(url_for("index"))

    conn.close()

    return render_template(
        "edit_student.html",
        student=student
    )


# ---------------------------
# Delete Student
# ---------------------------
@app.route("/delete/<int:id>")
def delete_student(id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("Student Deleted Successfully!")

    return redirect(url_for("index"))


# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)