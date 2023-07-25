import sqlite3

def create_age_table(conn):
    create_table_sql = """ CREATE TABLE IF NOT EXISTS names (
    name text PRIMARY KEY, 
    age integer
    )
    """
    create_table(conn, create_table_sql)

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

def query1(conn, doc):
    print(f'\n{doc["query1"]["description"]}\n\nKeep in mind - this is random data so it will be a high percentage.')
    res = conn.execute(doc["query1"]["query"])
    tuple_result = res.fetchall()[0]
    print(f"\nTOTAL FOREIGN FANS: {tuple_result[0]}")
    print(f"\nPERCENTAGE FOREIGN FANS: {tuple_result[1]}\n")
    return True

def query2(conn, doc):
    print(f'\n{doc["query2"]["description"]}')
    res = conn.execute(doc["query2"]["query"])
    tuple_result = res.fetchall()[0]
    print(f"\nTEH FARTHEST FANS IS: {tuple_result[0]} {tuple_result[1]} AT {tuple_result[2]} MILES AWAY FROM FORD FIELD.\n")

def query3(conn, doc):
    print(f'\n{doc["query3"]["description"]}')
    res = conn.execute(doc["query3"]["query"])
    tuple_result = res.fetchall()[0]
    print(f"\nFANS OVER 70: {tuple_result[0]}\nFANS UNDER 30: {tuple_result[1]}\nFANS BETWEEN 30-70: {tuple_result[2]} \n")

def query4(conn, doc):
    print(f'\n{doc["query4"]["description"]}')
    res = conn.execute(doc["query4"]["query"])
    tuple_result = res.fetchall()[0]
    print(f"\nMEN: {tuple_result[0]}\nWOMEN: {tuple_result[1]}\n\n")

def query5(conn, doc):
    print(f'\n{doc["query5"]["description"]}')
    res = conn.execute(doc["query5"]["query"])
    tuple_result = res.fetchall()[0]
    print(f"\nAVG DIFFERENCE IN AGE IN YEARS: {tuple_result[0]}\n\n")
