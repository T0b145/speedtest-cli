import csv
import speedtest

import pandas as pd
import matplotlib.pyplot as plt

# CSV file path
csv_file = 'data.csv'
chart_file = 'chart.png'

servers = []
# If you want to test against a specific server
# servers = [1234]

threads = None
# If you want to use a single threaded test
# threads = 1

s = speedtest.Speedtest()
s.get_servers(servers)
s.get_best_server()
s.download(threads=threads)
s.upload(threads=threads)
s.results.share()

results = s.results.dict()
# Write the dictionary to CSV file
with open(csv_file, mode='a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=results.keys(), delimiter=';')
    if file.tell() == 0:
        writer.writeheader()
    writer.writerow(results)




# read csv file into a pandas DataFrame
df = pd.read_csv(csv_file, delimiter=';')

# convert timestamp column to datetime object
df['timestamp'] = pd.to_datetime(df['timestamp'])

# compute rolling average of the last 3 measurements for download and upload speed
df['download_ma'] = df['download'].rolling(window=3).mean()
df['upload_ma'] = df['upload'].rolling(window=3).mean()

# create a line chart for download and upload speed with moving average
fig, ax = plt.subplots(figsize=(10, 6))
df.plot(x='timestamp', y=['download', 'upload'], alpha=0.5, ax=ax)
df.plot(x='timestamp', y=['download_ma', 'upload_ma'], ax=ax)
ax.set(title='Internet Speed over Time', xlabel='Timestamp', ylabel='Speed (Mbps)')


# save chart as png file
plt.savefig(chart_file)