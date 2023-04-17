import csv
import speedtest

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pytz

def plot_graph(csv_file, chart_file, n_days=30):
    # read csv file into a pandas DataFrame
    df = pd.read_csv(csv_file, delimiter=';')

    # convert timestamp column to datetime object and set timezone to Germany
    germany_tz = pytz.timezone('Europe/Berlin')
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_convert(germany_tz)

    # compute rolling average of the last 3 measurements for download and upload speed
    df['download_ma'] = df['download'].rolling(window=3).mean()
    df['upload_ma'] = df['upload'].rolling(window=3).mean()

    # filter data to last 30 days
    last_30_days = datetime.now() - timedelta(days=30)
    last_30_days = pd.Timestamp(last_30_days, tz=germany_tz)
    df = df[df['timestamp'] > last_30_days]

    # create a line chart for download and upload speed with moving average
    fig, ax = plt.subplots(figsize=(10, 6))

    # plot upload and download as dots
    ax.scatter(df['timestamp'], df['upload'], color='blue', alpha=0.4)
    ax.scatter(df['timestamp'], df['download'], color='red', alpha=0.4)

    # plot moving averages as lines
    df.plot(x='timestamp', y='download_ma', color='red', ax=ax)
    df.plot(x='timestamp', y='upload_ma', color='blue', ax=ax)

    ax.set(title='Internet Speed over Time', xlabel='Timestamp', ylabel='Speed (Mbps)')

    # save chart as png file
    plt.savefig(chart_file)

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

plot_graph(csv_file, chart_file)