#!/usr/bin/env python

from lifxlan import*; from time import sleep; import sys, time, math, pyowm, datetime, serial, string, os, io;
# import RPi.GPIO as GPIO;

#######################################################################################
# WEATHER API STUFF
owm = pyowm.OWM('ddafbf402476a208be381344dacee8ca')  # You MUST provide a valid API key

# You have a pro subscription? Use:
# owm = pyowm.OWM(API_key='your-API-key', subscription_type='pro')

# Search for current weather in SF()
observation = owm.weather_at_place('Sanfrancisco,us')
w = observation.get_weather()

# Weather details
sunrise=w.get_sunrise_time()
sunset=w.get_sunset_time()
cloudCover=w.get_clouds() # Cloud Cover as a percentage between 0 and 100. Change this to test!

#Convert Unix Time To String
risetime= datetime.datetime.fromtimestamp(sunrise).strftime('%H:%M:%S %Y-%m-%d')
settime=datetime.datetime.fromtimestamp(sunset).strftime('%H:%M:%S %Y-%m-%d')

#Convert String to Sunrise & Sunset Integer Array
sunRiseTime=[int(settime[0]+settime[1]), int(settime[3]+settime[4]), int(settime[6]+settime[7])]  
sunSetTime=[int(risetime[0]+risetime[1]), int(risetime[3]+risetime[4]), int(risetime[6]+risetime[7])]     

# print "sunrise:", sunrise
# print "sunset: ", sunset
# print "cloudCover: ", cloudCover

# print "risetime: ", risetime
# print "settime: ", settime

#Manual Override
print "sunRiseTime: ", sunRiseTime
print "sunSetTime: ", sunSetTime
print "cloudCover: ", cloudCover
# sunRiseTime = []; sunSetTime=[]; cloudCover=;
#######################################################################################

# Setup Light Bulb Object
lifxlan = LifxLAN()

# Warmth/Kelvin Variables
kelvin=2500;
kelvinRange = 9000-2500;
set2rise=False;
rise2set=False;

#Ccloudcover/Brightenss Variables
# Linear y=mx+b progression where 100% cloud coverage will lead to minBrightness and 0% will lead to maxBrightness
maxBrightness = 65535.0;
minBrightness = maxBrightness/2; # We can make the minimum brightness lower or higher here
CCSlope = (minBrightness-maxBrightness)/100; #This should be a neg number
CCAdjustedBrightness = cloudCover*CCSlope+maxBrightness;

# Hardcoded sunrise and sunset times
# sunSetTime=[18, 0, 0]; #Sunset = 6pm
# sunRiseTime=[6, 0, 0]; #Sunrise = 6am

# Math to calculate midDayTime time
midDayInMinutes =(sunSetTime[0]*60+sunSetTime[1] + sunRiseTime[0]*60+sunSetTime[1])/2;
midDayTime=[math.floor(midDayInMinutes/60), midDayInMinutes%60, 0];

# Current Time
formattedLocalTime = time.asctime(time.localtime(time.time()))
print "Local current time :", formattedLocalTime
localTime = time.localtime(time.time())
print "Local current time :", localTime [3], localTime[4], localTime[5]
hour = localTime [3];
minute = localTime [4];
second = localTime [5];

# Determine if Set2Rise or Rise2Set
if ((hour >= sunSetTime[0] and hour <= 24) or (hour >= 0 and hour <= sunRiseTime[0])):
    set2rise=True;
else:
    rise2set=True;

# Determining kelvin Parameter
if set2rise == True:
    kelvin=2500;
    CCAdjustedBrightness = minBrightness;

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

input=[0, 0, CCAdjustedBrightness, kelvin];
lifxlan.set_color_all_lights(input, rapid=True)

print "Kelvin: ", kelvin
print "Bightness: ", CCAdjustedBrightness