smartersite
===========

Doing things (for now grading) with files from UC Davis smartsite

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

The two .R scripts are for processing excel files provided by smartsite into
lookup tables for section membership.

