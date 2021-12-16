#!/bin/env/python3
import sys
import os
import argparse

#location = '.'
#suffix = '.py'
def get_filelist(location, suffix = None, recursive = False):
    """ Get a list of files in a directory and optionally its subdirs,
         with optional suffix matching requirement."""
    if recursive == False:
        if suffix is None: 
            filelist = [location+x for x in os.listdir(location)]
        else:
            filelist = [location+x for x in os.listdir(location) if x[-len(suffix):] == suffix]

    elif recursive == True:
        filelist = []
        for path, subdirs, files in os.walk(location):
            for x in files:
                if suffix is None or x[-len(suffix):] == suffix:
                    rpath = os.path.join(path, x)
                    filelist.append(rpath)

    return filelist

def list_to_file(string_list, filename):
    """write a list of strings to a file, each string on separate line."""
    f=open(filename, 'w')
    for line in string_list:
        f.write(line)
        f.write('\n')
    f.close()


if __name__ == '__main__':
    """ 
    example usage:
    find all the bam files in a directory and write their absloute paths to a file.
    """
    realigned_filelist = get_filelist('/scratch/nugentc/data/cunner-bulk-process/', 
                                        suffix = ".realigned.bam", 
                                        recursive = True)

    outfile = "bam_file_list.txt"
    list_to_file(realigned_filelist, outfile)