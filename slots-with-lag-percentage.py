import pandas as pd
import matplotlib.pyplot as plt
import re

# Read the log data from a file
file_path = "event-loop-lag-detected.log"
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

# Get the full range of slots
min_slot = df['slot'].min()
max_slot = df['slot'].max()
all_slots = range(min_slot, max_slot + 1)

# Create a DataFrame for all slots
all_slots_df = pd.DataFrame({'slot': all_slots})

# Define the slot ranges
slot_ranges = range(13)  # Define ranges from 0, 1, ..., 12

# Function to determine the lag category
def get_lag_category(slot):
    if slot in df['slot'].values:
        start_slot_sec = df[df['slot'] == slot]['startSlotSec'].values[0]
        for start in slot_ranges:
            if start <= start_slot_sec < start + 1:
                return f'{start}'
    return 'No Lag'

# Apply the function to get the lag category for each slot
all_slots_df['lag_category'] = all_slots_df['slot'].apply(get_lag_category)

# Calculate the percentage of slots in each category
category_counts = all_slots_df['lag_category'].value_counts(normalize=True) * 100

# Plotting the percentage of slots in each category with percentage labels
plt.figure(figsize=(12, 6))
bars = plt.bar(category_counts.index, category_counts.values, color='blue')

# Adding percentage labels above the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f'{yval:.2f}%', ha='center', va='bottom')

plt.xlabel('Lag Category')
plt.ylabel('Percentage of Slots (%)')
plt.title('Percentage of Slots with Event Loop Lag > 1 second')
plt.xticks(rotation=45)
plt.grid(False)
plt.show()
