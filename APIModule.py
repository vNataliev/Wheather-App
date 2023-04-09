import requests
import json


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

def getGeoLocation(cityName):
    locationPackage = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={cityName}").text
    locationJson = json.loads(locationPackage)["results"][0]
    latitude = locationJson["latitude"]
    longitude = locationJson["longitude"]
    return (latitude, longitude)

def getWheatherForecast(latitude, longitude):
    wheatherPackage = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,weathercode").text
    wheatherJson = json.loads(wheatherPackage)
    return wheatherJson

def getCitiesPackage(text):
    if text:
        citiesPackage = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={text}").text
        try:
            citiesJson = json.loads(citiesPackage)["results"]
            city, country = [], []
            for i in citiesJson:
                if "name" and "country" in i.keys():
                    city.append(i["name"])
                    country.append(i["country"])
            return city, country
        except:
            return [],[]
    else:
        return [], []

def splitPackage(package):
    return list(batch(package, 24))

def getLists(cityName):
    location = getGeoLocation(cityName) 
    wheatherForecast = getWheatherForecast(*location)
    daysTemperature = splitPackage(wheatherForecast["hourly"]["temperature_2m"])
    daysCodes = splitPackage(wheatherForecast["hourly"]["weathercode"])
    return daysTemperature, daysCodes

def getCities(text):
    return getCitiesPackage(text)
