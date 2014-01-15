#!/opt/local/bin/python
# need python 2.7 or greater

import os
import sys
import re
import string
import csv
from subprocess import call
import argparse

        



# compile a couple global regex
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
    ## [todo] - handle non convertable input other than ''
    if grade != '':
        while float(grade) > 5.0:
            grade = raw_input("Grade must be less than 5. What is the grade X/5?\n")
    return grade
           
def main(infile, gradefile, hwname, gradername, gradesection, lutfile, exitfile):
    # args contains: infile, gradefile, hwname, gradername, gradesection, lutfile, exitfile

    gradesection = 'A0' + str(gradesection)
    sectionlookup = sectiondict(lutfile)

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
            try:
                section = sectionlookup[username.group().strip(',')]
            except KeyError:
                continue # the student has no section assigned
            except:
                section = gradesection #if something else happens, be a nice guy
            if section != gradesection:
                continue

        if (not ID):
            ngf.writelines(l)
            if keepgoing:
                gf.writelines(l)

        if ID:
            if keepgoing:
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
    parser = argparse.ArgumentParser(description =
                                     '''Do grading in a directory tree from an unpacked zip as provided by smartsite.
                                     This command should be executed at the root of the tree with grades.csv.''')
    section = parser.add_argument_group('section')
    section.add_argument('-s', '--gradesection',
        metavar='section_to_grade', type=int, help="section number to grade (integer, 'A0' will be added). Requires an lutfile to work.",
        default=False)
    section.add_argument('-lu', '--lutfile',
        metavar='lookup_table_in_csv', type=str,
        help='File with columns of user ids and section numbers. Only valid with -s specified.')

    
    parser.add_argument(
        'infile', metavar='input_file_to_grade', type=str, help='input file with grades, eg grades.csv provided by smartsite',
        default='grades.csv')
    parser.add_argument(
        'gradefile', metavar='graded_output_file', type=str, help='output file for grades, eg gradesout.csv',
        default='grades.csv.bak')
    parser.add_argument(
        'hwname', metavar='homework_name_for_header', type=str, help='name of homework for header')
    parser.add_argument(
        'gradername', metavar='grader_name_for_footer', type=str, help='name of grader for footer',
        default=os.uname()[1])    
    parser.add_argument(
        'exitfile', metavar='ungraded_output_file', type=str,
        help='output file for ungraded assignments during a grading session',
        default='notgraded.csv')

    args = parser.parse_args()
    if (args.gradesection and not args.lutfile) or (not args.gradesection and args.lutfile):
         parser.print_help()
         sys.exit()
        
    if args.gradesection:
        print "grading section A0 " + str(args.gradesection)
        print "using lookup table based on " + args.lutfile
        
    main(args.infile, args.gradefile, args.hwname, args.gradername, args.gradesection, args.lutfile, args.exitfile)
