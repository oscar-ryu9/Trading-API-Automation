import time
import os
import pandas as pd

class CSVMonitor:
    def __init__(self, filename):
        self.filename = filename
        self.last_modified = None

    def is_modified(self):
        current_modified = os.path.getmtime(self.filename)
        if self.last_modified is None or current_modified > self.last_modified:
            self.last_modified = current_modified
            return True
        return False

    def process_csv(self):
        try:
            df = pd.read_csv(self.filename)
            # Process the CSV data here
            print(df.head())  # For demonstration, just printing the first few rows
        except Exception as e:
            print("Error processing CSV:", e)

def monitor_csv(filename):
    csv_monitor = CSVMonitor(filename)
    print("Monitoring CSV file for changes...")
    try:
        while True:
            if csv_monitor.is_modified():
                print("CSV file modified, processing...")
                csv_monitor.process_csv()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Monitoring stopped.")

if __name__ == "__main__":
    filename = "update.csv"  # Replace with your CSV file path
    monitor_csv(filename)
