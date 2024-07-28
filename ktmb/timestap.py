from datetime import datetime
from data import df

class TimeTracker:
    def __init__(self):
        self.arrival_time = None
        self.departure_time = None

    def arrive(self):
        self.arrival_time = datetime.now()
        print("Arrival time recorded:", self.arrival_time)

    def depart(self):
        if self.arrival_time is None:
            print("Error: You must arrive before you can depart.")
            return

        self.departure_time = datetime.now()
        print("Departure time recorded:", self.departure_time)

    def get_duration(self):
        if self.arrival_time is None or self.departure_time is None:
            print("Error: Both arrival and departure times must be recorded to get duration.")
            return

        duration = self.departure_time - self.arrival_time
        print("Duration of stay:", duration)

# Example usage
tracker = TimeTracker()
tracker.arrive()
# Simulate some time passing
# For the sake of this example, let's say 5 seconds have passed
tracker.depart()
tracker.get_duration()

