#!/usr/bin/env python

# This script uses grav.py functions to compute gravity for
# a single point whose data is provided on the command line. 
# Input: See print_usage() for the input parameter.
# Output: a single file that with one line containing the
# position ID, timestep and gravity measurement.
# Author: Rachel Gladysz 

from work_queue import *
import sys
import time
from datetime import datetime

start_timestep = 1
#end_timestep = 55
end_timestep = 1
PORT_ID = 54601
queue_wait_time = 10 # how many seconds to wait for the results
grav_pos_file = "grav_pos.txt"
script_file = "grav_per_point.py"
helper_script_file = "prism.py"
density_grid = "_density_grid.txt"
timing_file = "timing_"

num_args = 1 # including the script name

def print_usage():
    print "Usage: python ", sys.argv[0] 
    sys.exit(1)

if (len(sys.argv) != 1):
    print_usage()
elif len(sys.argv) <> num_args:
    print "The script expects %d arguments. You provided %d." % (num_args, len(sys.argv))
    print_usage()


try:
	Q = WorkQueue(port=PORT_ID)
except:
	print "could not instantiate Work Queue master"
	sys.exit(1)

print "Listening on port %d." % Q.port
print datetime.now()

print "Processing %d timesteps (start at %d, end at %d)." % ((end_timestep+1 - start_timestep), start_timestep, end_timestep )
gp_list = []
gp = open(grav_pos_file, 'r')
print "Processing %s file to create tasks." % (grav_pos_file)
count = 0
for line in gp:
	gp_list.append(line.split())
	for i in range(start_timestep, end_timestep+1): # +1, because of the way Python runs its ranges
		#density_file = "%d_density_grid.txt" % (i)
		density_file = str(i) + density_grid
		id = str(gp_list[count][0])
		#outfile = id+"_%d_density_grid.txt.out" % (i)
		outfile = str(id) + "_" + density_file + ".out"
		#print outfile
		
		#command = "python grav_per_point.py " + density_file + " %s %s %s %s" % (gp_list[count][0], gp_list[count][1], gp_list[count][2], gp_list[count][3])
		command = "python grav_per_point.py " + density_file + " %s %s %s %s > %s" % (gp_list[count][0], gp_list[count][1], gp_list[count][2], gp_list[count][3], outfile)
		#print command
		T = Task(command)
		T.specify_file(script_file, script_file, WORK_QUEUE_INPUT, cache = True)
		T.specify_file(helper_script_file, helper_script_file, WORK_QUEUE_INPUT, cache = True)
		T.specify_file(density_file, density_file, WORK_QUEUE_INPUT, cache = True)
		T.specify_file(outfile, outfile, WORK_QUEUE_OUTPUT, cache = False)
		taskid = Q.submit(T)
	count += 1
gp.close()

print "Waiting for %d tasks to complete..." % (count)
print datetime.now()
tstart = time.clock()
while not Q.empty():
    T = Q.wait( queue_wait_time ) # wait specifies how long the queue waits for results from workers
    if T:
        print "Task #%d complete: %s (returned %d)" % (T.id, T.command, T.return_status)
        if T.return_status != 0:
            print "Task result (%s): %s" % (T.result, T.output)
        print "Transfer time = %d; execution time = %d" % (T.total_transfer_time, T.cmd_execution_time )
	# Save the timing information for each task
	timing_fh = open( timing_file + str(T.id), 'w')
	#timing_fh.write("%d\t%d\n" % (T.total_transfer_time, T.cmd_execution_time ))
	timing_fh.write("%d\n" % ( T.cmd_execution_time ))
	timing_fh.close()
tend = time.clock()
taskTime = "%.3f" % (tend-tstart)
#print "Finished processing %d tasks." % (count)
print datetime.now()
print "Finished processing %d tasks in %s seconds." % (count, taskTime)
#print "Finished processing %d tasks in %d seconds (%f minutes)." % (count, taskTime, (tend-tstart)/60.0)
#print "Finished processing %d tasks in %d seconds (%f minutes)." % (count, taskTime, float(float(taskTime)/60.0))
