# Ed-assign

This repo implements a basic tool to create Ed assignments for CS50. It requires the Staff Roster, and some configuration over the number of roles, and the dates for which assignments are required, and generates a CSV file of random assignments. It ensures that a staff member is never assigned more than once per day, and that everyone is assigned an almost equal number of Ed roles. If the number of roles is not cleanly divisible by the number of staff, CAs will be the first to be given an extra Ed shift, then TFs, then Head TFs.

## Requirements

This requires a `python` installation with `pandas` installed.

## Configuration

The first method in the class should guide you through configuring the script, but here are step-by-step instructions:

1) Download the staff roster as a CSV by exporting it from the google sheet.

2) Place that file in the data folder, and update `self.staff_roster_file` accordingly, where this contains the     `path` to the file, so remember `data/` (please remember to put it in the `data` folder so that it is ignored by `git` so nobody's information is ever stored in the repo by accident. CSVs and xlsx files are also untracked, but just in case).

3) Set `self.config` according to the number of staff desired for each role required.

4) Set `self.dates` as required for the semester. Create the `dates` object to contain all the dates for the semester where staff are needed for Ed, and then set `dates_to_remove` to any dates where staff shouldn't be looking at Ed (e.g. Thanksgiving, Spring Break etc.)

5) (OPTIONAL) update `self.output_file_path` to rename the file produced as desired.

## Usage

See 'Configuration' and then run `python schedule.py`.

Then import this CSV file to the Google Sheet and follow instructions there.

## Known issues

I know that technically there is an issue in my switch functionality. However, that will never apply unless the cs50 staff shrinks to 1/4 of its current size or less perhaps. If that happens, you may need to fix my switch functionality. Or probably just write something new :)

Any other issues, feel free to email me at aholmes@college.harvard.edu.

## Other notes

Hermione is the term I use for someone who is initially assigned to roles on the same day more than once, in the spirit of Hermione being at two classes at once. The initial assignment can permit some Hermione-like behavior, but it is checked for at the end and corrected. If Hermione-like behavior is detected, it should print the assignemnt(s) for days with Hermione-like characters, and then 'Hermione resolved!' and the updated assignments for those days.