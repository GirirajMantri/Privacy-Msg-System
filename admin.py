import mysql.connector as sql
import pandas as pd
import os
from datetime import datetime
import threading
import cv2
import face_recognition
import time


# ==============================================================================
# welcome message

now = datetime.now()
date = now.strftime("%d/%b/%Y")
current_time = now.strftime("%H:%M:%S")



def welcome():
    try:
        print(" \n")
        print("                ==============================================================")
        print("                *                                                            *")
        print("                *                    -: WELCOME TO :-                        *")
        print("                *                                                            *")
        print("                *              -: Privacy Messaging System :-                *")
        print("                *                                                            *")
        print("                *                                         -By Bug_Duckers    *")
        print("                *                                                            *")
        print("                ==============================================================")
        print("                       Date =",date,"            Time =",current_time)
        print(" \n")

    except Exception as e:  # if an error exists
        print(e)  # print error


# ==============================================================================
# establish connection

try:
    cn = sql.connect(host="localhost", user="root", password="root")
    # cn = sql.connect(host="10.12.103.", user="guest", password="root")
    cur = cn.cursor()

    # create database if not exists and use it

    cur.execute("create database if not exists project")
    cur.execute("use project")

    # create tables if not exist
    cur.execute("CREATE TABLE IF NOT EXISTS users ( \
        username VARCHAR(20) PRIMARY KEY, \
        password VARCHAR(20) NOT NULL \
        )")

    cur.execute("CREATE TABLE IF NOT EXISTS conversation ( \
        s_no INT AUTO_INCREMENT PRIMARY KEY, \
        date DATE, \
        time TIME, \
        sender VARCHAR(20), \
        receiver VARCHAR(20), \
        msg VARCHAR(255), \
        FOREIGN KEY (sender) REFERENCES users(username), \
        FOREIGN KEY (receiver) REFERENCES users(username) \
        )")

    

except Exception as e:
    print(e)


# ==============================================================================
# login menu(homepage)
admin_pwd = "123"
shift_value = 3

def homepage():
    try:
        welcome()  # welcome msg
        print(" 1. Admin ")  # admin privileges [password(123)]
        print(" 2. User") # Enter Username and password
        print(" 3. EXIT ")   # quit the programme
        print(" \n Please SELECT A Value Between 1 & 3 As Per Your CHOICE \n")
        select = input(" Enter Your Choice : ")
        if select == '1':
            pwd = input(" Enter password: ")
            if pwd == admin_pwd:
                face_auth()
                if authentication:
                    admin_menu()
                else:
                    print("Face Authentication failed ! ")
                    homepage()  # back to homepage
            else:
                print(" \n Invalid Password \n Try Again :- \n")
                homepage()  # back to homepage

        elif select == '2':
            username = input("Enter username: ")

            global current_user
            current_user = username

            global password
            password = input("Enter password: ")

            cur.execute("SELECT * FROM users WHERE username = %s AND password = %s",(username, password))
            user = cur.fetchone()  # fetch one result
            if user:
                print("User authenticated successfully!")
                face_auth()
                if authentication:
                    user_menu()

                else:
                    print("Face Authentication failed ! ")
                    homepage()  # back to homepage
            
            else:
                print(" \n Invalid credentials! Try Again :- \n")
                homepage()  # back to homepage
            

        elif select == '3':
            exit()  # kill the terminal

        else:
            print(" \n Invalid choice! Enter 1-3 :- \n Try Again :- \n ")  # restrict input from 1 & 3
            homepage()

    except Exception as e:
        clear_terminal()
        print(e)


