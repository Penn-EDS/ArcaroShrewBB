#!/usr/bin/env python3  
#----------------------------------------------------------------------------
# Created By  : Pedro V Quijano Carde 
# Created Date: 06/01/2022
# Revision ='1.0' 
# ---------------------------------------------------------------------------
""" This is a wrapper funtion for the weightLib function. It zeros the weight
    cell at the first call of the function, or when passing True as an argument.
    Make sure there is nothing on the platform when first calling the function.
    Returns weight in grams and the most frequent maximum weight between 100
    and 400 grams.
    
    -platformWeight() returns a weight in grams. If the swab file is not created
    the user is prompted to do so by calibrating the load cell.
    
    1. Before running the script make sure nothing is on the weight platform
    2. When asked put a known weight, wait for 3-5 seconds and press enter.
    3. When asked input the weight in grams and press enter
    4. The load cell is ready to use
"""
# ---------------------------------------------------------------------------

from weightLib import *

# ---------------------------------------------------------------------------

zero = int() #Global variable for zero
bucket = []  #Global variable for bucket
maxBucket = int()  #Global variable for maxBucket
firstPassWeightCell = True
    
def platformWeight(zeroing = False):
    global zero  #calling global variables
    global bucket 
    global maxBucket 
    global firstPassWeightCell
    
    #maxOut = int()
    maxr = int()  #variable to return current max number
    numOut = int()  #variable to store weight measured
    bucketPass = int() #Variable to pass numOut - lowerlim
    lowerlim = 100  #Weight Lower Limit that will be considered for Maxbucket
    upperlim = 400  #Weight Upper Limit that will be considered for Maxbucket
    
    limrange = upperlim - lowerlim
    
    if firstPassWeightCell or zeroing: #Only run this part of the code on the first pass
        firstPassWeightCell = False
        
        zero = int() # Cancels initial drift if there is any
        zero = int(weight())
        
        for i in range(limrange + 2):  #Initialize all index positions with 0
            bucket.append(0)
        
        bucket.pop(limrange + 1)    #placeholder for when no max num has been picked
        bucket.insert(limrange + 1, 1)
    
    numOut = int(weight()) - zero
    
    if (numOut > 0):  #Make sure the weight is positive
        print('Weight: ', numOut)
    else:
        print('Weight: ', 0)   # Sometimes it rounds up to -1
        numOut = 0
        
    if (numOut >= lowerlim and numOut <= upperlim): #Only consider weight inside the limrange
        bucketPass = bucket[numOut - lowerlim]  #Take the tally of the weight (index)
        bucket.pop(numOut - lowerlim)  #Add one to the tally
        bucket.insert(numOut - lowerlim, bucketPass + 1)  #Add one to the tally
            
    maxBucket = max(bucket)  #Returns the largest tally
    maxBucketIndex = [index for index in range(len(bucket)) if bucket[index] == maxBucket] #Searches for all instances of maxbucket in bucket, and returns the one in the highest index
        
    if (maxBucketIndex[-1] == limrange + 1): #for when no maximum number has been selected
        print('Max: ', 0)
    else:
        maxr = maxBucketIndex[-1] + lowerlim 
        print('Max: ', maxr)
        
        
            
        
            
        