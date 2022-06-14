#!/usr/bin/env python3  
#----------------------------------------------------------------------------
# Created By  : Pedro V Quijano Carde 
# Created Date: 06/01/2022
# Revision = '1.1' Checks for the data directory and creates it if there is none 
# Revision ='1.0'
# ---------------------------------------------------------------------------
""" This script stores a text file
    -storeEvent(timeStamp, fileName, data)
        -timestamp: includes the time in the file name, done outside with
                    strftime("%Y-%m-%d_%H:%M:%S")
                    
        -filename: includes a string to the file name
        
        -data: this is what will be stored in the text file, can be integers,
               floating numbers, strings. For multiple inputs include them inside
               a list [var1, str1]. Format with \t and \n to import as delimited csv.
"""
# ---------------------------------------------------------------------------

import os

# ---------------------------------------------------------------------------

parentPath = os.path.dirname(__file__) #Get current working directory,
                                       #this way you can put the main script anywere you like
                                       #(in this case the only requirement is to have a Data
                                       #folder in the same directory as the script

try:
    os.mkdir(parentPath + '/Data/') #Attempt to make the directory Data
    
except OSError as error:
    pass #Do nothing if the directory is already there

def storeEvent(time_Stamp, file_Name, data):
    
    file1 = open(r"" + parentPath + '/Data/' +  time_Stamp + '__' + file_Name + '.txt',"a")
    file1.writelines(data)
    file1.close()