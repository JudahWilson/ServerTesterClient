import requests
import csv
from datetime import datetime

# URL of the server to be tested
server_url = "http://192.168.1.57:8000"

# Function to perform the uptime test
def perform_uptime_test():
    try:
        response = requests.get(f"{server_url}/up")
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Append test results to a CSV file
def append_to_csv(results, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H.%M.%S")
    filename = f"test-{timestamp}.csv"

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, results, status])

# Perform the test and store results
status = "UP" if perform_uptime_test() else "DOWN"
score = 5 if status == "UP" else 1
append_to_csv(status, score)