# all operations related to users
def admin_menu():
    try:
        welcome()  # welcome msg
        print(" 1. Add New user ")  # add values
        print(" 2. Display user Details ")  # select values
        print(" 3. Edit user Details ")  # alter table
        print(" 4. Remove A user ")  # drop|delete value
        print(" 5. CSV File")
        print(" 6. Go To Home Window ")  # homepage
        print(" \n Please SELECT A Value Between 1 TO 6 As Per Your CHOICE \n ")
        select = input(" Enter Your Choice : ")
        if select == '1':
            new_user_manual()  # add value in table users
        elif select == '2':
            display_user()  # select value from table users
        elif select == '3':
            try:
                clear_terminal()
                welcome()  # welcome msg
                username = input(" Enter user id whose password has to be Edited: ")
                password = input(" Enter new password: ")
                query = "update users set password='{}' where username='{}'".format(password, username)
                cur.execute(query)  # execute query in sql
                cn.commit()  # save changes in sql
                print(" password edited successfully \n")
                admin_menu()

            except Exception as e:
                clear_terminal()
                print(e)
                admin_menu()  # all operations related to users

            edit_user()  # alter values of table users
        elif select == '4':
            remove_user()  # delete value from users
        elif select == '5':
            csv_file()
        elif select == '6':
            homepage()  # homepage
        else:
            print(" \n Invalid choice! Enter 1-6 :- \n Try Again :- \n ")
            admin_menu()  # all operations related to users

    except Exception as e:
        clear_terminal()
        print(e)
        homepage() # homepage


# add value in terminal
def new_user_manual():
    try:
        clear_terminal()
        welcome()  # welcome msg
        print(" Enter The Following Details Of New user :- \n ")
        username = input(" username  (varchar): ")
        password = input(" password  (varchar): ")
        

        query = "insert into users (username,password) values('{}','{}')".format(username,password)
        cur.execute(query)  # execute query in sql
        cn.commit()  # save changes in sql

        print(" \n details filled successfully \n")

        admin_menu()

    except Exception as e:
        clear_terminal()
        print(e)
        admin_menu()


def csv_file():
    try:
        clear_terminal()
        welcome()  # welcome msg
        print(" 1. Import from CSV File ")
        print(" 2. Export to CSV File")
        print(" 3. GO Back ")  # all operations related to users
        print(" 4. Go To Home Window ")  # homepage
        print(" \n Please SELECT A Value Between 1 TO 3 As Per Your CHOICE \n ")
        select = input(" Enter Your Choice : ")
        if select == '1':
            csv_file_import()  # add value from csv file
        elif select == '2':
            csv_file_export()
        elif select == '3':
            admin_menu()  # all operations related to users
        elif select == '4':
            homepage()  # homepage
        else:
            print(" \n Invalid choice! Enter 1-3 :- \n Try Again :- \n ")
            display_user()

    except Exception as e:
        clear_terminal()
        print(e)
        admin_menu()

def csv_file_import():
    try:
        clear_terminal()
        welcome()  # welcome msg
        print(" 1. Import users from CSV File ")
        print(" 2. Import conversation from CSV File ")
        print(" 3. GO Back ")  # all operations related to users
        print(" 4. Go To Home Window ")  # homepage
        print(" \n Please SELECT A Value Between 1 TO 4 As Per Your CHOICE \n ")
        select = input(" Enter Your Choice : ")
        if select == '1':
            csv_file_import()  # add value from csv file
        elif select == '2':
            csv_file_export()
        elif select == '3':
            admin_menu()  # all operations related to users
        elif select == '4':
            homepage()  # homepage
        else:
            print(" \n Invalid choice! Enter 1-3 :- \n Try Again :- \n ")
            display_user()

    except Exception as e:
        clear_terminal()
        print(e)
        admin_menu()


# add data in users by csv file
def new_user_csv():
    try:
        clear_terminal()
        select = input(" Enter File Location : ")  # location of file
        file = pd.read_csv(select,header=None)  # header=0 if file have column name without header if it is without column names
        df = pd.DataFrame(file)  # change from csv to dataframe
        welcome()  # welcome msg
        for (row, col) in df.iterrows():
            username = col[0]  # column 1
            password = col[1]  # column 2
            query = "insert into users (username,password) values('{}','{}')".format(username,password)
            cur.execute(query)  # execute query in sql
            cn.commit()  # save changes in sql
        print(" \n details filled successfully \n")

        admin_menu()

    except Exception as e:
        clear_terminal()
        print(e)
        admin_menu()


