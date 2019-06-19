#!/usr/bin/env python3

import argparse
import yaml  # requires pip3 install pyyaml
import json
from json import JSONDecodeError
import pytest
import datetime
import dateutil
import dateutil.parser
import traceback
from dateutil import relativedelta
import sys
import warnings
import os
from os import access, R_OK, W_OK
from os.path import isfile

        
legal_days_of_week={"M":0,"T":1,"W":2,"R":3,"F":4,"S":5,"U":6}

def convert_days_of_week_string_to_list_of_ints(days_of_week):
    global legal_days_of_week

    result = []

    # this code just makes nicer error messages
    stack = traceback.extract_stack()
    filename, codeline, funcName, text = stack[-2]
    err_msg_prefix = "Parameter days_of_week passed from " + funcName + " at line " + str(codeline) + " in file " + filename + " should be a str"
    
    if type(days_of_week)!=str:
       raise ValueError(err_msg_prefix + " should be of type str")

    for c in days_of_week:
        if c not in legal_days_of_week:
          raise ValueError(err_msg_prefix + " contains a char not in MTWRFSU")
        result.append(legal_days_of_week[c])

    return result

def day_to_index(day):
    global legal_days_of_week
    if (type(day) != str) or (len(day)!=1) or (day not in legal_days_of_week):
        raise ValueError("legal values for day are MTWRFSU")
    return legal_days_of_week[day]

def yyyy_mm_dd(date):
    date = make_datetime_datetime(date)
    return date.strftime("%Y-%m-%d")

def make_datetime_datetime(date):

    stack = traceback.extract_stack()
    filename, codeline, funcName, text = stack[-2]
    
    if type(date)==str:
      return dateutil.parser.parse(date)
    if type(date) == datetime.date:
      return datetime.datetime.combine(date, datetime.time(0,0))
    if type(date)==datetime.datetime:
      return date

    msg = "Parameter date passed from " + funcName + " at line " + str(codeline) + " in file " + filename + " should be a str in yyyy-mm-dd format, a datetime.date, or a datetime.datetime"
    raise ValueError(msg)

def make_datetime_datetime_list(date_list):
    '''
    given a list of dates, each of which may be in any reasonable date format
    (i.e. str in yyyy-mm-dd format, datetime.date, or datetime.datetime) convert
    all to datetime.datetime)

    Simply applies make_datetime_datetime to entire list, with nice error handling
    '''

    stack = traceback.extract_stack()
    filename, codeline, funcName, text = stack[-2]

    try:
       return list(map(make_datetime_datetime,date_list))
    except ValueError:
       msg = "Parameter date_list passed from " + funcName + " at line " + str(codeline) + " in file " + filename + " should be a list of items in reasonable date format, including only: str in yyyy-mm-dd format, a datetime.date, or a datetime.datetime"
       raise ValueError(msg) from None

    
def sunday_before(date):
    """
    given a date in either datetime.date, datetime.datetime
     or string "yyyy-mm-dd" format, 
    if that date is
    a sunday, return back that date string. Otherwise, return
    the Sunday immediately prior
    """

    date = make_datetime_datetime(date)
    newdate = date - relativedelta.relativedelta(weekday=relativedelta.SU(-1))
    return newdate

def this_day_is_a_lecture_day(this_day, days_of_week):
    return ("MTWRFSA"[this_day.weekday()] in days_of_week)

def generate_dates(start_date,num_weeks,days_of_week):
    '''
    start_date may be a str in yyyy-mm-dd form, a datetime.date,
    or a datetime.datetime. It may be any day of the week.

    num_weeks should be an integer 

    days_of_week should be a string that consists only of letters from MTWRFSU,
    such as TR, TWR, MWF, etc.

    U is Sunday and S is Saturday

    Return value is a list of objects representing dates
    '''

    start_date = make_datetime_datetime(start_date)
    days_list = convert_days_of_week_string_to_list_of_ints(days_of_week)

    week = 0
    this_day = start_date
    result = []
    while week < num_weeks:
       if this_day_is_a_lecture_day(this_day,days_of_week):
         result.append(this_day)
       this_day = this_day + datetime.timedelta(days=1)  
       if this_day.weekday()==6:
         week += 1
    return result

def dates_without_holidays(datelist, holiday_list):
    datelist = make_datetime_datetime_list(datelist)
    holiday_list = make_datetime_datetime_list(holiday_list)
    return [item for item in datelist if item not in holiday_list]

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
    keys = ['start_date','num_weeks','lecture_days_of_week'] # required keys in YAML file
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

def mkdir_p(newdir):
    """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well

       Source: http://code.activestate.com/recipes/82465-a-friendly-mkdir/
       Note: os.makedirs() already makes all directories in the path but 
        raises an exception if directory already exists.
    """
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("a file with the same name as the desired " \
                      "dir, '%s', already exists." % newdir)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            mkdir_p(head)
        #print "_mkdir %s" % repr(newdir)
        if tail:
            os.mkdir(newdir)

def create_lectures_directory_if_it_does_not_exist(path):

    directory_path = os.path.join(path, "_lectures")
    try:
        mkdir_p(directory_path)
    except OSError:
        print ("Creation of the directory %s failed" % directory_path)
        return None
    else:
        print ("Successfully created the directory %s" % directory_path)
        return directory_path

