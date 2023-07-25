import requests
import logging
import sqlite3
import pandas as pd


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

def predict_age(name, cur):
    print(name)
    response = requests.get(f'https://api.agify.io?name={name}')
    res = cur.execute(f"SELECT age FROM name where name = {name}")
    print(res.fetchone())
    if len(res) > 0:
        logger.info(f'Age already predicted for {name}. Returning previous result to limit API calls.')
        return res.fetchone()
    else:
        return response.json()['age']

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')
logger = logging.getLogger('logger')

logger.info(f"Logger instantiated. Beginning query of RandomUser")

num_of_people = 10
people = pd.json_normalize(requests.get(f'https://randomuser.me/api/?results={num_of_people}').json()['results'])
people['predicted_age'] = ''
# flatten produce . delimited headers. change to _ for standardization
people.columns = people.columns.str.replace(".", "_")

conn = create_connection('db.sqlite')

# Get predicted ages
create_table_sql = """ CREATE TABLE names AS 
name text PRIMARY KEY, 
age integer
"""
create_table(conn, create_table_sql)
for i in people.index:
    people.at[i, 'predicted_age'] = predict_age(people.at[i,'name_first'], conn)


# now we need to store people results in DB

people.to_sql('people',conn,if_exists='replace',index=False)

# predict income by zip code by going through each line and if United States, running below, otherwise returning unknown
#pd.json_normalize()

