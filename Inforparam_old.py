#!/usr/bin/python
#
#  The 1st line tells UNIX like OS variants where to find the correct Python 
#  interpreter. This is ignored by Operating systems such as Windows
#
#  inforparam.py
#
#  A python script to substitute parameter strings in Informatica Parameter files
#
#  Read in a csv file containing 2 columns. The first column is the "Old" parameter
#  string and the second column contains the substitution for that parameter value.
#  The second parameter value is a file containing a list of parameter files to
#  process. Note the files should contain absolute paths
#
#
#   version 1.1  07/04/22   Dave Herdman
#
#   Revision History
#   V1.0    01/04/22    Initial Release Process only file totals
#   V1.1    07/04/22    Improve processing, add parameter to direct output files
# 
#   Developed using the Pycharm IDE
#   See PyCharm help at https://www.jetbrains.com/help/pycharm/
#
#   Usage: inforparam.py <csv-substitution-file> <File-containing-list-of-files> <output-directory>
#
import sys
import os
import os.path
import re
import csv


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # process the command line arguments (if any)
    if len(sys.argv) > 3:
        # Assume first argument is the path to the filename
        # Second argument is the output file path
        # Third argument is file output directory
        # silently ignore any other arguments
        csv_file_name = sys.argv[1]
        filelist_name = sys.argv[2]
        out_dir_name = sys.argv[3]
    else:
        print("Usage: inforparam.py <csv-substitution-file> <File-containing-list-of-files> <output-directory>")
        sys.exit("Incorrect number of arguments")


    #
    # Process the CSV file first
    #
    par_sub = dict()

    #with open("Sample_Mapped_ParamValues.csv") as csv_file:
    with open(csv_file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_count = 0
        for row in csv_reader:
            # Scan backwards to find an "=" character in the first value
            # old_par_value = row[0][row[0].rfind(r'=') + 1:]
            if row_count != 0:
                old_par_expr = row[0]
                par_sub[old_par_expr] = row[1]
                row_count += 1
            else:
                # First line of CSV file contains headers
                row_count += 1

    #
    # Process the parameter substitutions
    # We go through the contents of the file list file opening
    # each file in turn and scanning it to see if we need to
    # make any substitutions. Initially we write the output to
    # a list in case there are actually no changes to the file
    # required. If there are then we write the list to a new
    # file at the end of the loop to process a particular file
    #

    with open(filelist_name) as nxt_file:
        for par_file in nxt_file:
            par_file = par_file.rstrip(os.linesep)
            out_par_fiddle_open = False
            try:
                pfl = open(par_file,'r')
            except:
                print("Error opening file %s" % (par_file))
                sys.exit
            for line in pfl:
                # Parse each line in the parameter file
                for key in par_sub:
                    match_pos = line.find(key)
                    if match_pos >= 0:
                        # We have a match so do the substitution
                        equal_pos = line.rfind(r'=')
                        rhs = line[equal_pos + 1:]
                        lhs = line[:equal_pos +1]

                        # Formulate the new line
                        new_line = lhs + par_sub[key]

                        # if the output file is not open then do so
                        # otherwise just write to it
                        if out_par_file_open:
                                # If the file is already open the we have written one line to it
                                # We must now write a new line character before each subsequent
                                # line written to the file
                                npfl.write('\n')
                                npfl.write(new_line)
                        else:
                            new_file_name = "new_" + par_file
                            out_par_file_name = os.path.join(out_dir_name,new_file_name)
                            print("output file name is %s" % (out_par_file_name))
                            try:
                                npfl = open(out_par_file_name,"w")
                                out_par_file_open = True
                            except:
                                print("Can't open new parameter file %s for output" % (out_par_file_name))
                                sys.exit
                            npfl.write(new_line)
                        print("got a match, file is %s" % (par_file))
                        print("line is %s" % (line.rstrip(os.linesep)))
                        print("rhs is %s" % (rhs))
                        print("lhs is %s" % (lhs))
                        print("line will be %s" % (new_line))
                    else:
                        # We don't have a match in this line of the input file
                        pass
            pfl.close()
            npfl.close()





