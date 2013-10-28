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
