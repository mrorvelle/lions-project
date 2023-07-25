from db_helpers import create_age_table, create_connection, query1, query2, query3, query4, query5
from people_helpers import retrieve_people_data
import yaml


"""
To begin, we must extract data form the RandomUser API. Once extracted, we supplement the data in 2 ways:

1) We use the Agify.io API to predict a person's age based on their first name. 
    NOTE: If we already know a person's predicted age from a previous API call, we will NOT re-call 
    the API to save time and (theoretical) money.
2) We use haversine package to calculate the distance of each person's latitude and longitude from Ford Field in miles.
    NOTE: Unfortunately, the latitude and longitude values from RandomUser do not correspond to the person's listed 
    address it provides, so haversine produces unusual results often.

"""

# Produce and/or append to two tables: people and names
num_of_people = 200

conn = create_connection('db.sqlite')
people = retrieve_people_data(num_of_people, conn)
create_age_table(conn)



"""
Now, let's analyze some of our data using SQL. We have a file (sql_queries.yml) that contains our queries.
As we cycle through these queries, we will print a description of the query being run, and insights/results gathered in terminal.

"""

# Open and read the yml file of queries to pass to our db_helpers
with open('sql_queries.yml', 'r') as f:
    doc = yaml.load(f, Loader=yaml.FullLoader)

for i in range(1,6):
    successful = False
    while not successful:
        if input(doc[f'query{i}']['prompt']).lower() in ['y','yes']:
            if i == 1:
                query1(conn, doc)
            elif i ==2:
                query2(conn, doc)
            elif i == 3:
                query3(conn, doc)
            elif i == 4:
                query4(conn, doc)
            elif i == 5:
                query5(conn, doc)
            successful = True
    continue



conn.close()