# add data in conversation by csv file
def new_conversation_csv():
    try:
        clear_terminal()
        select = input(" Enter File Location : ")  # location of file
        file = pd.read_csv(select,header=None)  # header=0 if file have column name without header if it is without column names
        df = pd.DataFrame(file)  # change from csv to dataframe
        welcome()  # welcome msg
        for (row, col) in df.iterrows():
            date = col[1]  # column 2
            time = col[2]  # column 3
            sender = col[3]  # column 4
            receiver = col[4]  # column 5
            msg = col[5]  # column 6
            query = f"insert into conversation(date,time,sender,receiver,msg) values('{date}','{time}','{sender}','{receiver}','{msg}')"
            cur.execute(query)  # execute query in sql
            cn.commit()  # save changes in sql
        print(" \n details filled successfully \n")

        admin_menu()

    except Exception as e:
        clear_terminal()
        print(e)
        admin_menu()

def csv_file_export():
    try:
        clear_terminal()
        welcome()  # welcome msg
        print(" 1. Export users to CSV file ")
        print(" 2. Export conversation to CSV file")
        print(" 3. GO Back ")  # all operations related to users
        print(" 4. Go To Home Window ")  # homepage
        print(" \n Please SELECT A Value Between 1 TO 4 As Per Your CHOICE \n ")
        select = input(" Enter Your Choice : ")
        if select == '1':
            try:
                file_name = input("Enter file name : ")
                enclo = '"'
                query = f"SELECT * FROM users INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/{file_name}' FIELDS TERMINATED BY ','  ENCLOSED BY '{enclo}' LINES TERMINATED BY '\n'"
                cur.execute(query)  # execute query in sql
                cn.commit()  # save changes in sql
                print("Exported file successfully ! ")
                admin_menu()
            except Exception as e:
                print(e)
                admin_menu()  # all operations related to users
        elif select == '2':
            try:
                file_name = input("Enter file name : ")
                enclo = '"'
                query = f"SELECT * FROM conversation INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/{file_name}' FIELDS TERMINATED BY ','  ENCLOSED BY '{enclo}' LINES TERMINATED BY '\n'"
                cur.execute(query)  # execute query in sql
                cn.commit()  # save changes in sql
                print("Exported file successfully ! ")
                admin_menu()
            except Exception as e:
                print(e)
                admin_menu()  # all operations related to users
        elif select == '3':
            admin_menu()  # all operations related to users
        elif select == '4':
            homepage()  # homepage
        else:
            print(" \n Invalid choice! Enter 1-4 :- \n Try Again :- \n ")
            display_user()  # display values of users
        
        admin_menu()

    except Exception as e:
        clear_terminal()
        print(e)
        admin_menu()  # all operations related to users
    

# display values of tables
pd.set_option("display.max_rows", None, "display.max_columns", None)

# display values of users
def display_user():
    try:
        welcome()  # welcome msg
        print(" 1. Display All user Details ")
        print(" 2. Display A user Details with username ")
        print(" 3. GO Back ")  # all operations related to users
        print(" 4. Go To Home Window ")  # homepage
        print(" \n Please SELECT A Value Between 1 TO 4 As Per Your CHOICE \n ")
        select = input(" Enter Your Choice : ")
        if select == '1':
            display_user_all()  # display values of all users
        elif select == '2':
            display_user_one()  # display values of users by u_id
        elif select == '3':
            admin_menu()  # all operations related to users
        elif select == '4':
            homepage()  # homepage
        else:
            print(" \n Invalid choice! Enter 1-4 :- \n Try Again :- \n ")
            display_user()  # display values of users
        
        admin_menu()

    except Exception as e:
        clear_terminal()
        print(e)
        admin_menu()  # all operations related to users


# display values of all users
def display_user_all():
    try:
        clear_terminal()
        welcome()  # welcome msg
        query = "Select * from users"
        cur.execute(query)  # execute query in sql
        # convert to dataframe
        df = pd.DataFrame(cur.fetchall(), columns=['username', 'password'])
        print(df)  # display values of all users
        cn.commit()  # save changes in sql
        print(" \n user Details obtained successfully \n ")
        display_user()  # display values of users

    except Exception as e:
        clear_terminal()
        print(e)
        admin_menu()  # all operations related to users

