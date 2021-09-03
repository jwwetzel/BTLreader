import csv
import matplotlib.pyplot as plt
import argparse
import os
from collections import defaultdict
plt.rc('font',size=14)

parser = argparse.ArgumentParser(description='add filename, event scan')
parser.add_argument('fileName', type=str, help='Required Filename')
parser.add_argument('--start', type=int, help='beginning time slice')
parser.add_argument('--end', type=int, help='ending time slice.  If not given will show all from start on')
parser.add_argument('--channel', help='plot single channel')

args = parser.parse_args()

delay = 0
sipmPowerLevels = []
asicPowerLevels = []
pressureLevels  = []
tempLevels      = defaultdict(list)
currentLevels   = defaultdict(list)

outputName = "Analyzed"

markers     = ['.',',','o','v','^','<','>','1','2','3','4','8','s','P','p','*','h','H','+','x','X','D','d','|','_']
redColor    = [1,   1,      1,      0.8,    0.9,    0,  0,      0,0,    0.5,    1.0,    0.3,    0.5,    1.0,    1.0,    1.0,    0.9,0.1,0.8,0.4,0,0,0,0,0]
greenColor  = [0,   0.5,    0.9,    1,      1,      1,  0.7,    0.5,    0.5,    0.5,    0.5,    0,0,    0,      0,      0.5,    0.3,0.6,0.2,1.0,0,0,0,0]
blueColor   = [0,   0,      0,      0,      0,      1,  1,      0.9,    0.7,    0.9,    0.9,    0.5,    0.5,    1.0,    1.0,    0.7,0.9,0.2,0.2,0,0,0,0,0]


if args.fileName.endswith(".txt"):
    outputName = args.fileName[:-4]+"Analyzed"
    if not os.path.isdir(outputName):
        os.mkdir(outputName)

with open(args.fileName) as dataFile:
    for line in dataFile:
        if line.startswith('Delay'):
            delay = line.split(":")[1].strip()
        elif line.startswith('SIPM'):
            sipmPowerLevels.append(float(line.split(",")[2].split(" ")[1]))
            asicPowerLevels.append(float(line.split(",")[4].split(" ")[1]))
        else:
            tempLine = line.split(",")[::3]
            channel = 0
            for ch in tempLine:
                if channel < 20:
                    temp = float(ch.split("E")[0])*10**int(ch.split("E")[1][0:3])
                    tempLevels["Channel "+str(channel)].append(temp)
                    channel += 1
                else:
                    temp = float(ch.split("E")[0])*10**int(ch.split("E")[1][0:3])*1000*30.3
                    currentLevels["Channel "+str(channel)].append(temp)
                    channel += 1
                        
#print("Delay",delay)
#print("sipmPowerLevels",sipmPowerLevels)
#print("asicPowerLevels",asicPowerLevels)
#print(tempLevels)


allChanFig  = plt.figure(constrained_layout=True)
allChanFig.set_figheight(7)
allChanFig.set_figwidth(8)

allChanGS   = allChanFig.add_gridspec(2,1)
allChanGS2  = allChanGS[1].subgridspec(2,1)

allChanAx1  = allChanFig.add_subplot(allChanGS[0])
allChanAx1.set_title('Channels 0-20 Temperature vs time')

currChanGS  = allChanFig.add_gridspec(nrows=2, ncols=1)
allChanAx2  = allChanFig.add_subplot(allChanGS2[0])

allChanAx3  = allChanFig.add_subplot(allChanGS2[1])

if args.end is None:
    args.end = len(tempLevels["Channel 0"])
    
if args.start is None:
    args.start = 0

if args.channel is not None:
    chan = args.channel
    x = [int(delay)*int(item) for item in range(len(tempLevels["Channel "+str(chan)]))]
    y = tempLevels["Channel "+str(chan)]
    allChanAx1.plot(x[args.start:args.end], y[args.start:args.end], marker=',', linestyle='dashdot', label="Channel "+str(chan),color=(redColor[int(chan)],greenColor[int(chan)],blueColor[int(chan)]))
    allChanAx1.set_title("BTL Temperature vs Time ("+delay+" Second Interval)")
    allChanAx1.set_ylabel("Temperature ˚C")
else:
    for chan in range(len(tempLevels)):
        x = [int(delay)*int(item) for item in range(len(tempLevels["Channel "+str(chan)]))]
        y = tempLevels["Channel "+str(chan)]
        allChanAx1.plot(x[args.start:args.end], y[args.start:args.end], marker=',', linestyle='dashdot', label="Channel "+str(chan),color=(redColor[int(chan)],greenColor[int(chan)],blueColor[int(chan)]))
        allChanAx1.set_title("BTL Temperature vs Time ("+delay+" Second Interval)")
        allChanAx1.set_ylabel("Temperature ˚C")
#        print(redColor[int(chan)],greenColor[int(chan)],blueColor[int(chan)])

allChanAx2.set_ylabel("Pressure (PSI)")
x = [int(delay)*int(item) for item in range(len(currentLevels["Channel 20"]))]
y = currentLevels["Channel 20"]
allChanAx2.plot(x[args.start:args.end], y[args.start:args.end],'.', linestyle='dashdot', label = "ADC 0")
y = currentLevels["Channel 21"]
allChanAx2.plot(x[args.start:args.end], y[args.start:args.end],'.', linestyle='dashdot', label = "ADC 1")

allChanAx3.set_xlabel("Time (Seconds)")
allChanAx3.set_ylabel("Power (W)")
y = sipmPowerLevels
allChanAx3.plot(x[args.start:args.end], y[args.start:args.end],'.', linestyle='dashdot', label = "SiPM W")
y = asicPowerLevels
allChanAx3.plot(x[args.start:args.end], y[args.start:args.end],'.', linestyle='dashdot', label = "ASIC W")

allChanFig.legend(bbox_to_anchor=(1.0, 0.95), loc='upper left')

if args.channel is not None:
    allChanFig.savefig(outputName+"/"+outputName+"_Channel_"+str(args.channel)+".png", bbox_inches="tight")
else:
    allChanFig.savefig(outputName+"/"+outputName+"_AllChannels.png", bbox_inches="tight")

#    allChanAx2.set_xlabel("Time (Seconds)")
#    allChanAx2.set_ylabel("Current (nA)")
#    x = [int(delay)*int(item) for item in range(len(currentLevels["Channel 20"]))]
#    y = currentLevels["Channel 20"]
#    allChanAx2.plot(x[args.start:args.end], y[args.start:args.end],'.', linestyle='dashdot', label = "ADC 0")
#    y = currentLevels["Channel 21"]
#    allChanAx2.plot(x[args.start:args.end], y[args.start:args.end],'.', linestyle='dashdot', label = "ADC 1")
#
#allChanFig.legend(bbox_to_anchor=(1.0, 0.95), loc='upper left')
#allChanFig.savefig(outputName+"/"+outputName+"Channel_"+chan+".png", bbox_inches="tight")

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



