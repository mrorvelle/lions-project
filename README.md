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