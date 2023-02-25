import mysql.connector as mysql

db = mysql.connect(
    host="localhost",
    user="root",
    port="3306",
    password="password",
    database="college"
)

try:
    print("Connected to server successfully.")
except Exception as e:
    print("Unable to connect to sever.")
    print(e)

command_handler = db.cursor(buffered=True)


def student_session(username):
    print("\n STUDENT MENU \n")
    student_menu = ["1. View Register", "2. Download Register", "3. Logout"]

    for student in student_menu:
        print(student)

    user_input = int(input("Option: "))
    if user_input == 1:
        print(username)
        print("Displaying Register")
        username = (str(username), )
        command_handler.execute("SELECT date, username, status FROM college_attendance WHERE  username = ,%s", username)
        records = command_handler.fetchall()
        for record in records:
            print(record)
    else:
        pass


def teacher_session():
    while True:
        print("\n TEACHER MENU \n")
        teacher_menu = ["1. Mark Student Register", "2. View Register", "3. Logout"]

        for teacher in teacher_menu:
            print(teacher)
        user_input = int(input("Option: "))
        if user_input == 1:
            print(" \n MARK STUDENT REGISTER \n")
            command_handler.execute("SELECT  username from users WHERE  priviledge = 'Student'")
            records = command_handler.fetchall()
            date = input("Date - DD/MM/YYYY: ")
            for record in records:
                record = str(record).replace("'", "")
                record = str(record).replace(",", "")
                record = str(record).replace("(", "")
                record = str(record).replace(")", "")
                # Present | Absent | Late
                status = input(str("Status for " + str(record) + " P/A/L: "))
                query_values = (str(record), date, status)
                command_handler.execute("INSERT INTO college_attendance (username, date, status) VALUES (%s, %s, %s)",
                                        query_values)
                db.commit()
                print(record + " Marked as " + status)
        elif user_input == 2:
            print("\n VIEW ALL STUDENT REGISTER \n")
            command_handler.execute("SELECT username, date, status FROM college_attendance")
            records = command_handler.fetchall()
            print("Displaying All Records")
            for record in records:
                print(record)
        elif user_input == 3:
            break
        else:
            print("Invalid Option Selected")


def admin_session():
    while True:
        print("\n ADMIN MENU \n")
        admin_menu = ["1. Register a student", "2. Register a teacher", "3. Delete an existing student",
                      "4. Delete an existing teacher", "5. Logout"]

        for admin in admin_menu:
            print(admin)
        user_input = int(input("Option: "))

        if user_input == 1:
            print("\n Register \n")
            username = str(input("Username: "))
            password = str(input("Password: "))
            query_values = (username, password)
            command_handler.execute("INSERT INTO users (username, password, priviledge) VALUES (%s,%s, 'Student')",
                                    query_values)
            db.commit()
            print(username + " has been registered as a Student")

        elif user_input == 2:
            print("\n Register \n")
            username = str(input("Username: "))
            password = str(input("Password: "))
            query_values = (username, password)
            command_handler.execute("INSERT INTO users (username, password, priviledge) VALUES (%s,%s, 'Teacher')",
                                    query_values)
            db.commit()
            print(username + " has been registered as a Teacher")

        elif user_input == 3:
            print("\n Delete Existing Student Account \n")
            username = str(input("Username: "))
            query_values = (username, "Student")
            command_handler.execute("DELETE FROM users WHERE username = %s AND priviledge = %s", query_values)
            db.commit()
            if command_handler.rowcount < 1:
                print("User not found.")
            else:
                print(username + " has been deleted.")

        elif user_input == 4:
            print("\n Delete Existing Teacher Account \n")
            username = str(input("Username: "))
            query_values = (username, "Teacher")
            command_handler.execute("DELETE FROM users WHERE username = %s AND priviledge = %s", query_values)
            db.commit()
            if command_handler.rowcount < 1:
                print("User not found.")
            else:
                print(username + " has been deleted.")

        elif user_input == 5:
            break
        else:
            print("Invalid option selected.")


def auth_student():
    print("\n STUDENT LOGIN \n")
    username = str(input("Username: "))
    password = str(input("Password: "))
    query_values = (username, password, 'Student')
    command_handler.execute("SELECT  username FROM users WHERE  username = %s AND password = %s AND priviledge = %s", query_values)
    username = command_handler.fetchone()
    if command_handler.rowcount <= 0:
        print("Invalid login details.")
    else:
        student_session(username)


def auth_teacher():
    print("\n TEACHER LOGIN \n")
    username = str(input("Username: "))
    password = str(input("Password: "))
    query_values = (username, password)
    command_handler.execute("SELECT * FROM users WHERE username = %s AND password = %s AND priviledge = 'Teacher'",
                            query_values)
    if command_handler.rowcount <= 0:
        print("Login not recognised")
    else:
        teacher_session()


def auth_admin():
    print("\n ADMIN LOGIN \n")
    username = str(input("Username: "))
    password = str(input("Password: "))
    if username == "admin":
        if password == "password":
            admin_session()
        else:
            print("Incorrect Password.")
    else:
        print("Login details not recognised.")


def main():
    while True:
        print("Welcome To FCE College Management System. \n")
        main_manu = ["1. LOGIN AS ADMIN", "2. LOGIN AS TEACHER", "3. LOGIN AS STUDENT", "4. EXIT"]

        for i in main_manu:
            print(i)

        user_input = int(input("Option: \n"))

        if user_input == 1:
            auth_admin()

        elif user_input == 2:
            auth_teacher()

        elif user_input == 3:
            auth_student()

        elif user_input == 4:
            print("THANKS FOR USING OUR APP")
            break

        else:
            print("NO VALID OPTION WAS SELECTED.")


main()
