#!/usr/bin/env python


import argparse
import pytest

legal_days_of_week="MTWRF"

def validate_days_of_week(days_of_week)
    for c in days_of_week:n
        if c not in legal_days_of_week
          raise ValueError("days_of_week should contain only chars from" +
                           legal_days_of_week)
    

def validate_date(date):
     result = datetime.utcfromtimestamp(date) # raises ValueError if illegal value
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
    pass
 
def make_date_list(start_date, weeks, days_of_week, holiday_list):
    """
    return list of date strings in yyyy-mm-dd format

    Example: 
     make_date_list("2019-03-31",3,MW,["2019-04-08",2019-04-09"]) =>
       ["2019-04-01","2019-04-03","2019-04-10"]
    """
    
    validate_days_of_week(days_of_week)
    start_datetime = validate_date(start_date)

    for i in range(weeks):
        start_of_week_datetime = add_weeks(start_datetime,weeks)
        for c in days_of_week:
            this_datetime = compute_datetime(start_
    
def lecture_gen()
   pass





if __name__=="__main__":
    lecture_gen()
