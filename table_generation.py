#!/usr/bin/env python

# Code by Samantha Emerson

import csv
import datetime
import statistics
import math
import sys

import matplotlib
from matplotlib import pyplot as plt
from pyparsing import dict_of
import numpy as np

# Assemble your tables and plot into a single report with a title, author and date. Start the report with a 3 or 4 sentence summary of what you found, the body should have your tables and plot and any commentary about your methods or assumptions you think the reader would need to know. Finish the report with a conclusions section, where you state the conclusions you reached through this analysis.


def ranks_of_lived_days(dict_of_lifetimes):
    """ 2 tables ranking the top 10 Presidents from longest lived to shortest lived and then the top 10 presidents from shortest lived to longest lived """

    with open('tables/ranked_tables.txt', 'w') as rank_file:

        # print(str(dict_of_lifetimes))
        sorted_descending = sorted(dict_of_lifetimes.items(), key=lambda x:x[1])
        rank_file.write("List of Shortest-Lived Presidents: " + "\n")
        rank_file.write("{:<20} {:<15}".format("NAME","DAYS LIVED") + "\n")
        for key, value in sorted_descending[:10]:
            pres = key
            lived = value
            rank_file.write("{:<20} {:<15}".format(pres, lived) + "\n")
        rank_file.write("\n")

        sorted_ascending = sorted(dict_of_lifetimes.items(), key=lambda x:x[1], reverse=True)
        rank_file.write("List of Longest-Lived Presidents: " + "\n")
        rank_file.write("{:<20} {:<15}".format("NAME","DAYS LIVED") + "\n")
        for key, value in sorted_ascending[:10]:
            pres = key
            lived = value
            rank_file.write("{:<20} {:<15}".format(pres, lived) + "\n")



def calculate_mean(dict_of_lifetimes):
    """ Mean is (sum of items) / (number of items) """
    sum_of_items = 0
    for value in dict_of_lifetimes:
        sum_of_items = sum_of_items + dict_of_lifetimes[value]
    mean = sum_of_items / len(dict_of_lifetimes)
    return mean
    


def calculate_weighted_average(dict_of_lifetimes):
    """ Weighted average is (sum of (items times 1/(variance)^2)) / (sum of 1/(variance)^2s) """
    # what is the variance for this dataset? we know the exact birth dates.
    # i guess if we count *hours* in the day- if they were born at 12:01 and died at 11:59 pm, that's technically a difference of a full extra day. or if they were born at 11:59 pm and died at 12:01 am, that's a variance of one LESS day. so a variance +/- 0.99 days that would apply to each item in the dict.
    variance = 1.0 / (0.99 ** 2)
    length = len(dict_of_lifetimes)
    weighted = 0
    for value in dict_of_lifetimes:
        i = dict_of_lifetimes[value]
        weighted += (variance * i)
    weighted = weighted / (variance * length)
    return weighted


def calculate_median(dict_of_lifetimes):
    """ Checks if length is even or odd using len(). If odd, uses the middle value. If even, use the average of the two middle values """
    length = len(dict_of_lifetimes)
    if (length % 2) == 0:
        # even
        length = length + 1
        halfway_plus = int((length / 2) + 0.5)
        halfway_minus = int((length / 2) - 0.5)
        median_index = (list(dict_of_lifetimes)[halfway_plus] + list(dict_of_lifetimes)[halfway_minus]) / 2
    else:
        # odd - minus because index is going to start from 0
        halfway = int((length / 2) - 0.5)
        median_index = list(dict_of_lifetimes)[halfway]

    median = dict_of_lifetimes[median_index]
    return median


def calculate_mode(dict_of_lifetimes):
    """ Mode is most common value- look for non-unique values in the dict """

    check_for_unique = {}

    # Create a dict of times that each value appears in the input dictionary
    for value in dict_of_lifetimes:
        days_lived = dict_of_lifetimes[value]
        if days_lived in check_for_unique:
            check_for_unique[value] += 1
        else:
            check_for_unique[value] = 1
        # print("Dictionary contents: ", check_for_unique)
            
    # Find the maximum times a value appeared
    modes = []
    try:
        non_unique_max = max(check_for_unique.values(), key=check_for_unique.get)
        # Create a list of keys with this value (can be more than one value)
        for value in check_for_unique:
            if value == non_unique_max:
                modes.append(value)
    except TypeError:
        # If no item occurs more than the others, then there is no  mode:
        if modes == []:
            modes = "All values are unique; no"

    return modes


def calculate_max(dict_of_lifetimes):
    sorted_descending = sorted(dict_of_lifetimes.items(), key=lambda x:x[1])
    print("Shortest-Lived President (Name, Days): ")
    for key,value in sorted_descending[:1]:
        print(str(key) + ", " + str(value))


