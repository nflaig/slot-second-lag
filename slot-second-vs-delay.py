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


# Plotting the data
plt.figure(figsize=(10, 6))
plt.scatter(df['startSlotSec'], df['delayMs'], c='blue', label='Delay', s=15)
plt.xlabel('Slot Second')
plt.ylabel('Delay (ms)')
plt.title('Event Loop Lag: Slot Second vs. Delay')
plt.xlim(0, 12)
plt.legend()
plt.grid(True)
plt.show()
