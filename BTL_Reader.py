import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
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

outputName = "Analyzed"

if args.fileName.endswith(".txt"):
    outputName = args.fileName[:-4]+"Analyzed"
    if not os.path.isdir(outputName):
        os.mkdir(outputName)

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
                    currentLevels["Channel "+str(channel)].append(temp)
                    channel += 1
                        
#print("Delay",delay)
#print("sipmPowerLevels",sipmPowerLevels)
#print("asicPowerLevels",asicPowerLevels)
#print(tempLevels)


allChanFig  = plt.figure(constrained_layout=True)
allChanFig.set_figheight(7)
allChanFig.set_figwidth(8)

allChanGS   = allChanFig.add_gridspec(4,1)

allChanAx1  = allChanFig.add_subplot(allChanGS[0:3,:])
allChanAx1.set_title('Channels 0-20 Temperature vs time')

allChanAx2  = allChanFig.add_subplot(allChanGS[3:,:])

for chan in range(len(tempLevels)):
    x = [int(delay)*int(item) for item in range(len(tempLevels["Channel "+str(chan)]))]
    y = tempLevels["Channel "+str(chan)]
    allChanAx1.plot(x, y, '.', linestyle='dashdot', label="Channel "+str(chan))
    allChanAx1.set_title("BTL Temperature vs Time")
    allChanAx1.set_ylabel("Temperature ˚C")

allChanAx2.set_xlabel("Time (Seconds)")
allChanAx2.set_ylabel("Current (nA)")
x = [int(delay)*int(item) for item in range(len(currentLevels["Channel 20"]))]
y = currentLevels["Channel 20"]
allChanAx2.plot(x,y,'.', linestyle='dashdot', label = "ADC 0")
y = currentLevels["Channel 21"]
allChanAx2.plot(x,y,'.', linestyle='dashdot', label = "ADC 1")

allChanFig.legend(bbox_to_anchor=(1.0, 0.95), loc='upper left')
allChanFig.savefig(outputName+"/"+outputName+"_All_Channels.png", bbox_inches="tight")



#allChanFig, allChanAxes = plt.subplots(2,sharex=True)

#singleChanFig, singleChanAxes = plt.subplots()

#for chan in range(len(tempLevels)):
#    x = [int(delay)*int(item) for item in range(len(tempLevels["Channel "+str(chan)]))]
#    y = tempLevels["Channel "+str(chan)]
#    allChanAxes[0].plot(x, y, '.', linestyle='dashdot', label="Channel "+str(chan))
#    allChanAxes[0].set_title("BTL Temperature vs Time")
#    allChanAxes[1].set_xlabel("Time (Seconds)")
#    allChanAxes[0].set_ylabel("Temperature ˚C")
#    allChanFig.savefig(outputName+"/"+outputName+"_ch"+str(chan)+".png", bbox_inches="tight")
#if args.channel is not None:
#    print("not none")
#    x = [int(delay)*int(item) for item in range(len(tempLevels["Channel "+str(args.channel)]))]
#    y = tempLevels["Channel "+str(args.channel)]
#    singleChanAxes.title("BTL Temperature vs Time Channel "+str(args.channel))
#    singleChanAxes.xlabel("Time (Seconds)")
#    singleChanAxes.ylabel("Temperature ˚C")
#    singleChanAxes.plot(x, y, '.', linestyle='dashdot', label="Channel "+str(args.channel))
#    singleChanFig.savefig(outputName+"/"+outputName+"_SINGLE_ch"+str(chan)+".png", bbox_inches="tight")
#plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
#plt.tight_layout()
#plt.show()




#print(args.fileName)

#data = pd.read_csv(args.fileName)

#print(data)

#22 channels

#20 channels temperature
#2 channels of current
#Need power levels and inlet/outlet pressure in mA, /1000, last 2 numbers. separate graph



