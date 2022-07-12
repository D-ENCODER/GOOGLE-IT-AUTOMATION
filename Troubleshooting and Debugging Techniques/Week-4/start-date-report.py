#!/usr/bin/env python3


import csv
import datetime
import requests
import operator

FILE_URL = "https://storage.googleapis.com/gwg-hol-assets/gic215/employees-with-date.csv"


def get_start_date():
    """Interactively get the start date to query for."""

    print()
    print('Getting the first start date to query for.')
    print()
    print('The date must be greater than Jan 1st, 2018')
    year = int(input('Enter a value for the year: '))
    month = int(input('Enter a value for the month: '))
    day = int(input('Enter a value for the day: '))
    print()

    return datetime.datetime(year, month, day)


def get_file_lines(url):
    """Returns the lines contained in the file at the given URL"""

    # Download the file over the internet
    response = requests.get(url, stream=True)
    lines = []

    for line in response.iter_lines():
        lines.append(line.decode("UTF-8"))
    return lines


def get_same_or_newer(start_date):

    data = get_file_lines(FILE_URL)
    readers = csv.reader(data[1:])

    # Sort list
    sorted_readers = sorted(readers, key=operator.itemgetter(3))

    min_date_employees = {}

    for row in sorted_readers:
        # Get start date
        row_date = datetime.datetime.strptime(row[3], '%Y-%m-%d')
        if row_date > start_date:
            if row_date not in min_date_employees:
                min_date_employees[row_date] = ["{} {}".format(row[0], row[1])]
            else:
                min_date_employees[row_date].append("{} {}".format(row[0], row[1]))

    return min_date_employees


def list_newer(start_date):

    min_date_employees = get_same_or_newer(start_date)

    for emp_date, emp in min_date_employees.items():
        print("Started on {}: {}".format(emp_date.strftime("%b %d, %Y"), emp))


def main():
    start_date = get_start_date()
    list_newer(start_date)


if __name__ == "__main__":
    main()
