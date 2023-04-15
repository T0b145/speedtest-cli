import csv
import speedtest

# CSV file path
csv_file = 'data.csv'

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