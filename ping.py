from pythonping import ping
import time

# Define the target IP address or hostname
target = "8.8.8.8"

# Define the path to the notepad file
notepad_file = "ping_failures.txt"

# Open the notepad file in append mode

cntfailure = 0

# Initialize variables to track failure duration
failure_start_time = None
failure_end_time = None

for _ in range(48 * 60 * 60):
    # Loop through every second in a day
    try:
        # Send a single ping request
        response = ping(target, count=1)
        print(response)

        # If the ping fails
        if not response.success():
            if failure_start_time is None:
                failure_start_time = time.time()
        else:
            if failure_start_time is not None:
                failure_end_time = time.time()
                duration = int(failure_end_time - failure_start_time)
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            
                # Open the notepad file in append mode
                with open(notepad_file, "a") as file:
                    cntfailure += 1
                    file.write(f"{cntfailure} Failed to ping {target} for {duration} seconds, from {current_time}\n")
            
                failure_start_time = None
    
    except Exception as e:
        # Handle the exception (e.g., log the error)
        print(f"An error occurred: {e}")
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open(notepad_file, "a") as file:
                cntfailure += 1
                file.write(f"{cntfailure} An error occurred: {e} , from {current_time}\n")
        failure_start_time = None
    # Wait for one second
    time.sleep(1)

