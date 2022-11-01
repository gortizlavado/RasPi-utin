#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from electricity.electricity import Electricity
from task.task import Task
from weather.forecast import Forecast
from weather.weather import Weather
from display.display import Display
from settings import REQUEST_NEXT_DAY
from lib import epd7in5_V2
from util.time_helper import *

import urllib3
import logging
import time

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
    t = Task(http)
    return t.request_task()

def run_forecast(http):
    f = Forecast(http)
    return f.request_forecast()

def run_weather(http):
    w = Weather(http)
    return w.request_current_weather()

def init_epd():
    epd = epd7in5_V2.EPD()
    
    epd.init()
    epd.Clear()
    logging.info("inited epd!")
    return epd

def run_epd(d):
    # transform data
    d.transform_data_into_image()
    # print data
    epd.display(epd.getbuffer(d.himage))
    logging.info("printed in display!")

    #logging.info("Goto Sleep...")
    #epd7in5_V2.epdconfig.module_exit()
    epd.sleep()

def Merge(dict1, dict2):
    for i in dict2.keys():
        dict1[i]=dict2[i]
    return dict1

try:
    if __name__ == '__main__':
        
        # load data
        http = urllib3.PoolManager()
        electricity_data = run_electricity(http)
        task_data = run_task(http)
        forecast_data = run_forecast(http)
        weather_data = run_weather(http)
        logging.info("loaded data!")

        # init epd
        epd = init_epd()
        run_epd(d = Display(electricity_data, task_data, forecast_data, weather_data))

        data = dict()
        data[fetch_date_now()] = False
        while True:
            hour_now = fetch_hour_now()
            logging.info("this is: " + hour_now + "h")
            if REQUEST_NEXT_DAY == hour_now and False == data[fetch_date_now()] :
                logging.info("time to ask more data from tomorrow")
                tomorrow = fetch_date_tomorrow()
                electricity_data = run_electricity(http, filter=hour_now)
                more_electricity_data = run_electricity(http, date=tomorrow, size=6)
                run_epd(d=Display(Merge(electricity_data, more_electricity_data), task_data, forecast_data, weather_data))
                data[fetch_date_now()] = True
                data[tomorrow] = False
            time.sleep(60)

        #logging.info("Clear...")
        #epd.init()
        #epd.Clear()


except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
