import json
import os
import mysql.connector
from source.utilities import rand_fun
from mysql.connector import errorcode

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


def grab_config():
    # Getting configuration from json file.
    with open(os.path.join(os.getcwd(), r'utilities\config.json')) as f:
        conf = json.load(f)
    return conf


def grab_sql():
    # Getting SQL query from txt file.
    with open(os.path.join(os.getcwd(), r'utilities\sql.txt')) as f:
        sql = f.readline()
        print(sql)
    return sql


def db_start(cnx, tables, db_name):
    """
    Creating database if it not already exists.

    Parameters
    ----------
    cnx : mysql.connector.cursor
        Cursor to interface with MySQL database
    tables : dict
        Ditcionary that represents DB structure intnded to use with app
    db_name : str
        Name of database to be created or used in MySQL database
    Returns
    -------
    None
    """
    cursor = cnx.cursor()

    def create_database(cursor):
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8mb4'".format(db_name))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    try:
        cursor.execute("USE {}".format(db_name))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(db_name))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(db_name))
            cnx.database = db_name
        else:
            print(err)
            exit(1)
    for table_name in tables:
        table_description = tables[table_name]
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
    """
    Filling database with pre-determined number of objects.

    Parameters
    ----------
    cnx : mysql.connector.cursor
        Cursor to interface with MySQL database.
    n : int
        Number of objects to be added to database.
    Returns
    -------
    None
    """
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
