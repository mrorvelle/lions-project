import requests
import logging
import json
import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(e)

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')
logger = logging.getLogger('logger')

logger.info(f"Logger instantiated. Beginning query of RandomUser")

num_of_people = 1
people = requests.get(f'https://randomuser.me/api/?results={num_of_people}').json()['results']



conn = create_connection('db.sqlite')

if conn is not None:
        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS people (
                                        id text PRIMARY KEY,
                                        f_name text NOT NULL,
                                        l_name text NOT NULL,
                                        title text,
                                        gender text,
                                        email text,
                                        street_number text,
                                        street_name text,
                                        city text,
                                        state text,
                                        country text,
                                        zip_code text
                                    ); """
        
        # create projects table
        create_table(conn, sql_create_projects_table)

else:
    print("Error! cannot create the database connection.")