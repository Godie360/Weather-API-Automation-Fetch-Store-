
import requests
import json
import sqlite3
from datetime import datetime

# creating a SQLite connection 
def create_connection(database):
    connection = None
    try:
        connection = sqlite3.connect(database)
        return connection, connection.cursor()
    except sqlite3.Error as e:
        print("Error creating connection:", e)
        if connection:
            connection.close()
        return None, None

#inserting data into the table
def insert_data(cursor, temperature, weather_text, date, location):
    try:
        cursor.execute('INSERT INTO weather_data (temperature, weather_text, date, location) VALUES (?, ?, ?, ?)',
                       (temperature, weather_text, date, location))
    except sqlite3.Error as e:
        print("Error inserting data:", e)

#commiting changes and close the connection
def commit_and_close(connection):
    if connection:
        connection.commit()
        connection.close()

# API key and location details
api_key = 'B4P8JpQGXhOPtZTnHFlPVIebKQr87g54'
location_key = '313616'
url = f'http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}'

# Make a request to the AccuWeather API
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    try:
        # Parse the JSON response
        data = response.json()

        # Check if the response is a non-empty list
        if data and isinstance(data, list) and len(data) > 0:
            # Extract temperature, weather text, date, and location from the response
            temperature = data[0]['Temperature']['Metric']['Value']
            weather_text = data[0]['WeatherText']
            date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')  # Use UTC time for consistency
            location = f"{data[0]['LocalizedName']}, {data[0]['Region']['LocalizedName']}, {data[0]['Country']['LocalizedName']}"

            # Create a connection and cursor to the SQLite database
            connection, cursor = create_connection('model/weather_database.db')

            # Check if connection and cursor were successfully created
            if connection and cursor:
                # Insert the temperature, weather text, date, and location into the table
                insert_data(cursor, temperature, weather_text, date, location)

                # Commit changes and close the connection
                commit_and_close(connection)

                print("Data successfully inserted into the database.")
            else:
                print("Error creating connection or cursor.")
        else:
            print("Invalid response format or empty data.")
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
else:
    print("Request failed with status code:", response.status_code)
