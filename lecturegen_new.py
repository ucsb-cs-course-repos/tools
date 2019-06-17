#!/usr/bin/env python3

import argparse
import yaml  # requires pip3 install pyyaml
import pytest
import datetime
import dateutil
import dateutil.parser
from dateutil import relativedelta
import sys

legal_days_of_week="UMTWRFS"

def day_to_index(day):
    if (type(day) != str) or (len(day)!=1) or (day not in legal_days_of_week):
        raise ValueError("legal values for day are "+legal_days_of_week)
    return legal_days_of_week.index(day)

def yyyy_mm_dd(date):
    return date.strftime("%Y-%m-%d")

def sunday_before(date):
    """
    given a date in either datetime.date, datetime.datetime
     or string "yyyy-mm-dd" format, 
    if that date is
    a sunday, return back that date string. Otherwise, return
    the Sunday immediately prior
    """

    if type(date)==str:
      date = dateutil.parser.parse(date)
    if type(date) == datetime.date:
      date = datetime.datetime.combine(date, datetime.time(0,0))
    if type(date)!=datetime.datetime:
      raise ValueError("illegal date passed to sunday_before")
    newdate = date - relativedelta.relativedelta(weekday=relativedelta.SU(-1))
    return newdate

def load_yaml_file(filename):
    print("Parsing",filename)
    with open(filename, 'r') as stream:
      try:
        return yaml.safe_load(stream)
      except yaml.YAMLError as exc:
        print(exc)
        raise exc

if __name__=="__main__":
   result = load_yaml_file(sys.argv[1])           
   print(result)
   
# TESTS

def test_day_to_index_bad_input_raises_value_error():
    with pytest.raises(ValueError):
        day_to_index("X")

def test_day_to_index_Sunday():
    assert day_to_index("U")==0

def test_day_to_index_Monday():
    assert day_to_index("M")==1

def test_day_to_index_Friday():
    assert day_to_index("F")==5
    
def test_sunday_before_bad_date_raises_value_error():
    with pytest.raises(ValueError):
       sunday_before("bad_date")
    
def test_sunday_before_bad_date_raises_value_error():
    with pytest.raises(ValueError):
       sunday_before(12)

def test_sunday_before_is_fixed_point_if_already_Sunday():
    assert yyyy_mm_dd(sunday_before("2019-06-16"))=="2019-06-16"

def test_sunday_before_is_fixed_point_if_not_already_Sunday():
    assert yyyy_mm_dd(sunday_before("2019-06-17"))=="2019-06-16"

def test_sunday_before_works_on_datetime_datetime_values():
    arg = dateutil.parser.parse("2019-06-17")
    assert type(arg) == datetime.datetime
    result = sunday_before(arg)
    assert yyyy_mm_dd(result)=="2019-06-16"

def test_sunday_before_works_on_datetime_date_values():
    arg = datetime.date(2019, 6, 18)
    assert type(arg) == datetime.date
    result = sunday_before(arg)
    assert yyyy_mm_dd(result)=="2019-06-16"



    
