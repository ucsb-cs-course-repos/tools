# tools

 * `lecture-gen.py`: given a start date for the quarter, a string such as MW, TR, and a number of weeks, and a list of dates for campus-holidays, produce a directory `_lecture/lect01.md`, etc. with the correct default front matter at the top.
   * Also can be extended to set up hwk file stubs, see below.


# How to Run:
* Set config variables at top of lecture-gen.py for your specific course.
  * Some are optional to change: ex. PATH, OUTPUT_DIR_NAME, BASE_LECTURE_NAME
    * Optional: set path to a desired path (default is the users' current path, wherever the user runs lecture-gen.py)
* To use as a way to create hwk file stubs:
  * Set the config variables to output hwk things (ex change OUTPUT_DIR_NAME to "_hwk" and BASE_FILE_NAME to "hwk")
  * For now, no support for separate "hwk_assign" and "hwk_due" seperate files--right now the program in one run can only create one type of output file
    * i.e. can create stubs for hwk_assign files if homework is assigned the same day of the week, and a seperate run of the program to create hwk_due file stubs if homework is always due on same day of week
      * Warning: A holiday can lead to mismatched homework assign/due dates because the entire week would be skipped if a hwk_due file lands on a holiday


Run lecture-gen.py with python3 ($ python3 lecture-gen.py)
* In the case of "directory already exists error" this means that the "_lectures" directory already existed where the program tried to create the new _lectures directory.
  * If that old directory is deleted, or a different path is specified, the directory should create succesfully.
