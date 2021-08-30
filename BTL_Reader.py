import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
from collections import defaultdict
plt.rc('font',size=14)

parser = argparse.ArgumentParser(description='add filename, event scan')
parser.add_argument('fileName', type=str, help='Required Filename')
parser.add_argument('--start', help='beginning time slice')
parser.add_argument('--end', help='ending time slice.  If not given will show all from start on')
parser.add_argument('--channel', help='plot single channel')

args = parser.parse_args()

delay = 0
sipmPowerLevels = []
asicPowerLevels = []
pressureLevels  = []
tempLevels      = defaultdict(list)
currentLevels   = defaultdict(list)

with open(args.fileName) as dataFile:
    for line in dataFile:
        if line.startswith('Delay'):
            delay = line.split(":")[1].strip()
        elif line.startswith('SIPM'):
            sipmPowerLevels.append(line.split(",")[2].split(" ")[1])
            asicPowerLevels.append(line.split(",")[4].split(" ")[1])
        else:
            tempLine = line.split(",")[::3]
            channel = 0
            for ch in tempLine:
                if channel < 20:
                    temp = float(ch.split("E")[0])*10**int(ch.split("E")[1][0:3])
                    tempLevels["Channel "+str(channel)].append(temp)
                    channel += 1
                else:
                    temp = float(ch.split("E")[0])*10**int(ch.split("E")[1][0:3])*1000000000
                    print(temp)
                    currentLevels["Channel "+str(channel)].append(temp)
                        
#print("Delay",delay)
#print("sipmPowerLevels",sipmPowerLevels)
#print("asicPowerLevels",asicPowerLevels)
#print(tempLevels)

#
if args.channel is None:
    for chan in range(len(tempLevels)):
        x = [int(delay)*int(item) for item in range(len(tempLevels["Channel "+str(chan)]))]
        y = tempLevels["Channel "+str(chan)]
        plt.title("BTL Temperature vs Time")
        plt.xlabel("Time (Seconds)")
        plt.ylabel("Temperature ˚C")
        plt.plot(x, y, '.', linestyle='dashdot', label="Channel "+str(chan))
else:
    x = [int(delay)*int(item) for item in range(len(tempLevels["Channel "+str(args.channel)]))]
    y = tempLevels["Channel "+str(args.channel)]
    plt.title("BTL Temperature vs Time Channel "+str(args.channel))
    plt.xlabel("Time (Seconds)")
    plt.ylabel("Temperature ˚C")
    plt.plot(x, y, '.', linestyle='dashdot', label="Channel "+str(args.channel))
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(args.fileName+"_analyzed.png", bbox_inches="tight")
plt.show()




#print(args.fileName)

#data = pd.read_csv(args.fileName)

#print(data)

#22 channels

#20 channels temperature
#2 channels of current
#Need power levels and inlet/outlet pressure in mA, /1000, last 2 numbers. separate graph



