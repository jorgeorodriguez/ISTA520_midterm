#This script will take in one input that is dealing with a density grid file
#It will then go through the file and make sub files for each Timestep ID
#Each file will hold all the data that has that ID point
#
#Author: Nick Gizzi


gravPosFile= raw_input("Enter in the grav pos file to be sorted: ")
file=open(gravPosFile.strip(),'r')

firstLine=file.readline().strip()
ts=str(0)+firstLine[0]


new_file=open("density_grid_"+ts,'w')

new_file.write(firstLine+"\n")


for line in file:
    temp=line[0:line.find(" ")] #splitting the line into a list, its being seperated by white spaces.
    temp=int(temp)
    if line =="": #checks to see if there is a blank line in the file
        continue

    elif (temp ==ts):
        new_file.write(line)

    else:
        new_file.close()

        if temp<10:

            ts=str(0)+str(temp)#adds a 0 in front of any number less than 10
            new_file=open("density_grid_"+str(ts),'a')
            new_file.write(line)


        else:
            ts=str(temp)
            new_file=open("density_grid_"+str(ts),'a')
            new_file.write(line)
 

            
            


new_file.close()

file.close()
