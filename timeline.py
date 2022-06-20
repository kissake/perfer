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

end="Command finish time (calculated)"

numberFields = (
        wall, 
        userCpu, 
        sysCpu, 
        mem, 
        cacheio, 
        diskio, 
        swapout, 
        blockin, 
        blockout, 
        vcsw, 
        icsw, 
        start 
    )



#####
##### SUBROUTINES / OUTPUT / FORMATTING
#####


def perferReader(inputFile):

    reader = csv.DictReader(inputFile)

    dataPoints = []

    for line in reader:
        for number in numberFields:
            # NOTE: Some of these are actually integers...
            line[number] = float(line[number]) 

        line[end] = line[start] + line[wall] # Calcuated, for convenience(?)

        dataPoints.append(line)

    return dataPoints

def readDeltas(inputFile, reportValues):

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


def topNmeasurements(data, variable, N=5):
    # sort by the 'variable' being tested, to report the highest N values in that
    # column.
    
    data.sort(key=lambda datapoint: datapoint[1][variable])

    return data[0:5]


if __name__ == "__main__":

    reportOn = (userCpu,sysCpu, mem, blockin, blockout,)

    deltas = readDeltas(sys.stdin, reportOn)
    deltas.sort(key=lambda cpudelta: cpudelta[0])

    runningTotal = {}
    for delta in deltas:
        time = delta[0]
        changes = delta[1]
        print("time: %f" % (time))
        for value in reportOn:
            runningTotal[value] = runningTotal.get(value,0.0) + changes[value]
            print("\ttotal: %f" % (runningTotal[value]))

    print(topNmeasurements(deltas, userCpu))
