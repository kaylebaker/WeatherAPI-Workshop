import urllib.request
import json
import tkinter as tk

class App(tk.Tk): # Define App class that inherits from tk.Tk class
    def __init__(self):
        super().__init__() # Call the __init__() method of the tk.Tk class

        self.API_KEY = ''
        self.base_url = 'https://api.openweathermap.org/data/2.5/weather?'

        # Read in data of Australian cities from json file
        self.file = open('au-coor.json', 'r')
        self.data = json.load(self.file)
        self.file.close()

        # Create list of Australian cities for listbox
        self.city_list = []
        for item in self.data:
            self.city_list.append(item['city'] + ', ' + item['admin_name'])

        # Function that update listbox data based on typed input
        def check_key(event):

            value = event.widget.get()

            # get data from listbox
            if value == '':
                data = self.city_list
            else:
                data = []
                for item in self.city_list:
                    if value.lower() in item.lower():
                        data.append(item)

            # update data in listbox
            update(data)

        def update(data):

            # clear previous data from listbox
            self.lb.delete(0, 'end')

            # put new data
            for item in data:
                self.lb.insert('end', item)


        def on_button_press():

            # Get selected index and store as string 'selected_item'
            selected_index = self.lb.curselection()
            selected_item = self.lb.get(selected_index)
            
            # Change label to read the city/state of data displayed
            self.result_label.config(text="Showing current weather details for " + selected_item)

            # Get the coordinates of the selected city
            x = selected_item.split(',')
            city = x[0].strip()
            state = x[1].strip()
            for item in self.data:
                if item['city'] == city and item['admin_name'] == state:
                    lat = item['lat']
                    lon = item['lng']

            # Make API call and store retrieved data as JSON
            complete_url = self.base_url + f"lat={lat}&lon={lon}&appid={self.API_KEY}"
            response = urllib.request.urlopen(complete_url)
            returned_data = response.read()
            results = json.loads(returned_data)

            # Delete existing data in output boxes
            self.results_left.delete('1.0', 'end')
            self.results_right.delete('1.0', 'end')

            # Retrieve weather data and store in variables
            main = results['main']

            temp_current = round(main['temp'] - 273.15, 2) # Subtract 273.15 to convert from F to C
            temp_feels = round(main['feels_like'] - 273.15, 2)
            temp_min = round(main['temp_min'] - 273.15, 2)
            temp_max = round(main['temp_max'] - 273.15, 2)
            pressure = main['pressure']
            humidity = main['humidity']
            wind_speed = round(results['wind']['speed'] * 1.609) # Multiply by 1.609 tp convert from mph to kmh
            cloud_cover = results['clouds']['all']

            # Display results in left box
            self.results_left.insert('1.0', "Current Temp: " + str(temp_current) + " C\n")
            self.results_left.insert('2.0', "Feels Like:   " + str(temp_feels) + " C\n")
            self.results_left.insert('3.0', "Minimum Temp: " + str(temp_min) + " C\n")
            self.results_left.insert('4.0', "Maximum Temp: " + str(temp_max) + " C\n")

            # Display results in right box
            self.results_right.insert('1.0', "Pressure:    " + str(pressure) + " hPa\n")
            self.results_right.insert('2.0', "Humidity:    " + str(humidity) + "%\n")
            self.results_right.insert('3.0', "Wind Speed:  " + str(wind_speed) + " kph\n")
            self.results_right.insert('4.0', "Cloud Cover: " + str(cloud_cover) + "%\n")

        # Configure the root window
        self.title("OpenWeather API GUI")
        self.geometry("400x350")

        # Frames
        self.top_frame = tk.Frame(self)
        self.top_frame.pack()
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.pack(pady=(30, 0))

        # Labels for top_frame
        self.title_label = tk.Label(self.top_frame, justify='center', text="Australian City Weather Data")
        self.title_label.pack()
        self.subtitle_label = tk.Label(self.top_frame, justify='center', text="using OpenWeather API")
        self.subtitle_label.pack(pady=(0, 20))

        # List and Button for top_frame
        self.search_entry = tk.Entry(self.top_frame, width=30)
        self.search_entry.pack(anchor=tk.W)
        self.search_entry.bind('<KeyRelease>', check_key)
        self.list1 = tk.StringVar(value=self.city_list)
        self.lb = tk.Listbox(self.top_frame, width=30, height=5, listvariable=self.list1)
        self.lb.pack(side='left')
        update(self.city_list)
        self.get_button = tk.Button(self.top_frame, text="Get Weather", command=on_button_press)
        self.get_button.pack(side='left', padx=20)

        # Labels for bottom_frame
        self.result_label = tk.Label(self.bottom_frame, text="Showing current weather details for {city}")
        self.result_label.pack(anchor=tk.W)

        # TextBox widgets for bottom_frame
        self.results_left = tk.Text(self.bottom_frame, width=22, height=6)
        self.results_left.pack(side='left', pady=20, padx=5)
        self.results_right = tk.Text(self.bottom_frame, width=22, height=6)
        self.results_right.pack(side='left', pady=20, padx=5)

if __name__ == "__main__":
    app = App()
    app.mainloop()
