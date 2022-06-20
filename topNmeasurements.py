#!/usr/bin/python3

import pprint as pprint
import time as time
import csv as csv
import sys as sys



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


def topNaggregateMeasurements(data, variable, aggregateOn=cmd, N=5):
    # After aggregating based on the specified variable, then:
    # sort by the 'variable' being tested, to report the highest N values in that
    # column.
    
    aggregate = {}

    for datapoint in data:
        agg = datapoint[aggregateOn]
        # Add the value for this datapoint to previous sum, starting at 0.0.
        aggregate[agg] = datapoint.get(variable) + aggregate.get(agg, 0.0)

    output = list(aggregate.items())
    output.sort(key=lambda datapoint: datapoint[1])

    return output[(-1*(N)):]


def topNmeasurements(data, variable, N=5):
    # sort by the 'variable' being tested, to report the highest N values in that
    # column.
    
    data.sort(key=lambda datapoint: datapoint[variable])

    return data[(-1*N):]


if __name__ == "__main__":

    reportOn = (userCpu,sysCpu, mem, blockin, blockout,)

    data = perferReader(sys.stdin)

    print("Individual processes using the most CPU")
    measures = topNmeasurements(data, userCpu)
    for measure in measures:
        print("%f:\t%s" % (measure[userCpu], measure[cmd]))
    print()
    print("Programs using the most total CPU")
    agg = topNaggregateMeasurements(data, userCpu, N=5)
    for topAgg in agg:
        print("%f:\t%s" % (topAgg[1], topAgg[0]))

