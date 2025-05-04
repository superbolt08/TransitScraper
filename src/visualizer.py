# src/visualizer.py
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

def plot_trip_frequency(csv_path):
    df = pd.read_csv(csv_path)

    # Extract all time values and flatten them
    all_times = df.values.flatten()
    all_times = [t for t in all_times if isinstance(t, str) and t.strip()]

    # Convert times to datetime objects
    hours = []
    for t in all_times:
        try:
            dt = datetime.strptime(t.strip(), "%I:%M %p")
            hours.append(dt.hour)
        except ValueError:
            continue  # skip invalid formats

    # Plot frequency of trips per hour
    if not hours:
        print(f"[⚠️] No valid times in {csv_path}")
        return

    pd.Series(hours).value_counts().sort_index().plot(kind='bar')
    plt.title(f"Trip Frequency by Hour — {os.path.basename(csv_path)}")
    plt.xlabel("Hour of Day")
    plt.ylabel("Number of Trips")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
