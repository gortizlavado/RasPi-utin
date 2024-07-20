from electricity.electricity import datetime
import electricity.constants as c
import json

def fetch_start_ime_as_str(now):
    return now.strftime("%Y-%m-%dT") + "00:00"

def fetch_end_time_as_str(now):
    return now.strftime("%Y-%m-%dT") + "23:59"

def string_to_date_iso_format(strDateIso):
    return datetime.fromisoformat(strDateIso)

def do_request(http, now):
    filter = c.FILTER_START_DATE_TODAY + fetch_start_ime_as_str(now) + c.FILTER_END_DATE_TODAY + fetch_end_time_as_str(now) + c.FILTER_TIME_TRUNC_HOUR
    response = http.request(c.HTTP_GET_METHOD, c.API_URL + filter)
    return json.loads(response.data.decode('utf-8'))

def parse_response(electricity):
    format = "%d/%m %H"
    prices = electricity.response["included"][0]["attributes"]["values"]
    str_now = electricity.now.strftime(format)

    lowPrice = 1
    highPrice = 0
    data = dict()
    for price in prices :
        value = round(price["value"]/1000, 5)
        if value < lowPrice :
            lowPrice = value
        if value > highPrice :
            highPrice = value    
        time = string_to_date_iso_format(price["datetime"])
        str_time = time.strftime(format)
        if (str_now <= str_time) :
            data[str_time + 'h'] = value

    data['lowest'] = lowPrice
    data['highest'] = highPrice

    return data

def filter_data_by_time(electricity_data, hour_now) :

    data = dict()
    for electricity in electricity_data:
        key = electricity[6:8]
        if (key.isnumeric() and hour_now <= key) :
            data.setdefault(key + 'h', electricity_data.get(electricity))

    return data

def resize_data(electricity_data, size) :
    data = dict()
    for index, (key, value) in enumerate(electricity_data.items()):
        if (index < size) :
            data.setdefault(key, value)

    return data