def calculate_min(dict_of_lifetimes):
    sorted_ascending = sorted(dict_of_lifetimes.items(), key=lambda x:x[1], reverse=True)
    print("Longest-Lived President (Name, Days): ")
    for key,value in sorted_ascending[:1]:
        print(str(key) + ", " + str(value))


def calculate_st_dev(dict_of_lifetimes):
    """ standard deviation is sqrt((1/length - 1) * the sum of (each value - average)^2) """
    length = len(dict_of_lifetimes)
    sum_of_deviation = 0
    mean = calculate_mean(dict_of_lifetimes)
    for value in dict_of_lifetimes:
        sum_of_deviation = (dict_of_lifetimes[value] - mean) ** 2
    length_fraction = 1/(length-1)
    standard_deviation = math.sqrt(length_fraction * sum_of_deviation)
    return standard_deviation


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
        full_dataset = {}
        for row in reader:
            # key is president name, value is years / months / days lived. print out to tables where the TITLE is "years lived" etc.
            birthdate = row["BIRTH DATE"].split()
            birth_month = convert_month_to_value(birthdate[0])
            birth_day = int(birthdate[1].strip(","))
            birth_year = int(birthdate[2])
            birth_datetime = datetime.date(birth_year, birth_month, birth_day)
            # Activate this code if we want to include living presidents in our calculations. 
            # If not, then keeping this commented out excludes any surviving presidents.
            if row["DEATH DATE"] == "":
                death_datetime = datetime.date.today()
            if row["DEATH DATE"] != "":
                deathdate = row["DEATH DATE"].split()
                death_month = convert_month_to_value(deathdate[0])
                death_day = int(deathdate[1].strip(","))
                death_year = int(deathdate[2])
                death_datetime = datetime.date(death_year, death_month, death_day)
            lived_years = death_datetime - birth_datetime
            lived_days = lived_years.days
            dict_of_lifetimes[row["PRESIDENT"]] = lived_days
            row["DAYS LIVED"] = str(lived_days)

            full_dataset[row["PRESIDENT"]] = [str(birth_datetime),  str(death_datetime), row["DAYS LIVED"]]

        # print the whole dataset out in a nice table
        with open('tables/full_tables.txt', 'w') as full_file:
            full_file.write("{:<25} {:<15} {:<15} {:<15}".format("PRESIDENT","BIRTH DATE","DEATH DATE","DAYS LIVED") + "\n")
            for key, values in full_dataset.items():
                pres = key
                birth, death, lived = values
                if death == str(datetime.date.today()):
                    death = "Alive"
                full_file.write("{:<25} {:<15} {:<15} {:<15}".format(pres, birth, death, lived) + "\n")

        ranks_of_lived_days(dict_of_lifetimes)

        mean = calculate_mean(dict_of_lifetimes)
        rounded_mean = round(mean)
        mean_years = round(mean / 365)
        print("Mean lifetime: " + str(rounded_mean) + " days.")
        print("Mean lifetime: " + str(mean_years) + " years.")

        weighted = calculate_weighted_average(dict_of_lifetimes)
        print("Weighted average is: " + str(weighted) + " days.")

        median = calculate_median(dict_of_lifetimes)
        print("Median lifetime in days is: " + str(median) + " days.")

        modes = calculate_mode(dict_of_lifetimes)
        print("Mode of lifetimes is: " + str(modes) + " days.")

        calculate_max(dict_of_lifetimes) # related to top 10

        calculate_min(dict_of_lifetimes) # related to bottom 10

        st_dev = calculate_st_dev(dict_of_lifetimes)
        print("Standard deviation is: " + str(st_dev))

        # put all this in a table, and then make a plot that shows the distribution of the data (year_of_birth vs lived_years, maybe? and then put the weighted average vs the actual x-y trend line)

        list_of_years = []
        list_of_lived = []
        for key, values in full_dataset.items():
            pres = key
            birth, death, lived = values
            birthdate = birth[0:4]
            list_of_years.append(int(birthdate))
            list_of_lived.append(int(lived))
        plt.scatter(list_of_years, list_of_lived, label = 'Data')
        # plt.plot(weighted)
        plt.title('Change in Lifetime of Presidents by Year')
        plt.xlabel('Year of Birth')
        plt.ylabel('Days Lived')
        # plt.yticks([16000, 20000, 24000, 28000, 32000, 36000])
        fit = np.polyfit(list_of_years, list_of_lived, 1)
        line = np.poly1d(fit)
        plt.plot(list_of_years, line(list_of_years), 'r', label = 'Trendline')
        plt.legend(loc = 'best')
        plt.show()
        plt.savefig("lifetime_plot.png")




if __name__ == '__main__':
    main()
