#!/opt/local/bin/python

import os
import sys
import re
import string
from subprocess import call

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
            curstudent = matchdir(ID.group(), student_dirs)
            os.chdir(curstudent)

            dircont = os.listdir(os.getcwd())
            submissionsdir = matchdir('Submission', dircont)
            subs = os.listdir(submissionsdir)
            
            filestoopen  = [f for f in subs if f.find('.pdf') != -1 or f.find('.doc') != -1]
            for f in filestoopen:
                filepath = os.path.join(os.getcwd(), submissionsdir, f)
                if sys.platform.startswith('darwin'):
                    call(('open', filepath))
                elif os.name == 'nt':
                    os.startfile(filepath)
                elif os.name == 'posix':
                    call(('xdg-open', filepath))

            
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
                grade = raw_input("Did you change the grade? If so enter it X/5:\n")
                while float(grade) > 5.0:
                    grade = raw_input("Grade must be less than 5. What is the grade X/5?\n")
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


