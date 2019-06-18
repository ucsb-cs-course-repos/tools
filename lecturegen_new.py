#!/usr/bin/env python3

import argparse
import yaml  # requires pip3 install pyyaml
import json
from json import JSONDecodeError
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

def load_yaml_stream(stream):
    try:
        return yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        raise exc

def extract_value(yaml_dict, key, result):
    if type(result)!=dict:
        raise ValueError("param result to extract_value should be of type dict")
    if key not in yaml_dict:
      raise ValueError("Key '" + key + "' should be in YAML file")
    result[key]=yaml_dict[key]
  
def extract_values_from_yaml_dict(yaml_dict):
    result = {}
    keys = ['start_date','num_weeks']
    for k in keys:
        extract_value(yaml_dict, k, result)

    # treat cal_dates special, since we have to also extract holidays
    # from the JSON
    result['holidays']=[]
    cal_dates_dict = {}
    extract_value(yaml_dict, 'cal_dates', cal_dates_dict)
    cal_dates_json=yaml_dict['cal_dates']
    try:
      cal_dates = json.loads(cal_dates_json)
    except JSONDecodeError:
      print("json for 'cal_dates' in YAML file is malformed")
      print("malformed JSON: ",cal_dates_json)
      raise ValueError("json for 'cal_dates' in YAML file is malformed") from None
    if type(cal_dates) != list:
      raise ValueError("Key 'cal_dates' in YAML file should be a list of objects in JSON format")
    for d in cal_dates:
      if ('holiday' in d) and (d['holiday']==True):
         if 'date' not in d:
            raise ValueError("JSON for 'cal_dates'in YAML file has a member with 'holiday:True' but no value for 'date'")
         result['holidays'].append(d['date'])
    return result
         
if __name__=="__main__":

   parser = argparse.ArgumentParser(
       
       description='''
       Given a start date, number of weeks, and list of holidays,
       either as command line arguments, or provided in a _config.yml
       file, produces a _lecture directory suitable for use with Jekyll.

       If there is already a _lecture directory, any file that would have
       been overwritten will instead be pre-pended with the new content.
       ''',
       epilog= '''
       For more information, see https://ucsb-cs-course-repos.github.io
       ''')

   parser.add_argument('yaml_file', type=argparse.FileType('r'))
   args = parser.parse_args()
   
   with args.yaml_file as infile:
       yaml_dict = load_yaml_stream(infile)
       result = extract_values_from_yaml_dict(yaml_dict)
       print("result=",result)
   
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



    
