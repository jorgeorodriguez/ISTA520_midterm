list = [1,2,3,4,5]
e = [10,20,30,40,50,60,70,80,90,100,110,120,130,140,150]

start = 0


for i in range(len(list)):
    amount = list[i]
    print "[%d] = %d" % (i, amount)
    print "---"

    for d in range(start, start + amount):
        list_amount = e[d]
        print "[%d] = %d" % (d, list_amount)
        start = start + 1
    print "---"
    print "Start position " + str(start)
    print "---"
