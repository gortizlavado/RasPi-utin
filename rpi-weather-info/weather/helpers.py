from datetime import datetime
from settings import APP_ID
from settings import LATITUDE
from settings import LONGITUDE
import weather.constants as c
import json

def do_request_forecast(http):
    filter = c.FILTER_BY_REGION + c.FILTER_BY_APP_ID + c.FILTER_OPTIONS_UNITS + c.FILTER_OPTIONS_COUNT
    return do_request(http, c.API_URL_FORECAST, filter)

def do_request_weather(http):
    filter = c.FILTER_BY_REGION + c.FILTER_BY_APP_ID + c.FILTER_OPTIONS_UNITS
    return do_request(http, c.API_URL_WEATHER, filter)

def do_request(http, url, filter):
    filter = filter.replace(c.APP_PLACEHOLDER, APP_ID).replace(c.LAT_PLACEHOLDER, LATITUDE).replace(c.LON_PLACEHOLDER, LONGITUDE)
    response = http.request(c.HTTP_GET_METHOD, url + filter)
    return json.loads(response.data.decode('utf-8'))        

def parse_response_forecast(forecast):
    forecasts = forecast.response["list"]
    now = datetime.now()
    data = dict()
    
    for forecast in forecasts:
        dt = string_to_date_time(forecast["dt_txt"])
        just_hour = str(dt.hour)
        if (now < dt and just_hour != "3") :
            temp_array = [str(forecast["main"]["temp"]) + c.CELSIUS_UNIT, forecast["weather"][0]["icon"]]
            data[dt.strftime("%d/%m %H:%M")] = temp_array

    return data

def parse_response_weather(forecast):
    now = datetime.now()
    data = dict()

    data["temp"] = str(forecast.response["main"]["temp"]) + c.CELSIUS_UNIT
    data["feels_like"] = str(forecast.response["main"]["feels_like"]) + c.CELSIUS_UNIT
    data["humidity"] = str(forecast.response["main"]["humidity"]) + c.PERCENT_SYMBOL
    data["icon"] = forecast.response["weather"][0]["icon"]
    dt = timestampToDate(forecast.response["dt"])
    data["date"] = dt.strftime("%d %B %Y")
    data["day"] = dt.strftime("%A")
    data["time"] = now.strftime("%H:%M")

    return data    

def string_to_date_time(strDatetime):
    return datetime.strptime(strDatetime, "%Y-%m-%d %H:%M:%f")

def timestampToDate(timestamp):
    return datetime.fromtimestamp(timestamp, tz=None)