def write_lecture_file(num, lectures_path, lecture_date, lect_prefix):
        
    lecture_num = ("Lecture {}").format(num)
    lecture_file_name = os.path.join(lectures_path, (lect_prefix + "{0:02d}").format(num) + ".md")
    front_matter = generate_front_matter(lecture_num, lecture_date)
    
    if isfile(lecture_file_name) and access(lecture_file_name, R_OK) and access(lecture_file_name, W_OK):
        with open(lecture_file_name,'r') as f:
            old_contents = f.read()
            if old_contents.startswith(front_matter):
                pass
            else:
                with open(lecture_file_name,'w') as f:
                    f.write(front_matter + "\n" + old_contents)
    elif isfile(lecture_file_name) and not access(lecture_file_name, R_OK):
        print("WARNING: file {} exists but is not readable; skipped".format(lecture_file_name))
    elif isfile(lecture_file_name) and not access(lecture_file_name, W_OK):            
        print("WARNING: file {} exists but is not writable; skipped".format(lecture_file_name))
    else:
        try:
            with open(lecture_file_name, "w") as f:
                f.write(front_matter)
            print("Generated: {}".format(lecture_file_name))
        except:
            print("WARNING: file {} is not writable; skipped".format(lecture_file_name))                
            
    
def lecture_gen(path, lecture_dates, lect_prefix):
    """
    Creates a _lectures directory in the given path with premade lecture stubs
    for the dates given.  Each file is named lectureNN where NN is replaced with
    01, 02, etc.  If that file already exists, if the new front matter is different from 
    the existing from matter, it is prepended to the file.   Thus, running multiple times
    should be the same as running once.  If it does not exist, the file is created.
    """

    lectures_path = create_lectures_directory_if_it_does_not_exist(path)
    lecture_dates = make_datetime_datetime_list(lecture_dates)
    
    for i in range(len(lecture_dates)):
        write_lecture_file(i+1, lectures_path, lecture_dates[i], lect_prefix)
        
    print("{} lecture stubs generated in ".format(len(lecture_dates)),lectures_path)

def generate_front_matter(lecture_num, lecture_date):

    lecture_date = yyyy_mm_dd(lecture_date)
    retval = '''---
num: {0}
lecture_date: {1}
desc:
ready: false
pdfurl:
---
'''.format(lecture_num,lecture_date)
    return retval
        
if __name__=="__main__":

   parser = argparse.ArgumentParser(
       
       description='''
       Generates the _lectures directory for a Jekyll-based course repo

       Uses the values for start_date, num_weeks, lecture_days_of_week
       and cal_dates (with "holiday":true) in _config.yml

       If there is already a _lecture directory, any file that would have
       been overwritten will instead be pre-pended with the new content.
       ''',
       epilog= '''
       For more information, see https://ucsb-cs-course-repos.github.io
       ''')


   parser.add_argument('--yaml_file', metavar='yaml_file',
                       default='_config.yml', type=argparse.FileType('r'),
                       help='yaml file to process (defaults to _config.yml)')

   parser.add_argument('--dir', metavar='dir',
                       default=os.getcwd(), 
                       help='dir in which to create _lectures (defaults to current directory)')

   parser.add_argument('--prefix', metavar='prefix',
                       default='lect', 
                       help='prefix of each file, e.g. "lect" for "lect01", "lect02", etc.  defaults to "lect")')

   
   args = parser.parse_args()
   
   with args.yaml_file as infile:
       yaml_dict = load_yaml_stream(infile)
       result = extract_values_from_yaml_dict(yaml_dict)

   dates = generate_dates(result['start_date'],
                           result['num_weeks'],
                           result['lecture_days_of_week'])
   dates = dates_without_holidays(dates, result['holidays'])    
   lecture_gen(args.dir, dates, args.prefix)   
            
       
# TESTS


def test_day_to_index_bad_input_raises_value_error():
    with pytest.raises(ValueError):
        day_to_index("X")

def test_day_to_index_Sunday():
    assert day_to_index("U")==6

def test_day_to_index_Monday():
    assert day_to_index("M")==0

def test_day_to_index_Friday():
    assert day_to_index("F")==4
    
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


def test_make_datetime_datetime_bad_type():
    with pytest.raises(ValueError):
        make_datetime_datetime(1)

        
def test_convert_days_of_week_string_to_list_of_ints_XYZ():
    with pytest.raises(ValueError):
        convert_days_of_week_string_to_list_of_ints("XYZ")

def test_convert_days_of_week_string_to_list_of_ints_MWF():
    assert convert_days_of_week_string_to_list_of_ints("MWF")==[0,2,4]

def test_generate_dates_simple():
    expected = ["2019-06-18", "2019-06-20",
                "2019-06-25", "2019-06-27"]
    result = generate_dates("2019-06-18",2,"TR")
    assert list(map(yyyy_mm_dd,result))==expected

def test_generate_dates_start_on_thursday():
    expected = ["2018-09-27",
                "2018-10-02", "2018-10-04",
                "2018-10-09", "2018-10-11"]
    result = generate_dates("2018-09-27",3,"TR")
    assert list(map(yyyy_mm_dd,result))==expected

def test_dates_without_holidays_1():

    dates = ["2018-09-27",
                "2018-10-02", "2018-10-04",
                "2018-10-09", "2018-10-11"]
    holidays = ["2018-10-02", "2018-10-11"]
    expected = ["2018-09-27",
                "2018-10-04",
                "2018-10-09"]
    result = dates_without_holidays(dates, holidays)
    assert list(map(yyyy_mm_dd,result))==expected

def test_generate_front_matter_lecture01_2019_06_19():
   expected = '''---
num: lecture01
lecture_date: 2019-06-19
desc:
ready: false
pdfurl:
---
'''
   assert generate_front_matter("lecture01","2019-06-19")==expected

   
