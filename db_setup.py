import mysql.connector
import rand_fun
import json
from mysql.connector import errorcode


def grab_config():
    with open('config.json') as f:
        conf = json.load(f)
    return conf

def grab_sql():
    with open('sql.txt') as f:
        sql = f.readline()
        print(sql)
    return sql


def db_start(cnx, TABLES, DB_NAME):
    cursor = cnx.cursor()

    def create_database(cursor):
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8mb4'".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")


def fill_in_db(cnx, n=100):
    cursor = cnx.cursor()
    add_employee = ("INSERT INTO employees "
                    "(firstname, lastname, hiredate, gender, birthdate) "
                    "VALUES (%s, %s, %s, %s, %s)")
    add_salary = ("INSERT INTO salaries "
                  "(empno, salary, fromdate, todate, commentary) "
                  "VALUES (%(empno)s, %(salary)s, %(fromdate)s, %(todate)s,%(commentary)s)")
    add_title = ("INSERT INTO titles "
                 "(empno, title, fromdate, todate,lotterychance,description) "
                 "VALUES (%(empno)s, %(title)s, %(fromdate)s, %(todate)s,%(lotterychance)s,%(description)s)")
    for _ in range(n):
        cursor.execute(add_employee, rand_fun.random_employee())
        empno = cursor.lastrowid
        cursor.execute(add_salary, rand_fun.random_salary(empno))
        cursor.execute(add_title, rand_fun.random_titles(empno))
        cnx.commit()


# config = {
#   'user': 'root',
#   'password': 'order66',
#   'host': '127.0.0.1',
#   'raise_on_warnings': True
# }

DB_NAME = 'hr'

TABLES = {'employees': (
    "CREATE TABLE `employees` ("
    "  `empno` int(11) NOT NULL AUTO_INCREMENT,"
    "  `birthdate` date NOT NULL,"
    "  `firstname` varchar(14) NOT NULL,"
    "  `lastname` varchar(20) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `hiredate` date NOT NULL,"
    "  PRIMARY KEY (`empno`)"
    ") ENGINE=InnoDB"), 'salaries': (
    "CREATE TABLE `salaries` ("
    "  `empno` int(11) NOT NULL,"
    "  `salary` float(11) NOT NULL,"
    "  `fromdate` date NOT NULL,"
    "  `todate` date NOT NULL,"
    "  `commentary` varchar(50) NOT NULL,"
    "  PRIMARY KEY (`empno`,`fromdate`), KEY `empno` (`empno`),"
    "  CONSTRAINT `salaries_ibfk_1` FOREIGN KEY (`empno`) "
    "     REFERENCES `employees` (`empno`) ON DELETE CASCADE"
    ") ENGINE=InnoDB"), 'titles': (
    "CREATE TABLE `titles` ("
    "  `empno` int(11) NOT NULL,"
    "  `title` varchar(50) NOT NULL,"
    "  `fromdate` date NOT NULL,"
    "  `todate` date DEFAULT NULL,"
    "  `lotterychance` float(11) NOT NULL,"
    "  `description` varchar(50) NOT NULL,"
    "  PRIMARY KEY (`empno`,`title`,`fromdate`), KEY `empno` (`empno`),"
    "  CONSTRAINT `titles_ibfk_1` FOREIGN KEY (`empno`)"
    "     REFERENCES `employees` (`empno`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")}
