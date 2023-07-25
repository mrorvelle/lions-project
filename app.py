from db_helpers import create_age_table, create_connection
from people_helpers import retrieve_people_data
from sqlite3 import OperationalError

"""
To begin, we must extract data form the RandomUser API. Once extracted, we supplement the data in 2 ways:

1) We use the Agify.io API to predict a person's age based on their first name. 
    NOTE: If we already know a person's predicted age from a previous API call, we will NOT re-call 
    the API to save time and (theoretical) money.
2) We use haversine package to calculate the distance of each person's latitude and longitude from Ford Field in miles.
    NOTE: Unfortunately, the latitude and longitude values from RandomUser do not correspond to the person's listed 
    address it provides, so haversine produces unusual results often.

"""

### Produce and/or append to two tables: people and names ###
num_of_people = 200

conn = create_connection('db.sqlite')
people = retrieve_people_data(num_of_people, conn)
create_age_table(conn)


"""
Now, let's analyze some of our data using SQL. We have a file (sql_queries.sql) that contains our queries.
As we cycle through these queries, we will print a description of the query being run, and insights/results gathered.

"""

# Open and read the file and then split by ; delimiter
fd = open('sql_queries.sql', 'r')
sqlFile = fd.read()
fd.close()
commands = sqlFile.split(';')

# Query 1
res = conn.execute(commands[0])
res.fetchall()

conn.close()
