import time
import random
import psutil  # You may need to: pip install psutil
import statistics

class ProfileSystem:
    def __init__(self):
        self.response_times = []
        self.error_count = 0
        self.total_requests = 0

    def update_profile(self, user_id, data_size):
        """Simulates updating a user profile."""
        start_time = time.perf_counter()
        self.total_requests += 1
        
        # SIMULATION LOGIC
        try:
            # 1. Simulate network latency
            time.sleep(random.uniform(0.05, 0.2)) 
            
            # 2. Simulate a "Bottleneck" (Scalability Issue)
            # If data_size is large (e.g., a photo), processing takes longer
            if data_size > 500:
                time.sleep(random.uniform(0.5, 1.5))
            
            # 3. Simulate random Server Errors (5xx)
            if random.random() < 0.05:  # 5% failure rate
                raise Exception("Database Connection Timeout")

            status = "Success"
        except Exception as e:
            self.error_count += 1
            status = f"Failed: {e}"

        end_time = time.perf_counter()
        duration = (end_time - start_time) * 1000  # Convert to ms
        self.response_times.append(duration)
        
        return status, duration

    def get_monitoring_report(self):
        """Generates the performance report."""
        if not self.response_times:
            return "No data collected."
        
        avg_rt = sum(self.response_times) / len(self.response_times)
        p95 = statistics.quantiles(self.response_times, n=100)[94] # 95th percentile
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent

        print("\n--- PERFORMANCE & ENVIRONMENT REPORT ---")
        print(f"Total Requests: {self.total_requests}")
        print(f"Error Rate: {(self.error_count/self.total_requests)*100:.2f}%")
        print(f"Average Response Time: {avg_rt:.2f} ms")
        print(f"p95 Response Time: {p95:.2f} ms")
        print(f"Environment Health: CPU {cpu_usage}% | RAM {ram_usage}%")
        print("----------------------------------------\n")

# --- STUDENT EXERCISE EXECUTION ---
system = ProfileSystem()

print("Starting Stress Test...")
for i in range(50):
    # Simulate different users sending different data sizes
    size = random.choice([50, 100, 800]) # 800 simulates a heavy 'Profile Picture'
    status, res_time = system.update_profile(user_id=i, data_size=size)
    print(f"Request {i}: {status} ({res_time:.2f} ms)")

# Generate the final monitoring report
system.get_monitoring_report()
