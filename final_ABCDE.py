import tkinter as tk
from graphics import *
def validate_date_input():
    """
    Prompts the user for a date in DD MM YYYY format, validates each input one by one:
    - Correct data type
    - Correct range for day, month, and year
    """
    try:
        while True:
            try:
                date = input("Please enter the day of the survey in the format DD: ")
                if not date.isdigit():
                    print("Integer required for day. Please try again.")
                    continue
                date = int(date)
                if not (1 <= date <= 31):
                    print("Out of range - day must be between 1 and 31.")
                    continue
            except:
                print("Invalid input for day.")
                continue
            break 

        while True:
            try:
                month = input("Please enter the month of the survey in the format MM: ")
                if not month.isdigit():
                    print("Integer required for month and Follow the MM format, Please try again.")
                    continue
                month = int(month)
                if not (1 <= month <= 12):
                    print("Out of range - month must be between 1 and 12.")
                    continue
            except:
                print("Invalid input for month.")
                continue
            break

        while True:
            try:
                year = input("Please enter the year of the survey in the format YYYY: ")
                if not year.isdigit():
                    print("Integer required for year. Please try again.")
                    continue
                year = int(year)
                if not (2000 <= year <= 2024):
                    print("Out of range - year must be between 2000 and 2024.")
                    continue
            except:
                print("Invalid input for year.")
                continue
            break
    except Exception as e:
        print("Error: {e}") 

    return date, month, year

def validate_continue_input():
    while True:
        answer = input("Do you want to process another csv file? Y/N: ")
        if answer.upper() == "Y":
            main()
        break
        



