import requests
import time
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed

def send_request(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Request failed with status code {response.status_code}")

def test_performance(url, max_simultaneous_requests):
    latencies = []
    throughputs = []

    with ThreadPoolExecutor(max_workers=max_simultaneous_requests) as executor:
        futures = []
        for num_requests in range(1, max_simultaneous_requests + 1):
            print("Starting process for thread count", num_requests)
            start_time = time.time()
            for _ in range(num_requests):
                future = executor.submit(send_request, url)
                futures.append(future)

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception:
                    pass
            print("All requests completed for thread count", num_requests)
            end_time = time.time()

            total_time = end_time - start_time
            latency = total_time / num_requests
            throughput = num_requests / total_time

            latencies.append(latency)
            throughputs.append(throughput)

    # Plotting
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    ax1.plot(range(1, max_simultaneous_requests + 1), latencies, label='Latency')
    ax1.set_xlabel('Number of Simultaneous Requests')
    ax1.set_ylabel('Latency (seconds)')
    ax1.set_title('Latency vs Number of Simultaneous Requests')
    ax1.grid(True)

    ax2.plot(range(1, max_simultaneous_requests + 1), throughputs, label='Throughput')
    ax2.set_xlabel('Number of Simultaneous Requests')
    ax2.set_ylabel('Throughput (requests/second)')
    ax2.set_title('Throughput vs Number of Simultaneous Requests')
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    url = "http://localhost:8080/page1"  # Change this to your web server's URL
    max_simultaneous_requests = 200  # Maximum number of simultaneous requests

    test_performance(url, max_simultaneous_requests)
