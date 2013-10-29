
# This script uses the grav_pos.txt file that will be used to slowly scale up to determine
# how long it takes to run N ammount of Ids.
# It will iterate through the list and grab i many IDs and
# will then create a file.
# Input: no additional input is required.  grav_pos.txt must be in same directory
# Output: A total of 16 files containing time for each ID
# 
# Author: Nick Gizzi



import os

list = [1,2,3,4,5,10,25,50,100,300,500,750,1000,1250,1500,2000,2500]
e = open(os.path.realpath("grav_pos.txt"))

file_list=e.read().splitlines()



position = 0


for i in range(len(list)):
    amount = list[i]
    
    new_file=open("grav_pos_"+str(list[i])+".txt",'w')


    for d in range(position, position + amount):
        new_file.write(str(file_list[d])+"\n")
        position = position + 1

    new_file.close()
