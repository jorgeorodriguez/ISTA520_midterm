#This script will take in one input that is dealing with the grav pos
#It will then go through the file and make sub files of each ID
#Each file will hold all the data relevent to that ID point
#
#

gravPosFile= raw_input("Enter in the grav pos file to be sorted: ")
file=open(gravPosFile.strip(),'r')

firstLine=file.readline().strip()

ts=firstLine[0]

lastLine=file.readlines()[-1].strip()

file.close()

new_file=open(str(ts)+"_density_grid",'w')

new_file.write(firstLine)

file=open(gravPosFile.strip(),'r')

for line in file:
    print line
    if line =="":
        continue
    elif (lastLine==line):
        new_file.write(line)
        new_file.close()
        break

    elif line[0]==ts:
        new_file.write(line)

    else:
        new_file.close()
        ts=line[0]
        new_file=open(str(ts)+"_density_grid",'w')
        new_file.write(line)
 

            
            


new_file.close()

file.close()
