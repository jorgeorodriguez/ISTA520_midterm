#!/usr/bin/env python

# This script uses grav.py functions to compute gravity for
# a single point whose data is provided on the command line. 
# Input: See print_usage() for the input parameter.
# Output: a single file that with one line containing the
# position ID, timestep and gravity measurement.
# Author: ykk 

from work_queue import *
import sys
import time
from datetime import datetime

start_timestep = 0
#end_timestep = 55
end_timestep = 1
queue_wait_time = 10 # how many seconds to wait for the results
#grav_pos_file = "grav_pos.txt"
split_amount = 1
script_file = "grav_per_point.py"
helper_script_file = "prism.py"
#density_grid = "density_grid_"
density_grid = "density_grid/density_grid_"
timing_file = "timing_"

num_args = 4 # including the script name

def print_usage():
    print "Usage: python ", sys.argv[0], "<grav_pos split> <start T> <end T>"
    print "Where the number of splits is concatenated to the grav_pos file (e.g. grav_pos_00.txt)."
    sys.exit(1)

if (len(sys.argv) == 1):
    print_usage()
elif len(sys.argv) <> num_args:
    print "The script expects %d arguments. You provided %d." % (num_args, len(sys.argv))
    print_usage()

start_timestep = int(sys.argv[2])
end_timestep = int(sys.argv[3])
split_amount = (sys.argv[1])
#PORT_ID = 54601
PORT_ID = "555" + split_amount #"5%.4d" % (split_amount)
PORT_ID = int(PORT_ID)
#grav_pos_file = "grav_pos/grav_pos_%d.txt"%(split_amount)
grav_pos_file = "grav_pos/grav_pos_" + split_amount
"""
print "Processing %s file to create tasks." % (grav_pos_file)
print "Port %d" % (PORT_ID)
sys.exit(1)
"""
try:
    gp = open(grav_pos_file, 'r')
    print "Processing %s file to create tasks." % (grav_pos_file)
except:
    print "Unable to open %s file to create tasks." % (grav_pos_file)
    sys.exit(1)


try:
    Q = WorkQueue(port=PORT_ID)
except:
    print "could not instantiate Work Queue master"
    sys.exit(1)

print "Listening on port %d." % Q.port
print datetime.now()

print "Processing %d timesteps (start at %d, end at %d)." % ((end_timestep - start_timestep), start_timestep, end_timestep )
wallclock = time.time()
gp_list = []
count = 0
for line in gp:
    gp_list.append(line.split())
    #for i in range(start_timestep, end_timestep+1): # +1, because of the way Python runs its ranges
    for i in range(start_timestep, end_timestep):
        #density_file = "%d_density_grid.txt" % (i)
        #density_file = str(i) + density_grid
        density_file = "%s%.2d" % (density_grid, i)
        if not os.path.isfile(density_file):
                print "WARNING! "+density_file+ " doesn't exist!"
                print "I will be unable to process the tasks without this file."
                sys.exit(1)
        id = str(gp_list[count][0])
        #outfile = id+"_%d_density_grid.txt.out" % (i)
        #outfile = str(id) + "_" + density_file + ".out"
        outfile = density_file + "_" + str(id)  + ".out"
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
            print "Resubmitting the task to the workqueue!"
            taskid = Q.submit(T)
        else:
            print "execution time = %d" % (T.cmd_execution_time )
        """
        # Save the timing information for each task
        timing_fh = open( timing_file + str(T.id), 'w')
        #timing_fh.write("%d\t%d\n" % (T.total_transfer_time, T.cmd_execution_time ))
        timing_fh.write("%d\n" % ( T.cmd_execution_time ))
        timing_fh.close()
        """
tend = time.clock()
taskTime = "%.3f" % (tend-tstart)
#print "Finished processing %d tasks." % (count)
print datetime.now()
wq_time = time.time() - wallclock
print "Finished processing %s and %s files to create %s output." % (grav_pos_file, density_file, outfile)
print "Finished processing %d timesteps (start at %d, end at %d)." % ((end_timestep - start_timestep), start_timestep, end_timestep )
print "Finished processing %d tasks in %s seconds (wallclock %s))." % (count, taskTime, wq_time)
timing_fh = open( "wallclock_" + str(split_amount), 'w')
timing_fh.write("%.3f\n" % (wq_time ))
timing_fh.close()

