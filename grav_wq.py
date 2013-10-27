#!/usr/bin/env python

# This script uses grav.py functions to compute gravity for
# a single point whose data is provided on the command line. 
# Input: See print_usage() for the input parameter.
# Output: a single file that with one line containing the
# position ID, timestep and gravity measurement.
# Author: Rachel Gladysz 

from work_queue import *
import sys

start_timestep = 1
#end_timestep = 55
end_timestep = 1

PORT_ID = 54601

queue_wait_time = 10 # how many seconds to wait for the results

num_args = 1 # including the script name

def print_usage():
    print "Usage: python ", sys.argv[0] 
    #print "sys.argv[0] : Indicate the script file name"
    sys.exit(1)

if (len(sys.argv) != 1):
    print_usage()
elif len(sys.argv) <> num_args:
    print "The script expects %d arguments. You provided %d." % (num_args, len(sys.argv))
    print_usage()


grav_pos_file = "grav_pos.txt"
script_file = "grav_per_point.py"

try:
	Q = WorkQueue(port=PORT_ID)
except:
	print "could not instantiate Work Queue master"
	sys.exit(1)

print "Listening on port %d." % Q.port


gp_list = []
gp = open(grav_pos_file, 'r')

count = 0
for line in gp:
	gp_list.append(line.split())
	for i in range(start_timestep, end_timestep+1): # +1, because of the way Python runs its ranges
		density_file = "%d_density_grid.txt" % (i)
		id = str(gp_list[count][0])
		outfile = id+"_%d_density_grid.txt.out" % (i)
		print outfile
		
		#command = "python grav_per_point.py " + density_file + " %s %s %s %s" % (gp_list[count][0], gp_list[count][1], gp_list[count][2], gp_list[count][3])
		command = "python grav_per_point.py " + density_file + " %s %s %s %s > %s" % (gp_list[count][0], gp_list[count][1], gp_list[count][2], gp_list[count][3], outfile)
		print command
		T = Task(command)
		T.specify_file(script_file, script_file, WORK_QUEUE_INPUT, cache = True)
		T.specify_file("prism.py", "prism.py", WORK_QUEUE_INPUT, cache = True)
		T.specify_file(grav_pos_file, grav_pos_file, WORK_QUEUE_INPUT, cache = True)
		T.specify_file(density_file, density_file, WORK_QUEUE_INPUT, cache = True)
		T.specify_file(outfile, outfile, WORK_QUEUE_OUTPUT, cache = False)
		taskid = Q.submit(T)
	count += 1
gp.close()
print "Done."

 
print "Waiting for tasks to complete..."
while not Q.empty():
    T = Q.wait( queue_wait_time ) # wait specifies how long the queue waits for results from workers
    """
    if T is None:
	print "Queue timed out after %d seconds!" % (queue_wait_time)
    """
    if T:
        print "Task (id# %d) complete: %s (return code %d)" % (T.id, T.command, T.return_status)
	print "Task result (%s): %s" % (T.result, T.output)
print "done."
