# Python program to find current  
# weather details of any city 
# using openweathermap api 
  
import requests, json 
  
api_key = "31bf018c6919aeee4f9122e09977a0f4"
  
base_url = "http://api.openweathermap.org/data/2.5/weather?"
  
city_name = "Covilhã"
  
# complete url address 
complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
  
# get method of requests module 
# return response object 
response = requests.get(complete_url) 
  
# json method of response object  
# convert json format data into 
# python format data 
x = response.json() 
  
# Now x contains list of nested dictionaries 
# Check the value of "cod" key is equal to 
# "404", means city is found otherwise, 
# city is not found 
if x["cod"] != "404": 
  
    # store the value of "main" 
    # key in variable y 
    y = x["main"] 
  
    # store the value corresponding 
    # to the "temp" key of y 
    current_temperature = y["temp"] 
    current_temperature = round(current_temperature - 273.15, 2) # in celsius

    # store the value corresponding 
    # to the "pressure" key of y 
    current_pressure = y["pressure"] 
  
    # store the value corresponding 
    # to the "humidity" key of y 
    current_humidiy = y["humidity"] 
  
    # store the value of "weather" 
    # key in variable z 
    z = x["weather"] 
  
    # store the value corresponding  
    # to the "description" key at  
    # the 0th index of z 
    weather_description = z[0]["description"] 
  
    # print following values 
    print("\n Temperature = " + str(current_temperature) + " ºC\n")
    print(" Atmospheric pressure = " + str(current_pressure) + " hPa\n")
    print(" Humidity = " + str(current_humidiy) + " %\n")
    print(" Description = " + str(weather_description) + "\n")

    #print(x)
  
else: 
    print(" City Not Found ")
