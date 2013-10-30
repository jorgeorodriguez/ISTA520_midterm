#!/usr/bin/python

# This script arranges the gravity values for each ID per timestep,
# producing N lines by T columns, where N is the number of IDs and
# T is the number of timesteps.
# Input: See print_usage() for the input parameters and their order.
# Output: a single file that with the gravity measurement per 
# timestep.
# Author: Yekaterina Kharitonova (ykk-at-email.arizona)

import sys
import os

num_args = 1 # including the script name

def print_usage():
    print "Usage: python ", sys.argv[0]
    print "the script has a variable that specifies the names of the output files"
    print "which will be concatenated to obtain the final output file."
    sys.exit(1)
"""
if (len(sys.argv) == 1):
    print_usage()
el
"""
if len(sys.argv) <> num_args:
    print "The script expects %d arguments. You provided %d." % (num_args, len(sys.argv))
    print_usage()


start_timestep = 0
end_timestep = 55
start_id = 1
total_ids = 10000

# open the output file
#output_file = "density_grid"
output_file = "density_grid/density_grid"
final_file = "gravity.out"
output_fh = open( final_file, 'w')
print "Saving the final gravity file ", final_file

for id in range(start_id, total_ids+1):
        output_fh.write( "%d " % (id) )
        for ts in range(start_timestep, end_timestep):
                filename = "%s_%.2d_%d.out" % (output_file, ts, id)
                if os.path.isfile( filename ):
                        grav_fh = open( filename, 'r' )
                        for val in grav_fh:
                                val = val.strip()
                                #print "Saving the value (%s) from %s" % ( val, filename)
                                output_fh.write( val + ' ' )
                else:
                        output_fh.write( "_ ")
        output_fh.write( "\n")
