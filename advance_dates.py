#!/usr/bin/env python3

import argparse
import glob
import os
import yaml

import datetime
import dateutil
import dateutil.parser
from lecturegen import make_datetime_datetime

def separate_front_matter(list_of_strings):
   
   # define default retval for if there is no front_matter
   retval = {'front_matter':[],
             'rest':list_of_strings}

   if list_of_strings[0]!='---\n':
      return retval

   index_second_hyphen = 0
   for i in range(1,len(list_of_strings)):
      if list_of_strings[i]=='---\n':
         index_second_hyphen = i
         break
         
   if index_second_hyphen == 0:
      return retval

   return {'front_matter' : list_of_strings[0:index_second_hyphen+1],
           'rest' : list_of_strings[index_second_hyphen+1:]}

def read_lines(f):
   with open(f,'r') as infile:
      return infile.readlines()

def write_lines(f,data):

   with open(f,'w') as outfile:
      for d in data:
         outfile.write(d)

def advance_dates(contents,delta):

   yaml_string = "\n".join(contents['front_matter'][1:-1])
   yaml_doc = yaml.safe_load(yaml_string)

   if yaml_doc and 'assigned' in yaml_doc:
      assigned = make_datetime_datetime(yaml_doc['assigned'])
      assigned = assigned + datetime.timedelta(days=delta)                                       
      yaml_doc['assigned'] = assigned.strftime("%Y-%m-%d %H:%M")
   else:
      print("no assigned in " + str(yaml_doc))
      
   if yaml_doc and 'due' in yaml_doc:
      due = make_datetime_datetime(yaml_doc['due'])
      due = due + datetime.timedelta(days=delta)               
      yaml_doc['due'] = due.strftime("%Y-%m-%d %H:%M")                        
   else:
      print("no due in " + str(yaml_doc))
      
   yaml_lines = yaml.dump(yaml_doc).split("\n")
   yaml_lines = list(map(lambda x : x+"\n", yaml_lines))                        
   contents['front_matter']= ["---\n"] + yaml_lines + ["---\n"]
   return contents

         
if __name__=="__main__":

   parser = argparse.ArgumentParser(
       
       description='''
       Advance the assigned and due dates in front matter by some delta.
       Can move dates backwards by using negative delta.

       Affects all .md files in the directory specified.

       ''',
       epilog= '''

       To calculate delta, enter a string like this into Google Search:

       how many days between 2018-01-23 and 2019-08-06

       For more information, see https://ucsb-cs-course-repos.github.io
       ''')


   parser.add_argument('--dir', metavar='dir',
                       default=os.getcwd(), 
                       help='dir in which to advance .md files (defaults to current directory)')

   parser.add_argument('--delta', metavar='delta',
                       default=90, type=int,
                       help='days to move the calendar forward (default 90)')

   
   args = parser.parse_args()
   
   md_files = glob.glob(args.dir + "/*.md")

   for f in md_files:
      
      data = read_lines(f)
      contents = separate_front_matter(data)
      write_lines(f + ".backup", data)
            
      contents = advance_dates(contents,args.delta)
      
      # write new version
      data = contents['front_matter'] + contents['rest']
      write_lines(f,data)

# TESTS
   
def test_separate_front_matter_no_front_matter():
   contents='''no
   front
   matter
   '''.split("\n")

   contents = list(map(lambda x: x + "\n", contents))

   expected = {"front_matter":[],
               "rest": contents}

   assert separate_front_matter(contents)==expected


def test_separate_front_matter_no_front_matter_but_starts():
   contents='''---
   still 
   no
   matter
   '''.split("\n")

   contents = list(map(lambda x: x + "\n", contents))

   expected = {"front_matter":[],
               "rest": contents}

   assert separate_front_matter(contents)==expected


def test_separate_front_matter_has_front_matter():
   contents='''---
x
y
z
---
a
b
c
'''.split("\n")

   contents = list(map(lambda x: x + "\n", contents))
   expected = {"front_matter" :
               ["---\n",
                "x\n",
                "y\n",
                "z\n",
                "---\n"],
               "rest":
               ["a\n",
                "b\n",
                "c\n",
                "\n"]}

   assert separate_front_matter(contents)==expected

