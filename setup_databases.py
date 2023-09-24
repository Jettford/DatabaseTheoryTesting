import os
import mysql.connector

def main():
    connector = mysql.connector.connect(user="root", password="", host="127.0.0.1")

    connector.cursor().execute("CREATE DATABASE IF NOT EXISTS student;")
    connector.cursor().execute("CREATE DATABASE IF NOT EXISTS tutor;")

    # Doing through this MySQL is just much quicker, I know it is stupid
    # It is faster than doing it through python. I am sorry

    os.system(r"(C:\xampp\mysql\bin\mysql.exe -u root student < tables/student.sql)")
    os.system(r"(C:\xampp\mysql\bin\mysql.exe -u root tutor < tables/tutor.sql)")

    os.system(r"(C:\xampp\mysql\bin\mysql.exe -u root student < tables/student_and_course_data.sql)")
    os.system(r"(C:\xampp\mysql\bin\mysql.exe -u root tutor < tables/student_and_course_data.sql)")

if __name__ == "__main__":
    main()