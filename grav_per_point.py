#!/usr/bin/python

# This script uses prism.py functions to compute gravity for
# a single point whose data is provided on the command line. 
# Input: See print_usage() for the input parameters and their order.
# Output: a single file that with one line containing the
# position ID, timestep and gravity measurement.
# Author: Yekaterina Kharitonova (ykk-at-email.arizona)

import sys
from prism import calc_prism, calc_macmillan, calc_pointmass
from math import sqrt, pow
from datetime import datetime
from datetime import date
import time

tstart = time.clock()

num_args = 6 # including the script name

def print_usage():
    print "Usage: python ", sys.argv[0], " <density_grid_file> ID X Y Z"
    sys.exit(1)

if (len(sys.argv) == 1):
    print_usage()
elif len(sys.argv) <> num_args:
    print "The script expects %d arguments. You provided %d." % (num_args, len(sys.argv))
    print_usage()

dx, dy, dz = (10., 10., .1)

gp = [0, 0, 0, 0]
grav_pos = []
density_grid = []
r2exac = 10.
r2macm = 81.

# read density grid
density_file = sys.argv[1] # currently "density_grid.txt"
fid = open(density_file,'r')
for line in fid:
    density_grid.append([float(x) for x in line.split()])
fid.close()

# read gravimeter positions
gp[0] = int(sys.argv[2]) # ID
gp[1] = float(sys.argv[3]) # x
gp[2] = float(sys.argv[4]) # y
gp[3] = float(sys.argv[5]) # z

output_file = str(gp[0]) +"_"+ density_file + ".time" #  "id_its_density_grid.txt.time"
print output_file
fid = open(output_file,'w')

g_sum = 0
g_out =  []
for prism in density_grid:
	time_step = prism[0]

	dxMid = prism[1]
	dyMid = prism[2]
	dzMid = prism[3]
	hfin  = prism[4]

	# Calculate the distance to the mass to determine which formula to use
	rad = sqrt((dxMid-gp[1])**2 + 
		   (dyMid-gp[2])**2 +
		   (dzMid-gp[3])**2)
	r2  = rad**2
	dr2 = dx**2 + dy**2 + dz**2
	f2  = r2 / dr2
	#f2 = 1 
	if f2 <= r2exac: 
		#print 'prism'
		g_prism = calc_prism(dx, dy, dz,
				 dxMid, dyMid, dzMid,
				 hfin,
				 gp[1],gp[2],gp[3])
	elif f2 >= r2macm:
		#print ' mac'
		g_prism = calc_pointmass( hfin, dzMid, gp[3], dx, dy, dz, rad)
	else:
		#print 'pm'
		g_prism = calc_macmillan( hfin, dxMid, dyMid, dzMid, 
					  gp[1], gp[2], gp[3],
					  dx, dy, dz, rad)
	g_sum += g_prism
# add final time step
g_out.append([gp[0], time_step, g_sum])
for line in g_out:
	sys.stdout.write('%i %i %3.3f\n'%(line[0],line[1],line[2]))

tend = time.clock()
taskTime = "%.5g" % (tend-tstart)
fid.write(taskTime)



fid.close()
