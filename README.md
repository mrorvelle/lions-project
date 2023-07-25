# lions-project

## Overview of the project
This project required using 2+ free, random APIs to generate data in Python and perform some sql analysis.

APIs used were RandomUser and Agify.

## Strategy for Development

#### Data Storage
Sqlite was used to store data due to the sqlite package being built in to Python and it being a lightweight and accessible storage solution.

#### Structure
Methods have been split into DB and People helper files to enhance the user experience. The people_helpers.py file exists to gather and transform the people data as a mini-ETL job. The db_helpers.py exists to connect to and manage the actual strructure of the sqlite db used for storage.

This structure allows for merely running the app.py script to handle the totality of the project.

#### Running the App
1. Clone the repository to your local machine and navigate to the project directory
```
git clone https://github.com/mrorvelle/lions-project.git
cd lions-project
```
2. Install requirements.txt
```
python3 -m pip install requirements.txt
```
3. Run the application
python3 app.py

NOTE: If prompted to install additional packages, do so by running
```
python3 -m pip install [package_name]
```

#### SQL Queries Used

1. This query is used to calculate teh share of foreign fans in the database for international efforts/reporting. Its results will appear very high due to the nature of the fake/random data
```
SELECT count_foreign_fans,
       Round(( count_foreign_fans * 100.0 ) / total_fans, 2) AS PERCENT
FROM   (SELECT Sum(CASE
                     WHEN location_country != 'United States' THEN 1
                     ELSE 0
                   END)          AS count_foreign_fans,
               Count(name_first) AS total_fans
        FROM   people) 
```

2. This query finds the fan located the most miles from the geographic coordinates of ford field (as determined during an ETL step in python)
```
SELECT name_first,
       name_last,
       Round(distance_from_ford, 2)
FROM   people
ORDER  BY distance_from_ford DESC
LIMIT  1 
```

3. This query groups fans into three buckets based on dob_age field from RandomUser API
```
SELECT Sum(CASE
             WHEN dob_age > 70 THEN 1
             ELSE 0
           END) AS 'Over 70',
       Sum(CASE
             WHEN dob_age < 30 THEN 1
             ELSE 0
           END) AS 'Under 30',
       Sum(CASE
             WHEN dob_age <= 70
                  AND dob_age >= 30 THEN 1
             ELSE 0
           END) AS 'Between 30-70'
FROM   people 
```

4. This query breaks down the Lions fans by gender
```
SELECT Sum(CASE
             WHEN gender = 'male' THEN 1
             ELSE 0
           END) AS 'Male',
       Sum(CASE
             WHEN gender = 'female' THEN 1
             ELSE 0
           END) AS 'Female'
FROM   people 
```

5. This query leverages a join to a names table and a sub-query to do a quick DQ check by comparing the predicted vs. actual age of fans
```
SELECT Round(Avg(difference), 2) AS diff_avg
FROM   (SELECT p.name_first,
               p.dob_age,
               n.age,
               Abs(n.age - p.dob_age) AS difference
        FROM   people p
               JOIN names n
                 ON p.name_first = n.NAME) 
```