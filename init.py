import mysql.connector as sql
import csv
db = sql.connect(
    host='localhost',
    user='admin2077',
    password='Satyam@2005',
    database='library'
)
mycursor = db.cursor(buffered=True)
books = []
mycursor.execute('CREATE DATABASE library')
mycursor.execute('DROP TABLE admins')
mycursor.execute('DROP TABLE student')
mycursor.execute('DROP TABLE books')
mycursor.execute('DROP TABLE issues')


mycursor.execute(
    'CREATE TABLE admins(admin_id varchar(30) unique NOT NULL,name  VARCHAR(20) NOT NULL,password varchar(30) NOT NULL);')
mycursor.execute(
    'CREATE TABLE student(student_id varchar(30) unique NOT NULL,name  VARCHAR(20) NOT NULL ,class_no smallint UNSIGNED NOT NULL, PRIMARY KEY(student_id));')

mycursor.execute(
    'CREATE TABLE books(book_id INT auto_increment,book_name  VARCHAR(60) NOT NULL,genre varchar(20) default "other",sub_genre varchar(100),author varchar(30),book_length SMALLINT UNSIGNED, PRIMARY KEY(book_id));')

mycursor.execute(
    'CREATE TABLE issues(issue_id INT auto_increment,student_id varchar(30) NOT NULL,FOREIGN KEY(student_id) REFERENCES student(student_id),book_id INT unique NOT NULL,FOREIGN KEY(book_id) REFERENCES books(book_id),issued_on DATETIME NOT NULL default now(),issued_by varchar(30) NOT NULL,FOREIGN KEY(issued_by) REFERENCES admins(admin_id),PRIMARY KEY(issue_id));')


# mycursor.execute('DESCRIBE issues')
# for x in mycursor:
#     print(x)
y = int(input("Enter Number oF Admins to be registered"))
for x in range(y):
    id = input('Enter the ID for user {no}: '.format(no=x+1))
    name = input('Enter the Name for user {no}: '.format(no=x+1))
    password = input('Enter the Password for user {no}: '.format(no=x+1))
    mycursor.execute(
        'INSERT INTO admins VALUES("{id}","{name}","{password}");'.format(id=id, name=name, password=password))
mycursor.execute('select * from admins')
for x in mycursor:
    print(x)
y = int(input("Enter Number oF Students to be registered"))
for x in range(y):
    id = input('Enter the ID for user {no}: '.format(no=x+1))
    name = input('Enter the Name for user {no}: '.format(no=x+1))
    class_no = int(input('Enter the Class for user {no}: '.format(no=x+1)))
    mycursor.execute(
        'INSERT INTO student(student_id,name,class_no) VALUES("{id}","{name}",{class_no});'.format(id=id, name=name, class_no=class_no))
mycursor.execute('select * from student')
for x in mycursor:
    print(x)

with open('books_new.csv', 'r') as f1:
    fileReader = csv.reader(f1)
    next(fileReader)
    for row in fileReader:
        mycursor.execute(
            'INSERT INTO books(book_name,genre,sub_genre,author,book_length) VALUES("{name}","{genre}","{subgenre}","{author}","{book_length}");'.format(name=row[0], genre=row[2], subgenre=row[3], author=row[1], book_length=row[4]))
mycursor.execute('select * from books')
for x in mycursor:
    print(x)
db.commit()
