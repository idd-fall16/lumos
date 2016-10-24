import pyowm
import datetime
import time

owm = pyowm.OWM('ddafbf402476a208be381344dacee8ca')  # You MUST provide a valid API key

# You have a pro subscription? Use:
# owm = pyowm.OWM(API_key='your-API-key', subscription_type='pro')

# Search for current weather in SF()
observation = owm.weather_at_place('Sanfrancisco,us')
w = observation.get_weather()

# Weather details
sunrise=w.get_sunrise_time()
sunset=w.get_sunset_time()
cloudcover=w.get_clouds() #we can use to this for light data

#Convert Unix Time To String
risetime= datetime.datetime.fromtimestamp(sunrise).strftime('%H:%M:%S %Y-%m-%d')
settime=datetime.datetime.fromtimestamp(sunset).strftime('%H:%M:%S %Y-%m-%d')

#Convert String to Sunrise & Sunset Integer Array
srise=[int(risetime[0]+risetime[1]), int(risetime[3]+risetime[4]), int(risetime[6]+risetime[7])]    
sset=[int(settime[0]+settime[1]), int(settime[3]+settime[4]), int(settime[6]+settime[7])]   
