import os
import csv
from datetime import datetime, timedelta

csv_file = r"prefetch_data.csv"
time_threshold = timedelta(seconds=60)

datetime_formats = [
    '%d/%m/%Y %H:%M:%S',
    '%m/%d/%Y %H:%M:%S',
    '%d/%m/%Y %I:%M:%S %p',
    '%m/%d/%Y %I:%M:%S %p',
    '%Y/%m/%d %H:%M:%S',
    '%Y/%d/%m %H:%M:%S',
    '%Y/%m/%d %I:%M:%S %p',
    '%Y/%d/%m %I:%M:%S %p',
    '%d-%m-%Y %H:%M:%S',
    '%m-%d-%Y %H:%M:%S',
    '%d-%m-%Y %I:%M:%S %p',
    '%m-%d-%Y %I:%M:%S %p',
    '%Y-%m-%d %H:%M:%S',
    '%Y-%d-%m %H:%M:%S',
    '%Y-%m-%d %I:%M:%S %p',
    '%Y-%d-%m %I:%M:%S %p'
]

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def try_parse_datetime(date_str):
    for fmt in datetime_formats:
        try:
            return datetime.strptime(date_str, fmt), fmt
        except ValueError:
            continue
    raise ValueError(f"Time data '{date_str}' does not match any known format.")

def check_prefetch_times(csv_file):
    found_suspicious = False

    try:
        with open(csv_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            clear_screen()
            for row in reader:
                if len(row) < 8:
                    continue

                filename = row[0].strip()
                mod_time_str = row[2].strip()
                run_times_str = row[7].strip()

                try:
                    mod_time, mod_format = try_parse_datetime(mod_time_str)
                    most_recent_run_time_str = run_times_str.split(',')[0].strip()
                    most_recent_run_time, run_format = try_parse_datetime(most_recent_run_time_str)
                except ValueError as e:
                    print(f"An error occurred: {e}")
                    continue

                time_difference = (mod_time - most_recent_run_time).total_seconds()

                if time_difference > 60:
                    found_suspicious = True
                    print(f"\nPrefetch File: {filename}")
                    print(f"  Most Recent Run Time: {most_recent_run_time}")
                    print(f"  Modification Time: {mod_time}")
                    print(f"  Difference: {time_difference} seconds")
                    print("\nPossible Type Bypass Used\n")

        if not found_suspicious:
            clear_screen()
            print("Completed. Nothing Suspicious.")

    except Exception as e:
        print(f"An error occurred: {e}")

check_prefetch_times(csv_file)
input()
