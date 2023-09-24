import os
import json
import time

from random import randrange, randint
from datetime import timedelta, datetime

import mysql.connector

def date_between_times(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

def test1(cursor):
    test_student = 8474

    student_times = []

    for i in range(100):
        st = time.time_ns()
        cursor.execute("USE student;")

        cursor.execute(f"SELECT course_id FROM Enrolments WHERE student_id = {test_student};")
        courses = cursor.fetchall()

        cursor.execute(f"SELECT name FROM Courses WHERE id IN ({','.join([str(course[0]) for course in courses])});")
        course_names = cursor.fetchall()

        et = time.time_ns()

        student_times.append(et - st)

    print(f"Time taken for Student (Average over 100 runs): {sum(student_times) / len(student_times)}")

    tutor_times = []

    for i in range(100):
        st = time.time_ns()
        cursor.execute("USE tutor;")

        cursor.execute(f"SELECT id FROM Enrolments WHERE student_id = {test_student};")
        enrolment_id = cursor.fetchone()

        cursor.execute(f"SELECT course_id FROM EnrolmentCourse WHERE enrolment_id = {enrolment_id[0]};")
        courses = cursor.fetchall()

        cursor.execute(f"SELECT name FROM Courses WHERE id IN ({','.join([str(course[0]) for course in courses])});")
        course_names = cursor.fetchall()

        et = time.time_ns()

        tutor_times.append(et - st)
    
    print(f"Time taken for Tutor (Average over 100 runs): {sum(tutor_times) / len(tutor_times)}")

def test2(cursor):
    test_date = "2023-09-29"
    course = 4

    student_times = []

    for i in range(100):
        st = time.time_ns()
        cursor.execute("USE student;")

        cursor.execute(f"SELECT id FROM Courses WHERE name = 'Course Name {course}';")
        course_id = cursor.fetchone()[0]

        cursor.execute(f"SELECT id FROM EnrolmentDates WHERE date = '{test_date}';")
        date_id = cursor.fetchone()[0]

        cursor.execute(f"SELECT COUNT(id) FROM Enrolments WHERE date_id = {date_id} AND course_id = {course};")
        courses = cursor.fetchall()

        et = time.time_ns()

        student_times.append(et - st)

    print(f"Time taken for Student (Average over 100 runs): {sum(student_times) / len(student_times)}")

    tutor_times = []

    for i in range(100):
        st = time.time_ns()
        cursor.execute("USE tutor;")

        cursor.execute(f"SELECT id FROM Courses WHERE name = 'Course Name {course}';")
        course_id = cursor.fetchone()[0]

        cursor.execute(f"SELECT id FROM Enrolments WHERE date = '{test_date}';")
        enrolment_ids = cursor.fetchall()

        cursor.execute(f"SELECT COUNT(id) FROM EnrolmentCourse WHERE enrolment_id IN ({','.join([str(id[0]) for id in enrolment_ids])}) AND course_id = {course_id};")
        courses = cursor.fetchone()

        et = time.time_ns()

        tutor_times.append(et - st)
    
    print(f"Time taken for Tutor (Average over 100 runs): {sum(tutor_times) / len(tutor_times)}")

def test3(cursor):
    course = 4

    student_times = []

    for i in range(100):
        st = time.time_ns()
        cursor.execute("USE student;")

        cursor.execute(f"SELECT id FROM Courses WHERE name = 'Course Name {course}';")
        course_id = cursor.fetchone()[0]

        cursor.execute(f"SELECT student_id FROM Enrolments WHERE course_id = '{course_id}';")
        student_ids = cursor.fetchall()

        cursor.execute(f"SELECT first_name, last_name FROM Students WHERE id IN ({','.join([str(id[0]) for id in student_ids])});")
        students = cursor.fetchall()

        et = time.time_ns()

        student_times.append(et - st)

    print(f"Time taken for Student (Average over 100 runs): {sum(student_times) / len(student_times)}")

    tutor_times = []

    for i in range(100):
        st = time.time_ns()
        cursor.execute("USE tutor;")

        cursor.execute(f"SELECT id FROM Courses WHERE name = 'Course Name {course}';")
        course_id = cursor.fetchone()[0]

        cursor.execute(f"SELECT id FROM EnrolmentCourse WHERE course_id = '{course_id}';")
        enrolment_ids = cursor.fetchall()

        cursor.execute(f"SELECT student_id FROM Enrolments WHERE id IN ({','.join([str(id[0]) for id in enrolment_ids])});")
        student_ids = cursor.fetchall()

        cursor.execute(f"SELECT first_name, last_name FROM Students WHERE id IN ({','.join([str(id[0]) for id in student_ids])});")
        students = cursor.fetchall()

        et = time.time_ns()

        tutor_times.append(et - st)
    
    print(f"Time taken for Tutor (Average over 100 runs): {sum(tutor_times) / len(tutor_times)}")


def main():
    connector = mysql.connector.connect(user="root", password="", host="127.0.0.1", database="student")
    connector.autocommit = True
    # Build our data in memory/python and then insert it into the database
    # This is to ensure all the random data is consistent

    enrolments = {}

    cursor = connector.cursor(buffered=True)

    for i in range(1, 10001): # 10000 students
        enrolments[i] = {}
        enrolments[i]["date"] = date_between_times(datetime(2023, 9, 1), datetime(2023, 9, 30)).strftime('%Y-%m-%d')
        enrolments[i]["courses"] = []

        for j in range(randint(1, 3)):
            enrolments[i]["courses"].append(randint(1, 100))

    cursor.execute("USE student;")

    for key, enrolment in enrolments.items():
        for course in enrolment["courses"]:
            print(enrolment)
            cursor.execute(f"INSERT IGNORE INTO `enrolmentdates` (`date`) VALUES ('{enrolment['date']}');")
            connector.commit()

            cursor.execute(f"SELECT id FROM `enrolmentdates` WHERE `date` = '{enrolment['date']}';")

            result = cursor.fetchone()

            date_cache = result[0]

            cursor.execute(f"INSERT INTO Enrolments (student_id, course_id, date_id) VALUES ({key}, {course}, '{date_cache}');")


    cursor.execute("USE tutor;")

    for key, enrolment in enrolments.items():
        cursor.execute(f"INSERT INTO Enrolments (student_id, date) VALUES ({key}, '{enrolment['date']}');")
        enrolment_id = cursor.lastrowid

        for course in enrolment["courses"]:
            cursor.execute(f"INSERT INTO EnrolmentCourse (enrolment_id, course_id) VALUES ({enrolment_id}, {course});")

    # Run tests
    # Get all students from a course ID
    
    test1(cursor)
    test2(cursor)
    test3(cursor)
    
    connector.close()

if __name__ == "__main__":
    main()