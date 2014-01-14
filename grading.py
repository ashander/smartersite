#!/opt/local/bin/python

import os
import sys
import re
import string
from subprocess import call
import itertools

re_studentid = re.compile(r"[0-9]{7,9}")

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
    
def openpdfanddoc(listoffiles):
    ''' open pdf and doc files in teh submission directory'''
    filestoopen  = [f for f in listoffiles if f.find('.pdf') != -1 or f.find('.doc') != -1]
    for f in filestoopen:
        filepath = os.path.join(os.getcwd(), submissionsdir, f)
        if sys.platform.startswith('darwin'):
            call(('open', filepath))
        elif os.name == 'nt':
            os.startfile(filepath)
        elif os.name == 'posix':
            call(('xdg-open', filepath))


def main():
    '''
    python grading.py [infile] [gradefile] [hwname] [gradername] [exitfile='notgraded.csv']
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
        exitfile=sys.argv[5]
    except:
        exitfile='notgraded.csv'

    cwd = os.getcwd()
    student_dirs = os.listdir(cwd)

    EDITOR = os.getenv('EDITOR')
    COMMENTFILE = 'comments.txt'
    
    f = open(infile,'r')
    tograde = f.readlines()
    f.close()

    fout = open(gradefile,'w')
    f2 = open(exitfile, 'w')

    keepgoing = True
    for l in tograde:
        ID = re_studentid.search(l,)
        if keepgoing:
            fout.writelines(l.rstrip())
        if (not keepgoing) or (not ID):
            f2.writelines(l)
        if ID and keepgoing:
            curstudent = matchdir(ID.group(), student_dirs)
            os.chdir(curstudent)

            submissionsdir = matchdir('Submission', os.listdir(os.getcwd()))
            subdirfiles = os.listdir(submissionsdir)

            openpdfanddoc(subdirfiles)
            
            comment_header = "Comments on " + hwname + " for " + curstudent 
            comment_footer = "- graded by " + gradername

            output = []
            comment = comment_header + '\n'
            while (comment != 'Q') and (comment != 'q') and (comment != ''):
                output.append(comment + '\n')
                for o in output:
                    print o,
                comment = raw_input("Type a comment (or q/Q/enter to finish and assign a grade)\n")

            grade = raw_input("What is the grade X/5?\n")
            ## no coverage for non convertable input
            while float(grade) > 5.0:
                grade = raw_input("Grade must be less than 5. What is the grade X/5?\n")
            output.append("\nGrade is "+ grade + "/5.0" + '\n')
            output.append('\n' + comment_footer + '\n')
            cmt = open(COMMENTFILE, 'r+')
            cmt.writelines(output)
            cmt.flush()
            cmt.close()
            print "Here is what your commentfile looks like:\n"
            print "---------------beginfile-----------"
            for o in output:
                print o,
            print "---------------endfile-----------\n"
            editit = raw_input("Would you like to edit? Enter y/Y if so.\n")
            if editit == 'Y' or editit == 'y':
                call([EDITOR, COMMENTFILE])
                grade = raw_input("Did you change the grade? If so enter it below X/5. If not hit enter.\n")
                if grade != '':
                    while float(grade) > 5.0:
                        grade = raw_input("Grade must be less than 5. What is the grade X/5?\n")
            print '\n'
            print '\n'
            os.chdir('..')
            fout.writelines(grade)
            fout.writelines('\n')
            escape = raw_input("To keep going hit enter or another key.\nTo quit and save ungraded files, press Q/q:")
            if (escape == 'Q') or (escape == 'q'):
                keepgoing = False
                fout.flush()
                fout.close()
    if keepgoing:
        fout.flush()
        fout.close()
    if not keepgoing:
        f2.flush()
        f2.close()
                
        


        
if __name__=='__main__':
    main()


