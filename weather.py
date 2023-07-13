import requests
import json
#import network

""" Reference
https://data.weather.gov.hk/weatherAPI/doc/HKO_Open_Data_API_Documentation_sc.pdf
https://data.weather.gov.hk/weatherAPI/doc/HKO_Open_Data_API_Documentation.pdf
https://www.hko.gov.hk/en/wxinfo/dailywx/warnlegend.htm
https://www.hko.gov.hk/textonly/v2/explain/wxicon_e.htm
"""

icon = {
  "50":"Sunny",
  "51":"Sunny Periods",
  "52":"Sunny Intervals",
  "53":"Sunny Periods with A Few Showers",
  "54":"Sunny Intervals with Showers",
  "60":"Cloudy",
  "61":"Overcast",
  "62":"Light Rain",
  "63":"Rain",
  "64":"Heavy Rain",
  "65":"Thunderstorms",
  "70":"Fine",
  "71":"Fine",
  "72":"Fine",
  "73":"Fine",
  "74":"Fine",
  "75":"Fine",
  "76":"Mainly Cloudy",
  "77":"Mainly Fine",
  "80":"Windy",
  "81":"Dry",
  "82":"Humid",
  "83":"Fog",
  "84":"Mist",
  "85":"Haze",
  "90":"Hot",
  "91":"Warm",
  "92":"Cool",
  "93":"Cold"
}

weather_warning_signal = {
	"WFIREY" : "Yellow Fire Danger Warning",
	"WFIRER" : "Red Fire Danger Warning",
	"WFROST" : " Frost Warning",
	"WHOT" : "Hot Weather Warning",
	"WCOLD" : "Cold Weather Warning",
	"WMSGNL" : "Strong Monsoon Signal",
	"WRAINA" : "Amber Rainstorm Warning Signal",
	"WRAINR": "Red Rainstorm Warning Signal",
	"WRAINB" : "Black Rainstorm Warning Signal",
	"WFNTSA" : "Special Announcement on Flooding in the northern New Territories",
	"WL" : "Landslip Warning", 
	"WTMW" : "Tsunami Warning",
	"WTS" : "Thunderstorm Warning",
	"TC1" : "Standby Signal No. 1",
	"TC3" : "Strong Wind Signal No. 3",
	"TC8NE" : "No. 8 Northeast Gale or Storm Signal",
	"TC8SE" : "No. 8 Southeast Gale or Storm Signal",
	"TC8NW" : "No. 8 Northwest Gale or Storm Signal",
	"TC8SW" : "No. 8 Southwest Gale or Storm Sign",
	"TC9" : "Increasing Gale or Storm Signal No. 9",
	"TC10" : "Hurricane Signal No. 10",
}


def get_info(type):
	if type == "warning":
		url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warnsum&lang=en"
	elif type == "weather_report":
		url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en"
	elif type == "rainfall_forecast":
		url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=en"

	res = requests.get(url)
	data=json.loads(res.text)
	return data

def weather_warning():
	warning_list = []
	data = get_info("warning") 

	if data != "": # 判斷是否爲空字串
		for i in ("WFIRE","WFROST","WHOT","WCOLD","WMSGNL","WRAIN","WFNTSA","WL","WTCSGNL","WTMW","WTS"): # 遍歷循環所有天氣警告
			if i in data:
				warning_list.append(weather_warning_signal[data[i]["code"]]) # 獲取所有天氣警告數據
		
		return warning_list 

	else:
		return None


#print(weather_warning())

"""
示例代碼
warning = weather_warning()
if warning == None:
	print("No weather warning")
else:
	for i in range(len(warning)) :
		print(warning[i])

"""



def weather_info():
	info_list = []
	data  = get_info("weather_report")
	for i in range(len(data["icon"])):
		info_list.append(icon[str(data["icon"][i])]) # 獲取所有 Weather Icon 的數據
	return info_list

#print(weather_info())

"""示例代碼
info = weather_info()
for i in range(len(info)):
	print(info[i])
"""


def rainfall_forecast():
	data = get_info("rainfall_forecast")["weatherForecast"][0] #取翌日的天氣預報
	return data["PSR"] # 取降雨概率

#print(rainfall_forecast())


def temperature():
    data  = get_info("weather_report")["temperature"]["data"]
    temp = str(data[1]["value"]) + "°C" # Get the temperature in Hong Kong Observatory
    return temp

print(temperature())

