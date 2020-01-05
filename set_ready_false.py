#!/usr/bin/env python3

import argparse
import glob
import os
import yaml

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

def set_ready_to_false(contents):
   yaml_string = "\n".join(contents['front_matter'][1:-1])
   yaml_doc = yaml.safe_load(yaml_string)
   yaml_doc['ready']=False
   yaml_lines = yaml.dump(yaml_doc, default_flow_style=False).split("\n")
   yaml_lines = list(map(lambda x : x+"\n", yaml_lines))                        
   contents['front_matter']= ["---\n"] + yaml_lines + ["---\n"]
   return contents

         
if __name__=="__main__":

   parser = argparse.ArgumentParser(
       
       description='''
       Set ready to false in all .md files in --dir argument 
       (default: current directory)

       ''',
       epilog= '''
       For more information, see https://ucsb-cs-course-repos.github.io
       ''')


   parser.add_argument('--dir', metavar='dir',
                       default=os.getcwd(), 
                       help='dir in which to set ready to false (defaults to current directory)')

   args = parser.parse_args()
   
   md_files = glob.glob(args.dir + "/*.md")

   for f in md_files:
      
      data = read_lines(f)
      contents = separate_front_matter(data)
      write_lines(f + ".backup", data)
            
      contents = set_ready_to_false(contents)
      
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

