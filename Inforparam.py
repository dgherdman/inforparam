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
#   version 1.2  11/04/22   Dave Herdman
#
#   Revision History
#   V1.0    01/04/22    Initial Release Process only file totals
#   V1.1    07/04/22    Improve processing, add parameter to direct output files
#   V1.2    11/04/22    Fixed some bugs and only write new Parameter file if we
#                       actually changed anything in it.
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
            #
            # Open each input parameter file in turn
            # for processing.
            #
            par_file = par_file.rstrip(os.linesep)
            try:
                pfl = open(par_file,'r')
            except:
                print("Error opening file %s" % (par_file))
                sys.exit

            out_line = []

            pf_updated = False

            for line in pfl:
                # Parse each line in this parameter file
                # Check for all the key matches in any line
                key_match = False
                for key in par_sub:
                    match_pos = line.find(key)
                    if match_pos >= 0:
                        # We have a match so do the substitution
                        equal_pos = line.rfind(r'=')
                        rhs = line[equal_pos + 1:]
                        lhs = line[:equal_pos +1]

                        # Formulate the new line
                        out_line.append (lhs + par_sub[key])

                        # There can only be one match in a line
                        # so we break out of this loop
                        pf_updated = True
                        key_match = True
                        break

                # If there were no matches we keep the original line
                if key_match is False:
                    out_line.append(line)
            #
            # When we get here we have processed all the lines the
            # the input parameter file. We now need to write the
            # output parameter file
            #
            pfl.close()

            #
            # If we performed any updates then write the new file
            # otherwise process the next file
            #
            if pf_updated is True:
                new_file_name = "new_" + par_file
                out_par_file_name = os.path.join(out_dir_name, new_file_name)
                print("Output file name is %s" % (out_par_file_name))
                try:
                    npfl = open(out_par_file_name, "w")
                    out_par_file_open = True
                except:
                    print("Can't open new parameter file %s for output" % (out_par_file_name))
                    sys.exit

                for nline in out_line:
                    npfl.write(nline)

                npfl.close()
            else:
                print("File %s had no changes" % (par_file))

        # Next input Parameter File

    # Finished processing input file list


