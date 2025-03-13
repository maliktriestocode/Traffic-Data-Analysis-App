# Traffic Data Analysis Application

This Python application processes traffic data from a CSV file and provides insights such as total vehicles, peak traffic hours, and more. It also includes a graphical histogram to visualize traffic patterns at specific junctions.

---

## Features

1. **Date Validation**: Ensures the user inputs a valid date in `DD MM YYYY` format.
2. **CSV Data Processing**: Analyzes traffic data from a CSV file and calculates metrics such as:
   - Total vehicles, trucks, electric vehicles, and two-wheeled vehicles.
   - Peak traffic hours and over-speeding vehicles.
   - Traffic patterns at specific junctions (Elm Avenue/Rabbit Road and Hanley Highway/Westway).
3. **Results Display**: Outputs the analysis results to the console and saves them to a text file (`results.txt`).
4. **Histogram Visualization**: Displays a histogram comparing traffic patterns at Elm Avenue and Hanley Highway for the selected date.

---

## Prerequisites

Before running the application, ensure you have the following installed:

- **Python 3.x**: Download and install Python from [python.org](https://www.python.org/).
- **Graphics Library**: Install the `graphics.py` library. You can download it from [here](https://mcsp.wartburg.edu/zelle/python/graphics.py) and place it in your project directory.

---

## How to Run the Application

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name

2. Prepare the CSV File:

Ensure your CSV file is named in the format traffic_dataDDMMYYYY.csv (e.g., traffic_data01012024.csv).

Place the CSV file in the same directory as the script.

3. Run the Application:


python main.py

Follow the Prompts:

    Enter the date in DD MM YYYY format when prompted.

    The application will process the data, display the results, and save them to results.txt.

    A histogram will be displayed to visualize traffic patterns.

    Code Structure
    validate_date_input(): Validates user input for the date.

    process_csv_data(file_path): Processes the CSV file and calculates traffic metrics.

    display_outcomes(outcomes, date, month, year): Formats and displays the analysis results.

    save_results_to_file(outcomes, date, month, year): Saves the results to results.txt.

    HistogramApp: A class for creating and displaying a histogram of traffic data.

    main(): The main function that ties everything together.

    Example CSV Format
    The CSV file should have the following columns (headers):

    VehicleType: Type of vehicle (e.g., Car, Truck, Bicycle).

    electricHybrid: Whether the vehicle is electric/hybrid (true or false).

    JunctionName: Name of the junction (e.g., Elm Avenue/Rabbit Road, Hanley Highway/Westway).

    travel_Direction_in: Direction of travel into the junction.

    travel_Direction_out: Direction of travel out of the junction.

    VehicleSpeed: Speed of the vehicle.

    JunctionSpeedLimit: Speed limit at the junction.

    timeOfDay: Time of day in HH:MM format.

    Weather_Conditions: Weather conditions (e.g., Heavy Rain, Light Rain, Clear).

    Output
    Console Output:

    Displays the analysis results, including total vehicles, peak hours, and more.

    Text File (results.txt):

    Saves the analysis results for future reference.

    Histogram:

    Displays a graphical comparison of traffic patterns at Elm Avenue and Hanley Highway.

    Dependencies
    Python 3.x

    graphics.py library

