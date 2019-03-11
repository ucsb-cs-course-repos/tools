#!/usr/bin/env python

import argparse
import pytest
import datetime
import dateutil
from dateutil.parser import *
import os

legal_days_of_week="MTWRF"

def validate_days_of_week(days_of_week):
    for c in days_of_week:
        if c not in legal_days_of_week:
          raise ValueError("days_of_week should contain only chars from" +
                           legal_days_of_week)


def validate_date(date):
     result = datetime.datetime.utcfromtimestamp(date) # raises ValueError if illegal value
     #I am getting erros from the above call, using parse, we might not need this function
     return result

def validate_start_date(date):
     result = validate_date(date)
     sunday = 6 # see: https://docs.python.org/2/library/datetime.html
     day_of_week = result.weekday()
     if day_of_week != sunday:
         raise ValueError("Start Date should be a Sunday")
     return result

def add_weeks(start_datetime,weeks):
    """
    Return a datetime that is start_datetime plus weeks into the future

    Example:
      start_datetime represents 2019-03-31, weeks is 0 => 2019-03-31
      start_datetime represents 2019-03-31, weeks is 1 => 2019-04-07
      start_datetime represents 2019-03-31, weeks is 2 => 2019-04-14
    """
    days_ahead = weeks * 7
    final_datetime = n_days_ahead(start_datetime, 7*weeks)
    return final_datetime

def n_days_ahead(start_datetime, days):
    """
    Return a datetime that is start_datetime plus days into the future
    """
    delta = datetime.timedelta(days = days)
    return start_datetime + delta

def days_for_this_week(start_datetime, dates):
    """
    Return a tuple of len(dates) datetimes, one for each lecture day
    start_datetime is the first lecture day of the week, the rest
    are calculated by addings days forward according to dates

    Warning: Does not account for holidays (see days_without_holidays)
    """
    days_this_week = []

    for d in dates:
        day_num = day_to_num(d) + 1 #Plus 1 so Monday is offset 1 from Sunday
        days_this_week.append(n_days_ahead(start_datetime, day_num))

    return days_this_week

def days_without_holidays(days_of_week, holiday_list):
    """
    Given a tuple for the two lecture days of the week, returns a list
    of valid dates, removing any that clash with holidays
    """
    sanitized_holidays = []
    for h in holiday_list:
        sanitized_holidays.append(parse(h))


    sanitized_dates = []
    for day in days_of_week:
        if day not in sanitized_holidays:
            sanitized_dates.append(day)

    return sanitized_dates

def day_to_num(day):
    if day == "M":
        return 0
    elif day == "T":
        return 1
    elif day == "W":
        return 2
    elif day == "R":
        return 3
    elif day == "F":
        return 4
    else:
        raise ValueError("day_to_num should contain only chars from" +
                         legal_days_of_week)


def find_first_lect_datetime(start_datetime, days_of_week):
    """
    Note: No longer using this function
    In the case where start_datetime is not the first lecture date, this
    function returns the first lecture's date
    """
    first_day = days_of_week[0]
    dayNum = day_to_num(first_day)

    first_lect = start_datetime
    while first_lect.weekday() != dayNum:
        first_lect = n_days_ahead(first_lect, 1)

    return first_lect


def make_date_list(start_date, weeks, days_of_week, holiday_list):
    """
    return list of date strings in yyyy-mm-dd format

    Example:

    TODO shouldn't the 3 below be 2? As this is for 2 weeks?
     make_date_list("2019-03-31",3,"MW",["2019-04-08","2019-04-09"]) =>
       ["2019-04-01","2019-04-03","2019-04-10"]
    """

    validate_days_of_week(days_of_week)
    start_datetime = parse(start_date)

    final_datetimes = []
    for i in range(weeks):
        start_of_week_datetime = add_weeks(start_datetime,i)
        days_this_week_unsanitized = days_for_this_week(start_of_week_datetime, days_of_week)
        days_this_week_sanitized = days_without_holidays(days_this_week_unsanitized, holiday_list)
        final_datetimes.append(days_this_week_sanitized)

    return final_datetimes


def lecture_gen(path, start_date, weeks, days_of_week, holiday_list):
    """
    Creates a _lectures directory in the given path with premade lecture stubs
    according to the other fields: start date, number of weeks, days of the week
    that the lecture is on, and a list of holidays that lectures can not be held
    on.
    """
    #Create path:
    directory_path = os.path.join(path, "_lectures")
    try:
        os.mkdir(directory_path)
    except OSError:
        print ("Creation of the directory %s failed" % directory_path)
        return
    else:
        print ("Successfully created the directory %s" % directory_path)

    #create valid dates listing:
    valid_dates = make_date_list(start_date, weeks, days_of_week, holiday_list)
    lecture_num = 0
    for dates_by_week in valid_dates:
        for date in dates_by_week:
            lecture_num += 1 #first lecture num will be 1
            filename = "lecture" + str(lecture_num)
            f = open(os.path.join(directory_path, filename), "w+")
            f.write(str(date))
            f.close()

if __name__=="__main__":
    lecture_gen(os.getcwd(), "2019-03-31",2,"MW",["2019-04-08","2019-04-09"])

    """
    print("valid dates 1")
    valid_dates = make_date_list("2019-03-31",2,"MW",["2019-04-08","2019-04-09"])
    print(valid_dates)
    print("valid dates 2")
    valid_dates2 = make_date_list("2019-03-31",2,"MWF",["2019-04-08","2019-04-09"])
    print(valid_dates2)
    print("valid dates 3")
    valid_dates3 = make_date_list("2019-03-31",2,"TWR",["2019-04-08","2019-04-09"])
    print(valid_dates3)
    """
