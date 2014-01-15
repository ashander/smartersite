#!/opt/local/bin/python

import os
import sys
import re
import string
import csv
from subprocess import call


# compile a global regex
re_studentid = re.compile(r"[0-9]{7,9}")
re_studentusername = re.compile(r"[a-z]*,")


def matchdir (string, dirlist):
    '''
    return full entry of dirlist that
    contains a partial match for string s
    or
    False
    '''
    outlist = [d for d in dirlist if d.find(string) != -1]
    if len(outlist) == 0:
        return False
    else:
        return outlist.pop()

def sectiondict (filename):
    ''' filename should be loc for LUT with student
    user ids as first column'''
    with open(filename, 'r') as f:
        res = {}

        reader = csv.reader(f)
        reader.next()
        for row in reader:
            k, v = row
            res[k] = v
        return res
    
def openpdfanddoc(dir, listoffiles):
    ''' open pdf and doc files in teh submission directory'''
    filestoopen  = [f for f in listoffiles if f.find('.pdf') != -1 or f.find('.doc') != -1]
    for f in filestoopen:
        filepath = os.path.join(os.getcwd(), dir, f)
        if sys.platform.startswith('darwin'):
            call(('open', filepath))
        elif os.name == 'nt':
            os.startfile(filepath)
        elif os.name == 'posix':
            call(('xdg-open', filepath))

def writecomments(comment_header):
    ''' until user types q/Q/enter, solicit comments and put them on new 'lines'
    of the output 'file' (actually a list)
    print the full file with each new line
    '''
    output = []
    comment = comment_header + '\n'
    while (comment != 'Q') and (comment != 'q') and (comment != ''):
        output.append(comment + '\n')
        for o in output:
            print o,
        comment = raw_input("Type a comment (or q/Q/enter to finish and assign a grade)\n")
    return output

def getgrade(graderequeststring):
    ''' get grade as string ''' 
    grade = raw_input(graderequeststring)
    ## [todo] - handle non convertable input
    if grade != '':
        while float(grade) > 5.0:
            grade = raw_input("Grade must be less than 5. What is the grade X/5?\n")
    return grade
           
def main():
    '''
    python grading.py [infile] [gradefile] [hwname] [gradername] [gradesection] [sectionlut ='../sectionlut.csv'] [exitfile='notgraded.csv'] 
    '''
    # [todo] - should replace below with argparser module
    try:
        infile=sys.argv[1]
    except:
        infile = 'grades.csv'
    try:
        gradefile = sys.argv[2]
    except:
        gradefile = infile+'.bak'
        print "graded output will be put in grades.csv.bak\n"
    try:
        hwname = sys.argv[3]
    except:
        hwname = 'Comments on Homework ___ '

    try:
        gradername= sys.argv[4]
    except:
        gradername = os.uname()[1]
    try:
        gradesection = sys.argv[5]
        if int(gradesection):
            gradesection = 'A0' + gradesection
    except:
        gradesection = False
    try:
        lutfile = sys.argv[6]
        print lutfile
    except:
        lutfile = "../sectionlut.csv"
    try:
        exitfile=sys.argv[7]
    except:
        exitfile='notgraded.csv'
        

    sectionlookup = sectiondict(lutfile)
    print sectionlookup
    cwd = os.getcwd()
    student_dirs = os.listdir(cwd)

    EDITOR = os.getenv('EDITOR')
    COMMENTFILE = 'comments.txt'

    comment_footer = "- graded by " + gradername

    
    tgf = open(infile,'r')
    tograde = tgf.readlines()
    tgf.close()

    gf = open(gradefile,'w')
    ngf = open(exitfile, 'w')

    keepgoing = True
    for l in tograde:
        ID = re_studentid.search(l,)

        if ID and gradesection:
            username = re_studentusername.match(l,)
            ## need to strip , from match group. should find more generalized soln
            if sectionlookup[username.group().strip(',')] != gradesection:
                continue
            
        if (not ID) and keepgoing:
            ngf.writelines(l)
            gf.writelines(l)
        else:
            if not keepgoing:
                ngf.writelines(l)

        if ID and keepgoing:
            gf.writelines(l.rstrip())
            curstudent = matchdir(ID.group(), student_dirs)
            os.chdir(curstudent)

            submissionsdir = matchdir('Submission', os.listdir(os.getcwd()))
            subdirfiles = os.listdir(submissionsdir)

            openpdfanddoc(submissionsdir, subdirfiles)
            
            comment_header = "Comments on " + hwname + " for " + curstudent 

            output = writecomments(comment_header)
            grade = getgrade("What is the grade X/5? (If no grade at this time hit enter.)\n")
            
            output.append("\nGrade is "+ grade + "/5.0" + '\n')            
            output.append('\n' + comment_footer + '\n')

            cmt = open(COMMENTFILE, 'r+')
            print "Here is what your commentfile looks like:\n"
            print "---------------beginfile-----------"
            for o in output:
                print o,
                cmt.writelines(o)
            cmt.flush()
            cmt.close()
            print "---------------endfile-----------\n"


            editit = raw_input("Would you like to edit? Enter y/Y if so.\n")
            if editit == 'Y' or editit == 'y':
                call([EDITOR, COMMENTFILE])
                grade = getgrade("Did you change the grade? If so enter it below X/5. If not hit enter.\n")

            print '\n'

            os.chdir('..')
            gf.writelines(grade)
            gf.writelines('\n')
            escape = raw_input("To keep going hit enter or another key.\nTo quit and save ungraded files, press Q/q:")
            if (escape == 'Q') or (escape == 'q'):
                keepgoing = False
                gf.flush()
                gf.close()
                

    if keepgoing:
        gf.flush()
        gf.close()
        
    if not keepgoing:
        ngf.flush()
        ngf.close()
                
        


        
if __name__=='__main__':
    main()


