smartersite
===========

Doing things (for now grading) with files from UC Davis smartsite

## grading.py

Most of the action is in grading.py, for information run:

```python
python grading.py -h 
```
To be useful, this program must be run in the root of a directory tree as 
unzipped from a `bulk_download.zip` file as provided by the 'Grade' link 
in a smartsite Assignment.

The program will attempt to open submissions (.doc or .pdf as of now) and prompt 
the user for comments through the command line. 

You have an option to edit those comments (if $EDITOR is set in your shell).

It prompts for a grade (must be <= 5 as of now) and if that grade is provided, 
includes it in the comments and also the grade to an output file with the 
format of grades.csv.

In a given 'session' of grading, any students for which grades aren't provided
are written into an output file (also with the format of grades.csv) but with no
grades.

The script takes arguments that allow you to grade only students in specified section, 
so long as an appropriate csv file to look up section membership is provided.
There are also `R`-based tools to construct such a csv from Excel files downloaded
from smartsite (see 'R scripts' below).

## a workflow

1. download a zip archive from smartsite using bulk_download.zip
2. unpack it, which creates a single directory eg. to `Homework _ Lab 1`
3. `cd` to that directory
4. run `grading.py` as below (arguments to grade section 2 only)

```sh
~/TAwd/Homework _ Lab 1$ python ../grading.py -lu ../currentlut.csv -s 2 grades.csv outgrades.csv 'hw test' jaime notgraded.csv
# do some grading
# at some point, be done grading and exit by pressing `q` or `Q` at the appropriate prompt
```

5. next time, run the same script but with `notgraded.csv` as the input, 
```sh
~/TAwd/Homework _ Lab 1$ python ../grading.py -lu ../currentlut.csv -s 2 notgraded.csv outgrades2.csv 'hw test' jaime notgraded2.csv
# do some grading
# at some point, be done grading and exit by pressing `q` or `Q` at the appropriate prompt
```

6. assuming you graded the rest of the section's assignments in this session, you have grades spread 
across two files, `outgrades.csv` and `outgrades2.csv`, use `Rscript stackcsv.R` to combine, but first delete 
grades.csv, 
```sh
rm grades.csv
Rscript stackcsv.R outgrades.csv outgrades2.csv grades.csv
rm outgrades* notgraded.csv #cleanup 
```

7. zip up the entire directory and use 'Upload all' from smartsite to upload it. It's OK that `grades.csv` doesn't
contain a grade for every student sub directory. 

## R scripts

Two `.R` scripts are for processing excel files provided by smartsite into
lookup tables for section membership.

Another `.R` script is for stacking csvs that are like `grades.csv` provided by smartsite.

