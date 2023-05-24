import urllib.request
import json
from dotenv import load_dotenv
import os

load_dotenv()

# OpenWeather API key and base endpoint URL
base_url = 'https://api.openweathermap.org/data/2.5/weather?'
API_KEY = os.getenv('TOKEN')

# Import Australian city data from JSON file
file = open('au-coor.json', 'r')
city_data = json.load(file)
file.close()

# Create list of city names for input validation
city_list = []
for i in city_data:
    city_list.append(i['city'].lower())

print("\n|----- Australian Cities Weather Lookup -----|")

while True:
    print("Type in name of city and select state to get\ncurrent weather information. Type 'q' to quit")
    city = input("> ").lower()

    if city == 'q':
        break

    elif city in city_list:
        cities = []
        for item in city_data: # Iterate through all cities to find cities that match input and append to list
            if city == item['city'].lower():
                cities.append(item)

        # Print list of cities found
        print("\nCities found")
        for index, city in enumerate(cities, 1):
            print(f"{index}. {city['city']}, {city['admin_name']}")


        # Get latitude & longitude base on selection number
        selection = int(input("\nType city number to get weather data\n> "))
        for index, city in enumerate(cities, 1):
            if index == selection:
                lat = city['lat']
                lon = city['lng']
                city_name = f"{city['city']}, {city['admin_name']}"

        # Make API call and store retrieved data as JSON
        complete_url = base_url + f"lat={lat}&lon={lon}&appid={API_KEY}"
        response = urllib.request.urlopen(complete_url)
        data = response.read()
        data = json.loads(data)


        if data['cod'] != '404':
            main = data['main']

            # Define variables for desired weather information
            temp_current = round(main['temp'] - 273.15, 2)
            temp_min = round(main['temp_min'] - 273.15, 2)
            temp_max = round(main['temp_max'] - 273.15, 2)
            pressure = main['pressure']
            humidity = main['humidity']

            print(f'''
                City:\t{city_name}
                Current Temperature:\t{temp_current} C
                Minimum Temperature:\t{temp_min} C
                Maximum Temperature:\t{temp_max} C
                Pressure:\t\t{pressure} hPa
                Humidity:\t\t{humidity} %
            ''')

    else:
        print("Invalid city\n")

exit()