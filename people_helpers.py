import requests
import haversine as hs
import logging
import pandas as pd
from db_helpers import create_connection, create_table

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')
logger = logging.getLogger('logger')
db_file = 'db.sqlite'

def predict_age(name_passed, conn):

    cur = conn.cursor()
    res = cur.execute(f"SELECT age FROM names where name = ?", (name_passed,)).fetchone()
    if res is not None:
        logger.info(f"Ope! Found an existing age for {name_passed}. Will not ping API for name again.")
        return res[0]
    else:
        response = requests.get(f'https://api.agify.io?name={name_passed}')
        if response.json().get('age') is not None:
            cur.execute(f"INSERT INTO names VALUES (?,?)", (str(name_passed), int(response.json()['age'])))
        return response.json().get('age')

def distance_from_ford_field(lat,long):
    ford_field=(42.3400,83.0456)
    person=(float(lat),float(long))
    return hs.haversine(ford_field,person)

def retrieve_people_data(num_of_people, conn):
    logger.info(f"retrieving {num_of_people} from RandomUser")
    people = pd.json_normalize(requests.get(f'https://randomuser.me/api/?results={num_of_people}').json()['results'])
    people.columns = people.columns.str.replace(".", "_")
    people['distance_from_ford'] = ''
    people_enhanced = supplement_people_data(people, conn)

    logger.info(f"Loading people into database for analysis")
    people_enhanced.to_sql('people', conn, if_exists='replace', index=False)

    return people_enhanced

def supplement_people_data(people, conn):
    logger.info("supplementing people data with predicted age and distance from Ford Field.")
    for i in people.index:
        # check and populate name/age table
        predict_age(people.at[i,'name_first'], conn)
        # get distance from ford field
        people.at[i,'distance_from_ford'] = distance_from_ford_field(people.at[i,'location_coordinates_latitude'],people.at[i,'location_coordinates_longitude'])*.621371
    return people