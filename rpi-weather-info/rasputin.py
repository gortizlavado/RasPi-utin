#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from electricity.electricity import Electricity
from task.task import Task
from weather.forecast import Forecast
from weather.weather import Weather
from display.display import Display
from util.time_helper import fetch_hour_now
from util.time_helper import fetch_date_tomorrow

import urllib3
import logging

logging.basicConfig(level=logging.INFO)

def run_electricity(http, date=None, filter=None, size=None):
    e = Electricity(http)
    if date is not None :
        e.now = date
    if filter is not None :
        e.filter_hour = filter
    if size is not None :
        e.response_size = size
    return e.request_price()

def run_task(http):
    return Task(http).request_task()

def run_forecast(http):
    return Forecast(http).request_forecast()

def run_weather(http):
    return Weather(http).request_current_weather()

def merge(dict1, dict2):
    for i in dict2.keys():
        dict1[i]=dict2[i]
    return dict1    

class Rasputin:

    def __init__(self):
        self.http = urllib3.PoolManager()
        self.electricity_data = None
        self.task_data = None
        self.forecast_data = None
        self.weather_data = None

    def start(self):
        # load data
        self.task_data = run_task(self.http)
        self.electricity_data = run_electricity(self.http)
        self.forecast_data = run_forecast(self.http)
        self.weather_data = run_weather(self.http)
        logging.info("loaded data!")

    def afternoon_behaviour(self):
        electricity_data = run_electricity(self.http, filter=fetch_hour_now())
        more_electricity_data = run_electricity(self.http, date=fetch_date_tomorrow(), size=6)
        self.electricity = merge(electricity_data, more_electricity_data)


    def provide_himage(self):
        d = Display(self.electricity_data, self.task_data, self.forecast_data, self.weather_data)
        d.transform_data_into_image()
        return d.himage