# display values of users by u_id
def display_user_one():
    try:
        clear_terminal()
        welcome()  # welcome msg
        username = input(" Enter username: ")
        query = "Select * from users where username ='{}'".format(username)
        cur.execute(query)  # execute query in sql
        # convert to dataframe
        df = pd.DataFrame(cur.fetchall(), columns=['username', 'password'])
        print(df)  # display values of all users
        cn.commit()  # save changes in sql
        print(" \n user Details obtained successfully \n ")
        display_user()

    except Exception as e:
        clear_terminal()
        print(e)
        admin_menu()  # all operations related to users


# delete values of tables

# delete values of table users
def remove_user():
    try:
        clear_terminal()
        welcome()   # welcome msg
        print(" 1. delete A user Details with username ")
        print(" 2. delete All user Details ")
        print(" 3. Go Back ")
        print(" 4. Go To Home Window ")
        print(" \n Please SELECT A Value Between 1 TO 4 As Per Your CHOICE \n ")
        select = input(" Enter Your Choice : ")
        if select == '1':
            remove_user_one()   # delete values of a user by u_id
        elif select == '2':
            remove_user_all()   # delete values of all users
        elif select == '3':
            admin_menu()   # all operations related to users
        elif select == '4':
            homepage()   # homepage
        else:
            print(" \n Invalid choice! Enter 1-4 :- \n Try Again :- \n ")
            remove_user()   # delete values of users

    except Exception as e:
        clear_terminal()
        print(e)
        admin_menu()  # all operations related to users

# delete values of all users
def remove_user_all():
    try:
        clear_terminal()
        welcome()  # welcome msg
        select = input("\n Enter Admin Password to delete the record : ")
        if select == admin_pwd:
            print(" Password Matched\n")
            query = "delete from users"
            face_auth()
            if authentication:

                cur.execute(query)  # execute query in sql
                cn.commit()  # save changes in sql
                print("all users removed successfully")
                admin_menu()

            else:
                print("Face Authentication Failed")
                admin_menu()  # all operations related to users

        else:
            print(" Invalid Password")
            admin_menu()  # all operations related to users

    except Exception as e:
        clear_terminal()
        print(e)
        admin_menu()  # all operations related to users


# delete values of a user by u_id
def remove_user_one():
    try:
        clear_terminal()
        welcome()  # welcome msg
        username = input(" Enter the username of user who has to be deleted: ")
        select = input("\n Enter Admin Password to delete the record : ")
        if select == admin_pwd:
            print(" Password Matched\n")
            query = "delete from users where username='{}'".format(username)
            cur.execute(query)  # execute query in sql
            cn.commit()  # save changes in sql
            print(" user removed successfully")
            admin_menu()

        else:
            print(" Invalid Password")
            admin_menu()  # all operations related to users

    except Exception as e:
        clear_terminal()
        print(e)
        admin_menu()  # all operations related to users



