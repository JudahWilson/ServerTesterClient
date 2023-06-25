import requests
import csv
from datetime import datetime

# Number of requests to be sent
num_requests = 100

# URL of the server to be tested
server_url = "http://192.168.57.1:8000/response_and_latency"

# Function to perform the response time test
def perform_response_time_test():
    response_times = []

    for _ in range(num_requests):
        client_send_time = datetime.now()

        # Prepare request data including client_send_time
        request_data = {'client_send_time': client_send_time}

        # Send the request with request_data
        response = requests.get(server_url, params=request_data)
        server_response_time = datetime.now()

        # Extract server_send_time from response
        server_send_time = datetime.strptime(response.headers['Server-Send-Time'], '%Y-%m-%d %H:%M:%S.%f')

        # Calculate the required time measurements
        client_receive_time = datetime.now()
        client_to_server_time = (server_send_time - client_send_time).total_seconds() * 1000
        server_processing_time = (server_response_time - server_send_time).total_seconds() * 1000
        server_to_client_time = (client_receive_time - server_response_time).total_seconds() * 1000
        total_time = (client_receive_time - client_send_time).total_seconds() * 1000

        response_times.append({
            'client_send_time': client_send_time,
            'client_receive_time': client_receive_time,
            'client_to_server_time': client_to_server_time,
            'server_processing_time': server_processing_time,
            'server_to_client_time': server_to_client_time,
            'total_time': total_time
        })

    return response_times

# Append test results to a CSV file
def append_to_csv(results):
    timestamp = datetime.now().strftime("%Y-%m-%d %H.%M.%S")
    filename = f"test-{timestamp}.csv"

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            'Client Send Time',
            'Client Receive Time',
            'Client to Server Time (ms)',
            'Server Processing Time (ms)',
            'Server to Client Time (ms)',
            'Total Time (ms)'
        ])
        for result in results:
            writer.writerow([
                result['client_send_time'],
                result['client_receive_time'],
                result['client_to_server_time'],
                result['server_processing_time'],
                result['server_to_client_time'],
                result['total_time']
            ])

# Perform the response time test
response_times = perform_response_time_test()

# Save the results to a CSV file
append_to_csv(response_times)
