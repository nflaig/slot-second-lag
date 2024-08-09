import pandas as pd
import matplotlib.pyplot as plt
import re

# Read the log data from a file
file_path = "event-loop-lag-detected2.log"
with open(file_path, 'r') as file:
    log_data = file.read()

# Extract relevant data using regex
pattern = re.compile(r'slot=(\d+), startSlotSec=([\d.]+), endSlotSec=([\d.]+), delayMs=(\d+)')
matches = pattern.findall(log_data)

# Create a DataFrame
df = pd.DataFrame(matches, columns=['slot', 'startSlotSec', 'endSlotSec', 'delayMs'])
df['slot'] = df['slot'].astype(int)
df['startSlotSec'] = df['startSlotSec'].astype(float)
df['endSlotSec'] = df['endSlotSec'].astype(float)
df['delayMs'] = df['delayMs'].astype(int)

# Define the slot ranges
slot_ranges = range(13)  # Define ranges from 0, 1, ..., 12

# Calculate the number of lags in each range
lag_counts = []
for start in slot_ranges:
    count = df[(df['startSlotSec'] >= start) & (df['startSlotSec'] < start + 1)].shape[0]
    lag_counts.append(count)

# Debug: Print the counts for each slot range
for start, count in zip(slot_ranges, lag_counts):
    print(f"Start Slot: {start}, Count: {count}")

# Calculate the percentage of lags for each range
total_lags = sum(lag_counts)
lag_percentages = [(count / total_lags) * 100 for count in lag_counts]

# Prepare the range labels
range_labels = [f'{start}' for start in slot_ranges]

# Debug: Print the percentage for each slot range
for label, percentage in zip(range_labels, lag_percentages):
    print(f"Range Label: {label}, Percentage: {percentage:.2f}%")

# Plotting the percentage of lags per range
plt.figure(figsize=(12, 6))
plt.bar(range_labels, lag_percentages, color='blue')
plt.xlabel('Slot Second')
plt.ylabel('Percentage of Event Loop Lags (%)')
plt.title('Percentage of Event Loop Lags per Slot Second')
plt.xticks(rotation=45)
plt.grid(False)
plt.show()
