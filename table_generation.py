#!/usr/bin/env python

# Code by Samantha Emerson

import csv
import datetime

import matplotlib

# 2 tables ranking the top 10 Presidents from longest lived to shortest lived and then the top 10 presidents from shortest lived to longest lived
# (use CURRENT_DATE via external library to keep track of presidents that are still living)

# also calculate the mean, weighted average, median, mode, max, min and standard deviation of lived_days, put this in a table, and then make a plot that shows the distribution of the data (year_of_birth vs lived_years, maybe? and then put the weighted average vs the actual x-y trend line)

# Assemble your tables and plot into a single report with a title, author and date. Start the report with a 3 or 4 sentence summary of what you found, the body should have your tables and plot and any commentary about your methods or assumptions you think the reader would need to know. Finish the report with a conclusions section, where you state the conclusions you reached through this analysis.


def convert_month_to_value(month_name) -> int:
    month = 0
    if month_name == "Jan":
        month = 1
    elif month_name == "Feb":
        month = 2
    elif month_name == "Mar":
        month = 3
    elif month_name == "Apr":
        month = 4
    elif month_name == "May":
        month = 5
    elif month_name == "June":
        month = 6
    elif month_name == "July":
        month = 7
    elif month_name == "Aug":
        month = 8
    elif month_name == "Sep":
        month = 9
    elif month_name == "Oct":
        month = 10
    elif month_name == "Nov":
        month = 11
    elif month_name == "Dec":
        month = 12
    return month


def main():
    dict_of_lifetimes = {}
    with open("U.S. Presidents Birth and Death Information - Sheet1.csv") as spreadsheet:
        reader = csv.DictReader(spreadsheet)
        for row in reader:
            # key is president name, value is years / months / days lived. print out to tables where the TITLE is "years lived" etc.
            birthdate = row["BIRTH DATE"].split()
            birth_month = convert_month_to_value(birthdate[0])
            birth_day = int(birthdate[1].strip(","))
            birth_year = int(birthdate[2])
            birth_datetime = datetime.date(birth_year, birth_month, birth_day)
            # Activate this code if we want to include living presidents in our calculations. 
            # If not, then keeping this commented out excludes any surviving presidents.
            # if row["DEATH DATE"] is "":
            #     deathdate = datetime.date.today()
            if row["DEATH DATE"] != "":
                deathdate = row["DEATH DATE"].split()
                death_month = convert_month_to_value(deathdate[0])
                death_day = int(deathdate[1].strip(","))
                death_year = int(deathdate[2])
                death_datetime = datetime.date(death_year, death_month, death_day)
                lived_years = death_datetime - birth_datetime
                lived_days = lived_years.days
                dict_of_lifetimes[row["PRESIDENT"]] = lived_days
        print(str(dict_of_lifetimes))
        sorted_descending = sorted(dict_of_lifetimes.items(), key=lambda x:x[1])
        print(str(sorted_descending))
        for key,value in sorted_descending[:10]:
            print(str(key) + ", " + str(value))

        sorted_ascending = sorted(dict_of_lifetimes.items(), key=lambda x:x[1], reverse=True)
        print(str(sorted_ascending))
        for key,value in sorted_ascending[:10]:
            print(str(key) + ", " + str(value))


if __name__ == '__main__':
    main()
