# tools

* `lecturegen.py`: uses the values in the `_config.yml` file to set up the `_lectures` directory.  If you
  already have content in that directory, it will prepend the new front matter to the top of each file,
  so you don't lose any of your content.  It takes into account campus holidays as long as you set
  `"holiday":True` in the `cal_dates` JSON value.
  

* `set_ready_false.py`: sets all of the values of ready to false in the .md files in the target
  directory.

  Can be used at the start of a new term when reusing old material to mark it ready: false
  until the instructor has had a chance to review it.
  
  Note that this file parses and re-outputs the YAML.  Accordingly, it may make changes to the YAML
  source that nevertheless preserve the meaning of the code (e.g. reordering keys, removing
  redundant quotes).


* `advance_dates.py`: advances all assigned and due dates by some number of days (the "delta")

  Can be used at the start of a new term when reusing older material to move all the dates forwards
  by the delta between an old terms start date and the new terms start date.

  A negative amount can be used to nudge all the dates backwards by one or two days.

  Note that this file parses and re-outputs the YAML.  Accordingly, it may make changes to the YAML
  source that nevertheless preserve the meaning of the code (e.g. reordering keys, removing
  redundant quotes).

* `set_due_time.py`: sets the time of all `due` dates in the given directory

  Can be used at the start of a new term when reusing older material to change the
  times that assignments are due to some desired time (e.g. start of lecture time, 23:59, or whenever)

  Note that this file parses and re-outputs the YAML.  Accordingly, it may make changes to the YAML
  source that nevertheless preserve the meaning of the code (e.g. reordering keys, removing
  redundant quotes).

 