def process_csv_data(file_path):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """

    try:
        traffic_data = {
            "total_vehicles": 0,
            "trucks": 0,
            "electric": 0,
            "bicycles": 0,
            "two_wheeled": 0,
            "vehicles_out": 0,
            "vehicles_straight": 0,
            "over_speed": 0,
            "vehicles_elm": 0,
            "vehicles_hanley": 0,
            "scooters": 0,
            "rain": 0,
            "percentage_truck": 0,
            "bicycle_per_hour": 0,
            "scooter_percentage": 0,
            "hours": {},
            "Elm":{}, 
            "Hanley":{},
            "most_vehicles_hour": 0,
            "peak_hours": [],
            "peak_str": []
        }
        total = 0
        rain_hours = []

        with open(file_path, 'r') as file:
            # Read lines and split data manually
            lines = file.readlines()
            headers = lines[0].strip().split(",")  # First line contains headers
            for line in lines[1:]:  # Iterate through the rest of the lines
                values = line.strip().split(",")  # Split each line by commas
                row = dict(zip(headers, values))  # Create a dictionary of column-value pairs after completing the zip function which makes it to tuples

                if row["VehicleType"]:
                    traffic_data["total_vehicles"] += 1
                    if row["elctricHybrid"].lower() == "true":
                        traffic_data["electric"] += 1
                    if row["VehicleType"] == "Truck":
                        traffic_data["trucks"] += 1
                    if row["VehicleType"] == "Bicycle":
                        traffic_data["bicycles"] += 1
                    if row["VehicleType"] in ["Scooter", "Motorcycle", "Bicycle"]:
                        traffic_data["two_wheeled"] += 1
                    if row["JunctionName"] == "Elm Avenue/Rabbit Road" and row["travel_Direction_out"] == "N" and row["VehicleType"] == "Buss":
                        traffic_data["vehicles_out"] += 1
                    if row["JunctionName"] == "Elm Avenue/Rabbit Road" or row["JunctionName"] == "Hanley Highway/Westway":
                        if row["travel_Direction_in"] == row["travel_Direction_out"]:
                            traffic_data["vehicles_straight"] += 1
                    if row["VehicleSpeed"] and row["JunctionSpeedLimit"]:
                        if float(row["VehicleSpeed"]) > float(row["JunctionSpeedLimit"]):
                            traffic_data["over_speed"] += 1
                    if row["JunctionName"] == "Elm Avenue/Rabbit Road":
                        traffic_data["vehicles_elm"] += 1
                    if row["JunctionName"] == "Hanley Highway/Westway":
                        traffic_data["vehicles_hanley"] += 1
                    if row["JunctionName"] == "Elm Avenue/Rabbit Road" and row["VehicleType"] == "Scooter":
                        traffic_data["scooters"] += 1

                if row["JunctionName"] == "Hanley Highway/Westway":
                    hour = row["timeOfDay"].split(":")[0]
                    if hour in traffic_data["Hanley"]:
                        traffic_data["Hanley"][hour] += 1
                    else:
                        traffic_data["Hanley"][hour] = 1
                
                if row["JunctionName"] == "Elm Avenue/Rabbit Road":
                    hour = row["timeOfDay"].split(":")[0]
                    if hour in traffic_data["Elm"]:
                        traffic_data["Elm"][hour] += 1
                    else:
                        traffic_data["Elm"][hour] = 1
                
                hour = row["timeOfDay"].split(":")[0]
                if hour in traffic_data["hours"]:
                    traffic_data["hours"][hour] += 1
                else:
                    traffic_data["hours"][hour] = 1
                
                

                if row["JunctionName"] == "Hanley Highway/Westway":
                    if row["Weather_Conditions"] == "Heavy Rain" or row["Weather_Conditions"] == "Light Rain":
                        rain_hour = row["timeOfDay"].split(":")[0]
                        if rain_hour not in rain_hours:
                            rain_hours.append(rain_hour)
                        else:
                            continue
                    traffic_data["rain_hours"] = len(rain_hours)

    except Exception as e:
        print(f"Error: {e}")

    # Calculate the percentage and other statistics after the loop is done
    if traffic_data["total_vehicles"] != 0:
        traffic_data["percentage_truck"] = (traffic_data["trucks"] / traffic_data["total_vehicles"] * 100)

    if traffic_data["bicycles"] != 0:
        traffic_data["bicycle_per_hour"] = int(traffic_data["bicycles"] / 24)

    if traffic_data["vehicles_elm"] != 0:
        traffic_data["scooter_percentage"] = int((traffic_data["scooters"] / traffic_data["vehicles_elm"]) * 100)
    
    print(sum(traffic_data["Elm"].values()))
    print(sum(traffic_data["Hanley"].values()))

    # Find peak hours
    if traffic_data["hours"]:
        peak = max(traffic_data["hours"].values(), default=0)
        traffic_data["peak_hours"] = [i for i, j in traffic_data["hours"].items() if j == peak]
    traffic_data["most_vehicles_hour"] = max(traffic_data["hours"].values())  # Find max vehicles in an hour
    peak_str = ""
    for i in traffic_data["peak_hours"]:
        next_hour = str(int(i) + 1)
        peak_str += f"The peak hours are from {i}:00 to {next_hour}:00"

    traffic_data["peak_str"] = peak_str

    return traffic_data



def display_outcomes(outcomes, date, month, year):  # making a formated string to write it back into the file.
    output = f"The file selected is: traffic_data{date:02}{month:02}{year}.csv\n"
    output += f"Total vehicles: {outcomes['total_vehicles']}\n"
    output += f"Trucks: {outcomes['trucks']}\n"
    output += f"Electric vehicles: {outcomes['electric']}\n"
    output += f"Two-wheeled vehicles: {outcomes['two_wheeled']}\n"
    output += f"Buses leaving Elm Avenue heading North: {outcomes['vehicles_out']}\n"
    output += f"Vehicles passing without turning: {outcomes['vehicles_straight']}\n"
    output += f"Percentage of trucks: {round(outcomes['percentage_truck'])}%\n"
    output += f"Average bicycles per hour: {round(outcomes['bicycle_per_hour'])}\n"
    output += f"Over-speeding vehicles: {outcomes['over_speed']}\n"
    output += f"Vehicles through Elm Avenue: {outcomes['vehicles_elm']}\n"
    output += f"Vehicles through Hanley Highway: {outcomes['vehicles_hanley']}\n"
    output += f"Scooter percentage at Elm Avenue: {int(outcomes['scooter_percentage'])}%\n"
    output += f"Peak traffic hours: {outcomes['peak_str']}\n"
    output += f"Most vehicles in an hour: {outcomes['most_vehicles_hour']}\n"
    output += f"Rain hours: {outcomes['rain_hours']}\n"
    output += "\n*******************************************************\n"
    print(output)
    return output


def save_results_to_file(outcomes, date, month, year, file_name="results.txt"):
    try:
        # get the formatted string from display_outcomes to put it into results
        results = display_outcomes(outcomes, date, month, year)

        # write the results to the file successfully
        with open(file_name, "a") as file:
            file.write(results)
        
        print(f"Results successfully saved to {file_name}.")
    
    except Exception as e:
        print(f"Error saving results to file: {e}")

# Task D: Histogram Display

from graphics import GraphWin, Rectangle, Point, Text

class HistogramApp:
    def __init__(self, traffic_data, date_str):
        self.traffic_data = traffic_data
        self.date_str = date_str
        self.win = None

    def setup_window(self):
        win_width = 1400
        win_height = 700
        self.win = GraphWin(f"Histogram for {self.date_str}", win_width, win_height)
        self.win.setCoords(0, 0, win_width, win_height)

    def draw_histogram(self):
        if "Elm" not in self.traffic_data or "Hanley" not in self.traffic_data:
            print("Missing 'Elm' or 'Hanley' data. Cannot draw histogram.")
            return

        left_margin = 100
        bottom_margin = 100
        bar_width = 20
        bar_spacing = 15
        max_bar_height = 400

        hours = [f"{i:02}" for i in range(24)]
        elm_data = {h: self.traffic_data["Elm"].get(h, 0) for h in hours}
        hanley_data = {h: self.traffic_data["Hanley"].get(h, 0) for h in hours}

        max_vehicles = max(max(elm_data.values()), max(hanley_data.values()), 1)

        self.draw_axes(hours, left_margin, bottom_margin, max_bar_height)

        for i, hour in enumerate(hours):
            x_start = left_margin + i * (bar_width * 2 + bar_spacing)
            x_middle = x_start + bar_width
            elm_height = (elm_data[hour] / max_vehicles) * max_bar_height
            hanley_height = (hanley_data[hour] / max_vehicles) * max_bar_height

            # Elm bar
            self.draw_bar(x_start, bottom_margin, bar_width, elm_height, "green")
            self.draw_bar_label(x_start + bar_width/2, bottom_margin + elm_height + 10, elm_data[hour], "green")

            # Hanley bar
            self.draw_bar(x_middle, bottom_margin, bar_width, hanley_height, "red")
            self.draw_bar_label(x_middle + bar_width/2, bottom_margin + hanley_height + 10, hanley_data[hour], "red")

        self.add_legend(left_margin, bottom_margin - 50)

    def draw_axes(self, hours, left_margin, bottom_margin, max_bar_height):
        x_axis_length = len(hours)*(20*2+15)
        x_axis = Rectangle(Point(left_margin, bottom_margin), Point(left_margin + x_axis_length, bottom_margin))
        x_axis.setFill("black")
        x_axis.draw(self.win)

        y_axis = Rectangle(Point(left_margin, bottom_margin), Point(left_margin, bottom_margin + max_bar_height))
        y_axis.setFill("black")
        y_axis.draw(self.win)

        for i, hour in enumerate(hours):
            x_pos = left_margin + i * (20*2 + 15) + 10
            hour_label = Text(Point(x_pos, bottom_margin - 20), hour)
            hour_label.setSize(10)
            hour_label.draw(self.win)

    def draw_bar(self, x_start, bottom_margin, bar_width, bar_height, color):
        bar = Rectangle(Point(x_start, bottom_margin), Point(x_start + bar_width, bottom_margin + bar_height))
        bar.setFill(color)
        bar.draw(self.win)

    def draw_bar_label(self, x_pos, y_pos, value, color):
        label = Text(Point(x_pos, y_pos), str(value))
        label.setSize(8)
        label.setFill(color)
        label.draw(self.win)

    def add_legend(self, left_margin, legend_y):
        elm_legend_box = Rectangle(Point(left_margin, legend_y), Point(left_margin + 20, legend_y + 20))
        elm_legend_box.setFill("green")
        elm_legend_box.draw(self.win)
        elm_label = Text(Point(left_margin + 100, legend_y + 10), "Elm Avenue/Rabbit Road")
        elm_label.setSize(10)
        elm_label.draw(self.win)

        hanley_legend_box = Rectangle(Point(left_margin + 250, legend_y), Point(left_margin + 270, legend_y + 20))
        hanley_legend_box.setFill("red")
        hanley_legend_box.draw(self.win)
        hanley_label = Text(Point(left_margin + 350, legend_y + 10), "Hanley Highway/Westway")
        hanley_label.setSize(10)
        hanley_label.draw(self.win)

    def run(self):
        self.setup_window()
        self.draw_histogram()
        self.win.getMouse()
        self.win.close()






def main():
    date, month, year = validate_date_input()
    file_path = f"traffic_data{date:02}{month:02}{year}.csv" #to ensure file path is correct
    outcomes = process_csv_data(file_path)
    save_results_to_file(outcomes, date, month, year)
    Histogramapp = HistogramApp(outcomes, f"{date:02}/{month:02}/{year}")  # Pass the data and date to the HistogramApp
    
    Histogramapp.run()

main()