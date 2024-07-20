#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#from lib import epd7in5_V2
from settings import REQUEST_NEXT_DAY
from raspiutin import Raspiutin
from util.time_helper import fetch_date_now
from util.time_helper import fetch_hour_now
from util.time_helper import fetch_date_tomorrow

import logging
import time

logging.basicConfig(level=logging.INFO)

def init_epd():
    epd = epd7in5_V2.EPD()
    epd.init()
    logging.info("inited epd!")
    return epd

def refresh(epd, himage):
    epd.Clear()
    run_epd(epd, himage)

def run_epd(epd, himage):
    epd.display(epd.getbuffer(himage))
    logging.info("printed in display!")

    #logging.info("Goto Sleep...")
    epd.sleep()

try:
    if __name__ == '__main__':

        # 1. Init EPD
        #epd = init_epd()
        # 2. Create Raspiutin
        rpi = Raspiutin()
        rpi.start()
        # 3. Print into EPD
        #refresh(epd, rpi.provide_himage())
        # 4. Continue runing
        data = dict()
        data[fetch_date_now()] = False
        logging.info("--> up and runing <--")
        while True:
            hour_now = fetch_hour_now()
            logging.info("this is: " + hour_now + "h")
            if REQUEST_NEXT_DAY == hour_now and False == data[fetch_date_now()] :
                logging.info("time to ask more data for tomorrow")
                rpi.afternoon_behaviour()
                #refresh(epd, rpi.provide_himage())
                data[fetch_date_now()] = True
                data[fetch_date_tomorrow()] = False
            time.sleep(60)
            logging.info(data)

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
