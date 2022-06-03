#!/usr/bin/env python3  
#----------------------------------------------------------------------------
# Created By  : Pedro V Quijano Carde 
# Created Date: 06/01/2022
# Revision ='1.0' Add all modules currently used and make a simple script to
#                 use the rotary switch, pumps, and load cell.
# ---------------------------------------------------------------------------
""" This script stores a text file
    -storeEvent(timeStamp, fileName, data)
        -timestamp: includes the time in the file name, done outside with
                    strftime("%Y-%m-%d_%H:%M:%S")
        -filename: includes a string to the file name
        -data: this is what will be stored in the text file, can be integers,
        , floating numbers, strings. For multiple inputs include them inside
        a list [var1, str1]. Format with \t and \n to import as csv later.
"""
# ---------------------------------------------------------------------------

import os

# ---------------------------------------------------------------------------

def storeEvent(timeStamp, fileName, data):
    parentPath = os.path.dirname(__file__) #This is to get the current working directory, this way you can put the main script anywere you like (in this case the only requirement is to have a Data folder in the same directory as the script
    print(parentPath + '\n')
    
    file1 = open(r"" + parentPath + "/Data/" +  timeStamp + "__" + fileName + ".txt","a")
    file1.writelines(data)
    file1.close()