# tools

* `lecturegen.py`: uses the values in the `_config.yml` file to set up the `_lectures` directory.  If you
  already have content in that directory, it will prepend the new front matter to the top of each file,
  so you don't lose any of your content.  It takes into account campus holidays as long as you set
  `"holiday":True` in the `cal_dates` JSON value.
  

* `set_ready_false.py`: sets all of the values of ready to false in the .md files in the target
  directory.

  Note that this file parses and re-outputs the YAML.  Accordingly, it may make changes to the YAML
  source that nevertheless preserve the meaning of the code (e.g. reordering keys, removing
  redundant quotes).


 
