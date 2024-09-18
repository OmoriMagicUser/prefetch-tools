import os
import csv
from datetime import datetime, timedelta

csv_file = r"prefetch_data.csv"

time_threshold = timedelta(seconds=60)

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def get_datetime_format():
    print("Choose a Date and Time format:")
    print("")
    print("1. Military Time, Day.Month.Year")
    print("2. Military Time, Month.Day.Year")
    print("3. 12 Hour Clock, Day.Month.Year")
    print("4. 12 Hour Clock, Month.Day.Year")
    print("")
    choice = input("Enter your choice (1-4): ").strip()

    if choice == '1':
        return '%d/%m/%Y %H:%M:%S'
    elif choice == '2':
        return '%m/%d/%Y %H:%M:%S'
    elif choice == '3':
        return '%d/%m/%Y %I:%M:%S %p'
    elif choice == '4':
        return '%m/%d/%Y %I:%M:%S %p'
    else:
        print("\nInvalid choice. Please enter a number between 1 and 4.\n")
        clear_screen()
        return get_datetime_format()

def check_prefetch_times(csv_file):
    found_suspicious = False

    datetime_format = get_datetime_format()

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

                mod_time = datetime.strptime(mod_time_str, datetime_format)

                most_recent_run_time_str = run_times_str.split(',')[0].strip()
                most_recent_run_time = datetime.strptime(most_recent_run_time_str, datetime_format)

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