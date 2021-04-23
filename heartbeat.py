import datetime
import os
import csv
import time
import sys


def write_line(filename):
    """
    Each time called, write new line to csv
    """
    now = datetime.datetime.now().isoformat()

    # write to file
    columns = ['', 'isotime', 'heartbeat']
    if not os.path.exists(filename):
        with open(filename, 'w') as fp:
            writer = csv.DictWriter(fp, fieldnames=columns, delimiter=',')
            writer.writeheader()

    with open(filename, mode='a+') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=columns, delimiter=',')
        writer.writerow({'': 0,
                         'isotime': now,
                         'heartbeat': 1,
                         })


if __name__ == '__main__':
    filename = '/home/pi/weather/heartbeat.csv'
    try:
        write_line(filename)
    except KeyboardInterrupt:
        print(f'{sys.stderr}, \nExiting by user request.\n')
        sys.exit(0)
