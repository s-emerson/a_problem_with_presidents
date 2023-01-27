#!/usr/bin/env python

# Code by Samantha Emerson

import csv
import datetime
import statistics
import math

import matplotlib
from pyparsing import dict_of

# Assemble your tables and plot into a single report with a title, author and date. Start the report with a 3 or 4 sentence summary of what you found, the body should have your tables and plot and any commentary about your methods or assumptions you think the reader would need to know. Finish the report with a conclusions section, where you state the conclusions you reached through this analysis.


def tables_of_lived_days(dict_of_lifetimes):
    """ 2 tables ranking the top 10 Presidents from longest lived to shortest lived and then the top 10 presidents from shortest lived to longest lived """

    # TODO: convert this to a table instead of an iterated printout

    print(str(dict_of_lifetimes))
    sorted_descending = sorted(dict_of_lifetimes.items(), key=lambda x:x[1])
    print("List of Shortest-Lived Presidents (Name, Days): ")
    for key,value in sorted_descending[:10]:
        print(str(key) + ", " + str(value))

    sorted_ascending = sorted(dict_of_lifetimes.items(), key=lambda x:x[1], reverse=True)
    print("List of Longest-Lived Presidents (Name, Days): ")
    for key,value in sorted_ascending[:10]:
        print(str(key) + ", " + str(value))


def calculate_mean(dict_of_lifetimes):
    """ Mean is (sum of items) / (number of items) """
    sum_of_items = 0
    for value in dict_of_lifetimes:
        sum_of_items = sum_of_items + dict_of_lifetimes[value]
    mean = sum_of_items / len(dict_of_lifetimes)
    return mean
    


def calculate_weighted_average(dict_of_lifetimes):
    """ Weighted average is (sum of (items times 1/(standard deviation)^2)) / (sum of 1/(standard deviation)^2s) """
    # all values should have equal weight though- what causes this to be different from the mean in this case?
    st_dev = calculate_st_dev(dict_of_lifetimes)
    pass


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
    # mode is most common value
    # look for non-unique values in the dict

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
        print("Max value: ", non_unique_max)
        # Create a list of keys with this value (can be more than one value)
        for value in check_for_unique:
            if value == non_unique_max:
                modes.append(value)
    except TypeError:
        # If no item occurs more than the others, then there is no  mode:
        if modes == []:
            print("No mode found / all values are unique.")

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

        tables_of_lived_days(dict_of_lifetimes)

        mean = calculate_mean(dict_of_lifetimes)
        rounded_mean = round(mean)
        mean_years = round(mean / 365)
        print("Mean lifetime: " + str(rounded_mean) + " days.")
        print("Mean lifetime: " + str(mean_years) + " years.")

        calculate_weighted_average(dict_of_lifetimes)

        median = calculate_median(dict_of_lifetimes)
        print("Median lifetime in days is: " + str(median))

        calculate_mode(dict_of_lifetimes)

        calculate_max(dict_of_lifetimes) # related to top 10

        calculate_min(dict_of_lifetimes) # related to bottom 10

        st_dev = calculate_st_dev(dict_of_lifetimes)
        print("Standard deviation is: " + str(st_dev))

        # put all this in a table, and then make a plot that shows the distribution of the data (year_of_birth vs lived_years, maybe? and then put the weighted average vs the actual x-y trend line)




if __name__ == '__main__':
    main()
