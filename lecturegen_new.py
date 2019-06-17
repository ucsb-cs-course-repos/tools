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

def sunday_before(date_yyyy_mm_dd):
    """
    given a date in "yyyy-mm-dd" format, if that date is
    a sunday, return back that date string. Otherwise, return
    the Sunday immediately prior
    """

    date = dateutil.parser.parse(date_yyyy_mm_dd)
    newdate = date - relativedelta.relativedelta(weekday=relativedelta.SU(-1))
    return newdate.strftime("%Y-%m-%d")

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
       sunday_before("bad_date")

def test_sunday_before_is_fixed_point_if_already_Sunday():
    assert sunday_before("2019-06-16")=="2019-06-16"

def test_sunday_before_is_fixed_point_if_not_already_Sunday():
    assert sunday_before("2019-06-17")=="2019-06-16"

    
