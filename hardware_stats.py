import requests
import csv
from datetime import datetime

# URL of the server
server_url = "http://192.168.1.57:8000"

# Function to fetch server statistics
def fetch_server_stats():
    try:
        response = requests.get(server_url + '/stats')
        if response.status_code == 200:
            stats = response.json()
            return stats
        else:
            return None
    except requests.exceptions.RequestException:
        return None

# Assign a critical rating based on the metric value and criteria
def assign_critical_rating(category, metric, value):
    if category == 'cpu':
        if metric == 'usage_percent':
            if value < 50:
                return 5  # Excellent
            elif value < 70:
                return 4  # Good
            elif value < 90:
                return 3  # Moderate
            elif value < 95:
                return 2  # Poor
            else:
                return 1  # Critical
    elif category == 'memory':
        if metric == 'usage_percent':
            if value < 50:
                return 5  # Excellent
            elif value < 70:
                return 4  # Good
            elif value < 90:
                return 3  # Moderate
            elif value < 95:
                return 2  # Poor
            else:
                return 1  # Critical
    elif category == 'disk':
        if metric == 'usage_percent':
            if value < 50:
                return 5  # Excellent
            elif value < 70:
                return 4  # Good
            elif value < 90:
                return 3  # Moderate
            elif value < 95:
                return 2  # Poor
            else:
                return 1  # Critical
        elif metric == 'total' or metric == 'used' or metric == 'free':
            if value < 10e9:
                return 1  # Critical
            elif value < 100e9:
                return 2  # Poor
            elif value < 500e9:
                return 3  # Moderate
            elif value < 1e12:
                return 4  # Good
            else:
                return 5  # Excellent
    elif category == 'battery':
        if metric == 'health':
            if value == 'Good':
                return 5  # Excellent
            elif value == 'Fair':
                return 4  # Good
            elif value == 'Poor':
                return 2  # Poor
            else:
                return 1  # Critical
    elif category == 'temperature':
        if metric == 'cpu':
            if value < 60:
                return 5  # Excellent
            elif value < 70:
                return 4  # Good
            elif value < 80:
                return 3  # Moderate
            elif value < 90:
                return 2  # Poor
            else:
                return 1  # Critical

    return ''  # Default no rating


# Append test results to a CSV file
def append_to_csv(stats):
    timestamp = datetime.now().strftime("%Y-%m-%d %H.%M.%S")
    filename = f"stats-{timestamp}.csv"

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        # Write header row
        writer.writerow(['Timestamp', 'Category', 'Metric', 'Value', 'Critical Rating'])

        # Write rows for CPU, Memory, Disk, and Battery stats
        for category, data in stats.items():
            for metric, value in data.items():
                critical_rating = assign_critical_rating(category, metric, value)
                writer.writerow([timestamp, category, metric, value, critical_rating])

# Fetch server statistics
stats = fetch_server_stats()

# Append stats to CSV file
if stats is not None:
    append_to_csv(stats)
    print("Statistics fetched and saved to CSV file.")
else:
    print("Failed to fetch server statistics.")
