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

def plotVariable(plot, dataset, variable):
    plot.plot(
            [ x[0] for x in dataset ],
            [ x[1][variable] for x in dataset ]
            )


reportOn = (userCpu,sysCpu, mem, blockin, blockout,)

deltas = readFile(sys.stdin, reportOn)
deltas.sort(key=lambda measurement: measurement[0])

startTime = deltas[0][0]
runningTotal = []
measurement = {}
for value in reportOn:
    measurement[value] = 0.0

for delta in deltas:
    newMeasurement = {}
    time = delta[0]
    changes = delta[1]

    # For a pretty graph, we really need to have the previous value
    # reported at t - epsilon, and the new value reported at t.
    runningTotal.append((time - startTime - sys.float_info.epsilon, measurement.copy()))
    
    for value in reportOn:
        measurement[value] = measurement.get(value,0.0) + changes[value]
    
    runningTotal.append((time - startTime, measurement.copy()))


# Test for consistency; every addition should have a corresponding equal subtraction.
# There could be floating point errors that lead to minor errors; this is okay.
for key, value in runningTotal[-1][1].items():
    if value != 0.0:
        print("%s is %f instead of 0.0 as expected." % (key, value))

for report in reportOn:
    plotVariable(plt, runningTotal, report)
plt.show()
