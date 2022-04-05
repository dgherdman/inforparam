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
#   version 1.0  01/04/22   Dave Herdman
#
#   Revision History
#   V1.0    01/01/22    Initial Release Process only file totals
# 
#   Developed using the Pycharm IDE
#   See PyCharm help at https://www.jetbrains.com/help/pycharm/
#
#   Usage: inforparam.py <csv-substitution-file> <File-containing-list-of-files>
#
import sys
import os
import re
import csv


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # process the command line arguments (if any)
    if len(sys.argv) > 2:
        # Assume first argument is the path to the filename
        # Second argument is the output file path
        # silently ignore any other arguments
        csv_file_name = sys.argv[1]
        filelist_name = sys.argv[2]
    else:
        print("Usage: inforparam.py <csv-substitution-file> <File-containing-list-of-files>")
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
    #

    with open(filelist_name) as nxt_file:
        for par_file in nxt_file:
            try:
                pfl = open(par_file.rstrip(os.linesep),"r")
            except:
                print("Error opening file %s" % (par_file))
                sys.exit
            for line in pfl:
                # Parse each line in the parameter file
                for key in par_sub:
                    match_pos = line.find(key)
                    if match_pos >= 0:
                        # We have a match so do the substitution
                        rhs`` = line.rfind(r'=') + 1:]
                        print("got a match, file is %s" % (par_file))
                        print("line is %s" % (line.rstrip(os.linesep)))
                        print("line will be %s")
                    else:
                        # We don't have a match
                        pass
            pfl.close()
#        csv_file = open(csv_file_name,"r")
#        csv_reader = csv.reader(csv_file, delimiter=',')
#    for row in csv_reader:
#        #
#
#        part1 = row[0][0:row[0].find(r'=') +1]
#        print("%s will become %s" % (row[0], part1 + par_sub[old_par_value]))





