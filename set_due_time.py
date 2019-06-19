#!/usr/bin/env python3

import argparse
import glob
import os
import yaml

import datetime
import dateutil
import dateutil.parser
from lecturegen import make_datetime_datetime

from advance_dates import separate_front_matter
from advance_dates import read_lines
from advance_dates import write_lines

import pytest

def set_due_time(contents,new_hour,new_minute):

   yaml_string = "\n".join(contents['front_matter'][1:-1])
   yaml_doc = yaml.safe_load(yaml_string)

      
   if 'due' in yaml_doc:
      due = make_datetime_datetime(yaml_doc['due'])
      due = due.replace(hour=new_hour, minute=new_minute)
      yaml_doc['due'] = due.strftime("%Y-%m-%d %H:%M")
      print("yaml_doc['due']",yaml_doc['due'])
   else:
      print("no due in " + str(yaml_doc))
      
   yaml_lines = yaml.dump(yaml_doc).split("\n")
   yaml_lines = list(map(lambda x : x+"\n", yaml_lines))                        
   contents['front_matter']= ["---\n"] + yaml_lines + ["---\n"]
   return contents

def parse_time(hh_mm):
      
     error_message = "argument --time should be a hh:mm formatted time"
     split_time = hh_mm.split(":")
     if len(split_time)!=2:
       raise ValueError(error_message)
     try:
        hour = int(split_time[0])
        if hour < 0 or hour > 23:
           raise ValueError(error_message)
        min = int(split_time[1])
        if min < 0 or min > 59:
           raise ValueError(error_message)
     except:
        raise ValueError(error_message)
     return {"hh":hour, "mm": min} 

  
if __name__=="__main__":

   parser = argparse.ArgumentParser(
       
       description='''
       Set due time in front matter of all .md files to time in --time argument

       ''',
       epilog= '''
       For more information, see https://ucsb-cs-course-repos.github.io
       ''')


   parser.add_argument('--dir', metavar='dir',
                       default=os.getcwd(), 
                       help='dir in which to set ready to false (defaults to current directory)')

   parser.add_argument('--time', metavar='time',
                       help='time in hh:mm format, 24 hour clock, e.g. 09:30 or 14:00')

   
   args = parser.parse_args()

   time = parse_time(args.time)
   print("time",time)
   
   md_files = glob.glob(args.dir + "/*.md")

   for f in md_files:
      
      data = read_lines(f)
      contents = separate_front_matter(data)
      write_lines(f + ".backup", data)

      contents = set_due_time(contents, time['hh'], time['mm'])
      
      # write new version
      data = contents['front_matter'] + contents['rest']
      write_lines(f,data)

# TESTS


def test_parse_time_bad1():
   with pytest.raises(ValueError):
      parse_time("1234")
 
def test_parse_time_bad1():
   with pytest.raises(ValueError):
      parse_time("2:30pm")

def test_parse_time_14_30():
   assert parse_time("14:30")=={"hh":14, "mm":30}

def test_parse_time_09_00():
   assert parse_time("09:00")=={"hh":9, "mm":0}

      
