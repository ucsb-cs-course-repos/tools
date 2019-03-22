# tools

 * `lecture-gen.py`: given a start date for the quarter, a string such as MW, TR, and a number of weeks, and a list of dates for campus-holidays, produce a directory `_lecture/lect01.md`, etc. with the correct default front matter at the top.

# How to Run:
* For now, in "if __name__=="__main__":" block: Set the fields start_date, weeks, days_of_week, and holiday_list for the class.
* Optional: set path to a desired path (default is the users' current path, wherever the user runs lecture-gen.py)

Run lecture-gen.py with python3 ($ python3 lecture-gen.py)
* In the case of "directory already exists error" this means that the "_lectures" directory already existed where the program tried to create the new _lectures directory.
