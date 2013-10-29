#This script will take in one input that is dealing with a grav pos file
#It will then go through the file and make sub files for each Timestep ID
#Each file will hold all the data that has that ID point
#
#Author: Nick Gizzi


gravPosFile= raw_input("Enter in the grav pos file to be sorted: ")
file=open(gravPosFile.strip(),'r')

firstLine=file.readline().strip()

ts=0+firstLine[0]

lastLine=file.readlines()[-1].strip()

file.close()

new_file=open("density_grid_"+str(ts),'w')

new_file.write(firstLine)

file=open(gravPosFile.strip(),'r')

for line in file:
    if line =="":#checks to see if there is a blank line in the file
        continue
    elif (lastLine==line):
        new_file.write(line)
        new_file.close()
        break

    elif line[0]==ts:
        new_file.write(line)

    else:
        new_file.close()
        if line[0]<10:    #adds a 0 in front of any number less than 10
            ts=0+line[0]
        else:
            ts=line[0]
        new_file=open(str(ts)+"_density_grid",'w')#checks to see if there is a blank line in the file
        new_file.write(line)
 

            
            


new_file.close()

file.close()
