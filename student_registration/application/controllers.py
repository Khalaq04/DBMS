from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
from application.models import Student, Course, Enrollments
import sqlalchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import Session, relationship
from application.database import Base, db, engine
from application.config import LocalDevelopementConfig

def error():
    return render_template("error.html")

@app.route("/", methods=["GET", "POST"])
def root():
    students = Student.query.all()

    if not students:
        return render_template("root_1.html")
    
    return render_template("root_2.html", students=students)

@app.route("/student/create", methods=["GET", "POST"])
def add_student():
    if request.method == "GET":
        return render_template("add_student.html")
    
    try:
        if request.method == "POST":
            roll_number = request.form["roll"]
            first_name = request.form["f_name"]
            last_name = request.form["l_name"]
            course_list = request.form.getlist('check')

            if db.session.query(Student).filter(Student.roll_number == roll_number).first() is not None:
                return render_template("exists.html")

            new_student = Student(roll_number=roll_number, first_name=first_name, last_name=last_name)
            for course in course_list:
                course_details = db.session.query(Course).filter(Course.course_name == course).one()
                new_student.courses.append(course_details)
            db.session.add(new_student)
            db.session.commit()
            return redirect(url_for('root'))
    
    except:
        return render_template("exists.html")
    
@app.route("/student/<int:student_id>", methods=["GET", "POST"])
def details(student_id):
    student = Student.query.filter(Student.student_id == student_id).one()
    enrollments = Enrollments.query.filter(Enrollments.estudent_id == student_id).all()
    courses = []
    for enrollment in enrollments:
        course = Course.query.filter(Course.course_id == enrollment.ecourse_id).all()
        courses.append(course[0])
    return render_template("details.html", student=student, courses=courses)

@app.route("/student/<int:student_id>/update", methods=["GET", "POST"])
def update(student_id):
    student = Student.query.filter(Student.student_id == student_id).one()
    enrollments = Enrollments.query.filter(Enrollments.estudent_id == student_id).all()
    courses = []
    for enrollment in enrollments:
        course = Course.query.filter(Course.course_id == enrollment.ecourse_id).all()
        courses.append(course[0])

    if request.method == "GET":
        return render_template("update.html", student=student, courses=courses)
    
    try:
        if request.method == "POST":
            roll_number = request.form["roll"]
            first_name = request.form["f_name"]
            last_name = request.form["l_name"]
            course_list = request.form.getlist('check')

            if db.session.query(Student).filter(Student.roll_number == roll_number).first() is not None and student.roll_number != roll_number:
                return render_template("exists.html")

            student.roll_number = roll_number
            student.first_name = first_name
            student.last_name = last_name

            Enrollments.query.filter(Enrollments.estudent_id == student_id).delete()
            for course in course_list:
                course_details = db.session.query(Course).filter(Course.course_name == course).one()
                student.courses.append(course_details)
            db.session.commit()

            return redirect(url_for('root'))
        
    except:
        return error()
    
@app.route("/student/<int:student_id>/delete", methods=["GET", "POST"])
def delete(student_id):
    Student.query.filter(Student.student_id == student_id).delete()
    Enrollments.query.filter(Enrollments.estudent_id == student_id).delete()
    db.session.commit()
    return redirect(url_for('root'))