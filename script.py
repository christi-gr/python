#!/usr/bin/python3

import sys
import getopt

from pathlib import Path
import pandas as pd
import re

def clean(text, search_list, replace_list):
    text = text.strip()
    for ind in range(0,len(search_list)):
        text = re.sub( search_list[ind], replace_list[ind], text, 0, re.U)
    return text

def matches( text, pattern_list):
    for item in  pattern_list:
        if  re.search( item, text ):
            return True

    return False

def get_pattern_replace(csv_path):
     data = pd.read_csv( csv_path, header=None)
     return [ data.iloc[:,0]. tolist(), data.iloc[:,1]. tolist() ]

def detection( start_path, fp_path ):

    part = Path( start_path )
    files = list( part.glob( '**/*.c' ) )
    fs_pattern = open( fp_path , mode="w", encoding="utf-8" )

    for f in files:
        fs_pattern.write( str( f ) + "\n" )
    fs_pattern.close()
    
def replacement( start_path, pf_path, fp_path ):

    detection( start_path, fp_path )
    search, replace = get_pattern_replace( pf_path )

    fs_pattern = open( fp_path, mode="r", encoding="utf-8" )

    for line in fs_pattern:
        line = line.strip()

        with open(line,'r') as file:
            filedata = file.read()

            #matching text pattern
            if  matches( filedata, search ) :
                filedata = clean(filedata, search, replace)

                with open(line,'w') as file_substitude:
                    file_substitude.write(filedata)
            
    fs_pattern.close()

def main(argv):
    arg_input = "./"
    arg_fs = "file_list.txt"
    arg_pattern = "pattern.csv"
    arg_help = "{0} -i <input> -p <pattern> -o <fs>".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "hi:p:o:", ["help", "input=",
        "pattern=", "fs="])
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-i", "--input"):
            arg_input = arg
        elif opt in ("-o", "--o"):
            arg_fs = arg
        elif opt in ("-p", "--pattern"):
            arg_pattern = arg

    replacement( arg_input , arg_pattern, arg_fs )

if __name__ == "__main__":
    main(sys.argv)
