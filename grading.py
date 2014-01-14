#!/opt/local/bin/python

import os
import sys
import re
import string
from subprocess import call
import tempfile

re_studentid_file = re.compile(r",[0-9]*,")
#re_studentid_dir = re.compile(r"\([0-9]*\)")

re_studentid = re.compile(r"[0-9]{7,9}")

def main():
    try:
         hwname = sys.argv[1]
         gradername= sys.argv[2]
         writefile = sys.argv[3]
    except:
         hwname = 'Comments on Homework ___ '
         gradername = os.uname()[1]

    cwd = os.getcwd()
    student_dirs = os.listdir(cwd)

    EDITOR = os.getenv('EDITOR')
    COMMENTFILE = 'comments.txt'
    
    f = open('grades.csv','r')
    fout = open(writefile,'w')
    for l in f:
        ID = re_studentid.search(l,)
        fout.writelines(l.rstrip()) 
        if ID:

            
            dir_matches = [re.search(ID.group(), s) for s in student_dirs]
            td = [d for d in dir_matches if d] # should be length 1 list with only match
            if len(td) != 1:
                "ERROR %r matches in directories, expected 1" % len(td)
            dir_index = dir_matches.index(td[0]) # loc in student_dirs of match

            os.chdir(student_dirs[dir_index])

            dircont = os.listdir(os.getcwd())
            submatch = [re.search('Submission', d) for d in dircont]
            thematch = [s for s in submatch if s]
            if len(thematch) != 1:
                "ERROR %r matches in Submission directories, expected 1" % len(td)
            theindex = submatch.index(thematch[0])
            os.system("open "+ dircont[theindex] + "/*" )
            
            comment_header = "Comments on " + hwname + " for " + student_dirs[dir_index]
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
            print '\n'
            print '\n'
            os.chdir('..')
            fout.writelines(grade)
            
        fout.writelines('\n')
    fout.flush()
    fout.close()
    f.close()

        
if __name__=='__main__':
    main()


