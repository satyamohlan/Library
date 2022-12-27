# Importing and Connecting to SQL Database
import pymysql as sql
db = sql.connect(
    host='localhost',
    user='admin2077',
    password='Satyam@2005',
    database='library')
mycursor = db.cursor()
# Login using Username and Password:
print('Welcome to Epsilon Book Issuing Services!')
admin = input('Enter Admin Username: ')
admin_password = input('Enter Admin Password: ')
# Searching for User with matching Username and Password in the Database
mycursor.execute('SELECT name,admin_id from admins WHERE admin_id="{admin}" AND password="{password}"'.format(
    admin=admin, password=admin_password))
app_user = mycursor.fetchone()
# If user is not undefined, start the program
if(app_user != None):
    print('Welcome %s!' % (app_user[0]))
    while True:
        print('Press 1 to issue/Un-Issue a book \nPress 2 to See All-TIme/Yearly/Monthly Stats \nPress 3 to See Overdue issued books \nPress 4 to Exit')
        act1 = int(input('Enter Your Action: '))
        if(act1 == 1):
            student = input('Enter ID of the Student: ')
            # Verfying if the Student Id Entered Exists or Not
            mycursor.execute(
                'SELECT * FROM student WHERE student_id=%s ' % (student))
            issue_student = mycursor.fetchone()
            if(issue_student != None):
                print('Name Of Student: %s \nClass Of student: %s \nAdmission Number of Student: %s' % (
                    issue_student[1], issue_student[2], issue_student[0]))
                mycursor.execute(
                    "SELECT * FROM issues WHERE student_id=%s AND returned='NO' " % (student))
                issued_books = mycursor.fetchall()
                if(issued_books != None):
                    print('Books Currently Issued to Student: ')
                    for x in issued_books:
                        mycursor.execute(
                            "SELECT * from books where book_id=%s" % x[2])
                        book = mycursor.fetchone()
                        print(book)
                while True:
                    print('Press 1 to Issue a Book \nPress 2 to Un-issue an Earlier Book \nPress 3 to Explore Book Catalogue by Name/Author \nPress 4 to Exit ')
                    act2 = int(input('Enter Your Action: '))

                    if(act2 == 1):
                        mycursor.execute(
                            "SELECT * FROM issues WHERE student_id=%s and returned='NO'" % (student))
                        issued_books = mycursor.fetchall()
                        if(len(issued_books) < 2):
                            book = input(
                                'Enter ID of the Book You Want to Issue: ')
                            mycursor.execute(
                                'SELECT * from books where book_id=%s' % book)
                            issue_book = mycursor.fetchone()
                            if(issue_book != None):
                                print(issue_book)
                                Final_signal = input(
                                    'Do You Want to Issue the Following book?(Y/N) ').lower()
                                if(Final_signal in ['y', 'yes']):
                                    try:
                                        mycursor.execute("INSERT INTO issues(student_id,book_id,issued_by) VALUES('%s',%s,'%s')" % (
                                            issue_student[0], issue_book[0], app_user[1]))
                                        db.commit()
                                    except sql.Error as error:
                                        print(
                                            "Something went wrong: {}".format(error))
                                    else:
                                        print('Book Issued Successfully!\n')

                                elif(Final_signal in ['n', 'no']):
                                    print('OK')
                                else:
                                    print('Input Not Understood.')
                            else:
                                print('No Book With Following Code Exists')
                        else:
                            print(
                                'Student Cannot have more than 2 books Issued at the same time.')
                    elif(act2 == 2):
                        unissue = int(
                            input('Enter Book Code for the book to be Returned: '))

                        print("Returning Book...\n")
                        mycursor.execute("UPDATE issues SET returned='YES' where student_id='%s' and book_id='%s'" % (
                            issue_student[0], unissue))
                        db.commit()
                    elif(act2 == 3):
                        print(
                            'Genres available: Tech, Science, Non-Fiction, Fiction, Philosophy')
                        genre = input(
                            'Enter the Term You want to Search/Genre You want to Explore: ').lower()
                        mycursor.execute(
                            "SELECT * FROM books WHERE genre='{genre}'or book_name like '%{genre}%';" .format(genre=genre))
                        list = mycursor.fetchall()
                        print('\n'.join('{}: {}'.format(*val)
                                        for val in enumerate(list)))
                    elif(act2 == 4):
                        print('Exiting...\n')
                        break
            else:
                print('No Student with Following Admission Number')
        elif(act1 == 3):
            mycursor.execute(
                "SELECT * FROM issues where returned!='YES' AND TIMESPAN<NOW()")
            overdue_books = mycursor.fetchall()
            for x in overdue_books:
                mycursor.execute(
                    "SELECT * from books where book_id=%s" % x[2])
                overdue_book = mycursor.fetchone()
                mycursor.execute(
                    "SELECT * from student where student_id=%s" % x[1])
                overdue_student = mycursor.fetchone()
                print('Overdue Books:')
                print(overdue_book)
                print('Issue ID:{ID}    Issued To:{Student}     Issued By:{Admin}       Overdue Since:{Date}'.format(
                    ID=x[0], Student=str(overdue_student[1])+' '+str(overdue_student[2]), Admin=x[4], Date=x[5]))

        elif act1 == 4:
            print('Thank You for Visiting Us!')
            break

else:
    print('Wrong Password/Username Entered')
