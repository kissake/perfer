#!/usr/bin/python3

import pprint as pprint
import time as time
import csv as csv
import sys as sys
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection #Maybe not?
# Don't need NumPy



wall="Wall clock time, in seconds"
userCpu="CPU time in userspace, in seconds"
sysCpu="CPU time in system, in seconds"
mem="Max resident set size in kB"
cacheio="Page faults not req. i/o"
diskio="Page faults requiring i/o"
swapout="Number of swap outs"
blockin="Nuber of block input operations"
blockout="Number of block output operations"
vcsw="Voluntary context switches (wait(), select())"
icsw="Involuntary context switches (resource contention)"
start="Command start time, absolute, unix time"
cmd="Command (with arguments in following columns)"




#####
##### SUBROUTINES / OUTPUT / FORMATTING
#####


def readFile(inputFile, reportValues):

    deltas = []

    reader = csv.DictReader(inputFile)

    for line in reader:
        startTime = float(line[start])
        wallTime = float(line[wall])
        x1 = startTime
        x2 = startTime + wallTime

        # start
        a1 = {}
        # end
        a2 = {}

        for value in reportValues:
            
            temp = float(line[value])
            a1[value] = temp / wallTime
            a2[value] = -1 * a1[value]

        # This is the transition representing increase in CPU usage
        deltas.append((x1, a1))
        # This is the corresponding transition representing return to zero.
        deltas.append((x2, a2)) 

    return deltas


reportOn = (userCpu,sysCpu, mem, blockin, blockout,)

deltas = readFile(sys.stdin, reportOn)
deltas.sort(key=lambda cpudelta: cpudelta[0])

runningTotal = {}
for delta in deltas:
    time = delta[0]
    changes = delta[1]
    print("time: %f" % (time))
    for value in reportOn:
        runningTotal[value] = runningTotal.get(value,0.0) + changes[value]
        print("\ttotal: %f" % (runningTotal[value]))

exit(0)

if debugRequested is None:
    DEBUG=False
else:
    DEBUG=sys.stderr

if DEBUG:
    pprint.pprint(os.getcwd(), stream=DEBUG)
    pprint.pprint(os.environ, stream=DEBUG)
    pprint.pprint(sys.argv, stream=DEBUG)



#####
##### ARGUMENT PARSING
#####
#
# Argument parsing (we only accept one commandline argument, and only when it is alone and bare)

if len(sys.argv) < 2 or sys.argv[1] == '--help': 
    print('''
Example usage:

export PERFEROUTPUT=`mktemp`
export PERFERENVIRON="PATH:PERL5LIB"
export PERFERCWD=TRUE
export PERFERCMD=TRUE
perfer --header

perfer <command to be monitored>
''')
    exit(0)

#####
##### MAIN
#####

exit()
