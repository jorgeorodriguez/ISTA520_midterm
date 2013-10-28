#This program will read in a file, then sift through it line by line
#It will then check to see what the min num and max num is in this file
#Along with adding all of the values being read in up into one large sum
#It will then use the counter variable to get the average number in the file

import os


fileIn= raw_input("Enter File:")

open_file=open(os.path.realpath(fileIn))

float minValue
float maxValue
float total
int average

#used to keep track of how many total lines there are in the file
int counter

for line in open_file:
    counter+=1
    
    if line > maxValue:
        maxValue = line
    if line < minValue:
        minValue=line

    total= total + line


average=total/counter




open_file.close()
               
