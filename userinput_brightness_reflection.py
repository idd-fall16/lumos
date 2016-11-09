#!/usr/bin/env python

from lifxlan import *; import sys; import time; import math

lifxlan = LifxLAN()

kelvin=2500;
kelvinRange = 9000-2500;
set2rise=False;
rise2set=False;

# Hardcoded sunrise and sunset times
sunSetTime=[18, 0, 0];
sunRiseTime=[6, 0, 0];

# Math to calculate midDayTime time
midDayInMinutes =(sunSetTime[0]*60+sunSetTime[1] + sunRiseTime[0]*60+sunSetTime[1])/2;
midDayTime=[math.floor(midDayInMinutes/60), midDayInMinutes%60, 0];

# Current Time
formattedLocalTime = time.asctime(time.localtime(time.time()))
print "Local current time :", formattedLocalTime

localTime = time.localtime(time.time())
print "Local current time :", localTime [3], localTime[4], localTime[5]
# hour = localTime [3]
# minute = localTime [4]
# second = localTime [5]
hour = int(sys.argv[1])
minute = 0;
second = 0;
print"Military Time: ",hour, ":00"


# Determine if Set2Rise or Rise2Set
if ((hour >= sunSetTime[0] and hour <= 24) or (hour >= 0 and hour <= sunRiseTime[0])):
    set2rise=True;
else:
    rise2set=True;

# Determining kelvinin Parameter
if set2rise == True:
    kelvin=2500;

elif rise2set==True:
    if (hour < midDayTime[0]): 
        numMinutes = (midDayInMinutes) - (sunRiseTime[0]*60+sunRiseTime[1]);
        kelvinStep = kelvinRange/numMinutes #kelvinins per minute
        kelvin = math.ceil(((hour*60+minute) - (sunRiseTime[0]*60+sunRiseTime[1]))*kelvinStep +2500);
    else:
        numMinutes = (midDayInMinutes) - (sunSetTime[0]*60+sunSetTime[1]);
        kelvinStep = kelvinRange/numMinutes #kelvinins per minute
        kelvin = math.ceil(((hour*60+minute) - (midDayTime[0]*60+midDayTime[1]))*kelvinStep + 9000);


else:
    kelvin=2500;

input=[0, 0, 30000, kelvin];
lifxlan.set_color_all_lights(input, rapid=True)

print "Kelvin: ", kelvin

