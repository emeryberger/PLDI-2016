These are some of the scripts used to manage the PLDI 2016 review process.
These operate on CSV files downloaded from HotCRP.

They have been released into the public domain and may be freely used.

-----

prefs-checker.py: prints sorted list of # of bids (prefs) placed per reviewer
  - used to keep track of bidding progress.

conflict-vetter.py: finds all stated conflicts from authors and mails them for vetting to reviewers
  - used for checking for bogus conflicts / conflict engineering.

extract-json-ecoop.py: converts JSON files (as exported from ECOOP) into .csv format
  - used for checking for simultaneous submission to ECOOP & PLDI.

conflict-pcprefs.py:
  - used to generate file for David Walker's scripts, which were not used


