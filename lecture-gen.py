#!/usr/bin/env python


import argparse
import pytest
import datetime
import dateutil
from dateutil.parser import *

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

def days_for_this_week(start_datetime):
    """
    Return a tuple of two datetimes, one for each lecture day
    start_datetime is the first lecture day of the week, the second
    is calculated by start_datetime + 2 days days_ahead

    Warning: Does not account for holidays (see days_without_holidays)
    """

    day_one = start_datetime
    day_two = n_days_ahead(start_datetime, 2)
    return (day_one, day_two)

def days_without_holidays(days_of_week, holiday_list):
    """
    Given a tuple for the two lecture days of the week, returns a list
    of valid dates, removing any that clash with holidays
    """
    sanitized_holidays = []
    for h in holiday_list:
        sanitized_holidays.append(parse(h))


    sanitized_dates = []
    if days_of_week[0] not in sanitized_holidays:
        sanitized_dates.append(days_of_week[0])
    if days_of_week[1] not in sanitized_holidays:
        sanitized_dates.append(days_of_week[1])

    return sanitized_dates

def make_date_list(start_date, weeks, days_of_week, holiday_list):
    """
    return list of date strings in yyyy-mm-dd format

    Example:

    TODO shouldn't the 3 below be 2? As this is for 2 weeks?
     make_date_list("2019-03-31",3,"MW",["2019-04-08","2019-04-09"]) =>
       ["2019-04-01","2019-04-03","2019-04-10"]
    """

    validate_days_of_week(days_of_week)
    #start_datetime = validate_date(parse(start_date))
    start_datetime = parse(start_date)

    final_datetimes = []
    for i in range(weeks):
        start_of_week_datetime = add_weeks(start_datetime,i)
        days_this_week_unsanitized = days_for_this_week(start_of_week_datetime)
        days_this_week_sanitized = days_without_holidays(days_this_week_unsanitized, holiday_list)
        final_datetimes.append(days_this_week_sanitized)

    return final_datetimes


def lecture_gen():
   pass


if __name__=="__main__":
    #lecture_gen()
    valid_dates = make_date_list("2019-04-01",2,"MW",["2019-04-08","2019-04-09"])
    print(valid_dates)
