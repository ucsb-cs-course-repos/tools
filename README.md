# tools

 * `lecture-gen.py`: given a start date for the quarter, a string such as MW, TR, and a number of weeks, and a list of dates for campus-holidays, produce a directory `_lecture/lect01.md`, etc. with the correct default front matter at the top.

* `hwk-gen.py`: NOT FINISHED. Similar to lecture gen but instead creates stubs for hwk assign dates and hwk due dates. Definitely not working yet.

# How to Run:
* Set config variables at top of lecture-gen.py for your specific course.
  * Some are optional to change: ex. PATH, OUTPUT_DIR_NAME, BASE_LECTURE_NAME
  * Optional: set path to a desired path (default is the users' current path, wherever the user runs lecture-gen.py)

Run lecture-gen.py with python3 ($ python3 lecture-gen.py)
* In the case of "directory already exists error" this means that the "_lectures" directory already existed where the program tried to create the new _lectures directory.
  * If that old directory is deleted, or a different path is specified, the directory should create succesfully.