def face_auth():
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Counter for frame processing
    counter = 0

    # Load and encode the reference images
    known_face_encodings = []
    known_face_names = []

    try:
        # Add your reference images and names
        known_person1_image = face_recognition.load_image_file('ak.jpg')
        # known_person2_image = face_recognition.load_image_file('d1.jpeg')
        known_person3_image = face_recognition.load_image_file('m1.jpg')

        # Encode the reference images and append to the lists
        known_face_encodings.append(face_recognition.face_encodings(known_person1_image)[0])
        # known_face_encodings.append(face_recognition.face_encodings(known_person2_image)[0])
        known_face_encodings.append(face_recognition.face_encodings(known_person3_image)[0])

        known_face_names.append('AK')
        # known_face_names.append('Dhani')
        known_face_names.append('Mantri')

    except Exception as e:
        print(f"Error loading or encoding images: {e}")
        cap.release()
        cv2.destroyAllWindows()
        return False

    # Global variable for detected names with a lock for thread safety
    detected_names = []
    lock = threading.Lock()

    def check_faces(frame):
        nonlocal detected_names
        try:
            # Detect face locations and encodings
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
                name = "Unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                if name != "Unknown":
                    names.append(name)

            # Safely update the detected names
            with lock:
                detected_names = names
        except Exception as e:
            print(f"Error during face verification: {e}")

    start_time = time.time()
    global authentication
    authentication = False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame. Exiting...")
            break

        # Mirror the frame
        frame = cv2.flip(frame, 1)

        # Process every 30 frames in a separate thread
        if counter % 30 == 0:
            threading.Thread(target=check_faces, args=(frame.copy(),), daemon=True).start()
        counter += 1

        # Display the detected names
        with lock:
            if detected_names:
                match_text = ", ".join(detected_names)
                cv2.putText(frame, "MATCH!", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Users: {match_text}", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                authentication = True
            else:
                cv2.putText(frame, "NO MATCH!", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                authentication = False

        # Show the video frame
        cv2.imshow('Video', frame)

        # Exit conditions
        if cv2.waitKey(1) == ord('q'):
            break
        if time.time() - start_time > 3:
            break

    cap.release()
    cv2.destroyAllWindows()



def user_menu():
    try:
        welcome()  # welcome msg
        print(" 1. Send message ")  # add values
        print(" 2. Display inbox ")  # select values
        print(" 3. Display public inbox ")  # alter values of table users
        print(" 4. Go To Home Window ")  # homepage
        print(" \n Please SELECT A Value Between 1 TO 4 As Per Your CHOICE \n ")
        select = input(" Enter Your Choice : ")
        if select == '1':
            send_msg()
        elif select == '2':
            display_inbox()  # select value from table users
        elif select == '3':
            p_inbox()  # alter values of table users
        elif select == '4':
            homepage()  # homepage
        else:
            print(" \n Invalid choice! Enter 1-4 :- \n Try Again :- \n ")
            user_menu()  # all operations related to users

    except Exception as e:
        clear_terminal()
        print(e)
        homepage() # homepage


def send_msg():
    try:
        clear_terminal()
        welcome()  # welcome msg
        receiver = input(" Enter the username of recipient: ")
        msg = input(" Enter your message: ")
        encrypted_msg = encrypt_text(msg, shift_value)
        query = "insert into conversation(date,time,sender,receiver,msg) values(curdate(),curtime(),'{}','{}','{}')".format(current_user,receiver, encrypted_msg)
        cur.execute(query)  # execute query in sql
        cn.commit()  # save changes in sql
        print("Message sent successfully")
        user_menu()
    except Exception as e:
        clear_terminal()
        print(e)
        user_menu()  # all operations related to users

def display_inbox():
    try:
        clear_terminal()
        welcome()  # welcome msg
        query = "Select * from conversation where receiver = '{}'".format(current_user)  # select all values from table users
        cur.execute(query)  # execute query in sql
        # convert to dataframe
        df = pd.DataFrame(cur.fetchall(), columns=['s_no','date','time','sender','receiver','msg'])

        face_auth()
        if authentication:
            df['msg'] = df['msg'].apply(lambda x: decrypt_text(x, shift_value))  # Decrypt each message
        print(df)  # display values of all users
        cn.commit()  # save changes in sql
        print(" \n msg  obtained successfully \n ")
        user_menu()  # display values of users

    except Exception as e:
        clear_terminal()
        print(e)
        user_menu()  # all operations related to users

def p_inbox():
    try:
        clear_terminal()
        welcome()  # welcome msg
        query = "Select * from conversation where receiver = 'everyone'"  # select all values from table users
        cur.execute(query)  # execute query in sql
        
        # convert to dataframe
        df = pd.DataFrame(cur.fetchall(), columns=['s_no','date','time','sender','receiver','msg'])

        face_auth()
        if authentication:
            df['msg'] = df['msg'].apply(lambda x: decrypt_text(x, shift_value))  # Decrypt each message
        print(df)  # display values of all users
        cn.commit()  # save changes in sql
        print(" \n user Details obtained successfully \n ")
        user_menu()  # display values of users

    except Exception as e:
        clear_terminal()
        print(e)
        user_menu()  # all operations related to users

def encrypt_text(msg, shift):
    encrypted_msg = ''.join([chr(ord(char) + shift) for char in msg])
    return encrypted_msg

def decrypt_text(encrypted_msg, shift):
    decrypted_text = ''.join([chr(ord(char) - shift) for char in encrypted_msg])
    return decrypted_text

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

homepage()