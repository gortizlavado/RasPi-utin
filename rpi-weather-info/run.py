# -*- coding:utf-8 -*-

from electricity.electricity import Electricity
from task.task import Task
from weather.forecast import Forecast
from weather.weather import Weather
from lib import epd7in5_V2

from PIL import Image,ImageDraw,ImageFont

import urllib3
import logging
import sys

import time

logging.basicConfig(level=logging.INFO)

picdir = sys.path[0] + '/pic/'

def run_electricity(http):
    e = Electricity(http)
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

def draw_skeleton(draw):
    # Draw one rectangle for weather data
    draw.rectangle([(0, 0),(479, 120)], outline = 0)
    # And another for the tasks
    draw.rectangle([(0, 320),(239, 799)], outline = 0)
    # And a third for the electric
    draw.rectangle([(241, 320),(479, 799)], outline = 0)

def generate_font_by(size):
    return ImageFont.truetype(picdir + 'Font.ttc', size)

def loop_tasks(name, list_name, value_y):
    y = value_y
    draw.text((60, y), name, font = font35, fill = 0)
    y = y + 10
    for overdue in task_data[list_name]:
        y = y + 30
        draw.text((x, y), overdue, font = font22, fill = 0)
    y = y + 40
    return y

def load_weather_icon_and_resize(name):
    icon_name = name.replace("n", "d")
    weather_icon = Image.open(picdir + icon_name + '.png')
    icon_resized = weather_icon.resize(size=(50, 50))
    return icon_resized

try:
    if __name__ == '__main__':

        # load fonts
        font58 = generate_font_by(size=58)
        font35 = generate_font_by(size=35)
        font32 = generate_font_by(size=32)
        font28 = generate_font_by(size=28)
        font22 = generate_font_by(size=22)
        font12 = generate_font_by(size=12)
        logging.info("loaded fonts!")
        
        # load data
        http = urllib3.PoolManager()
        electricity_data = run_electricity(http)
        task_data = run_task(http)
        forecast_data = run_forecast(http)
        weather_data = run_weather(http)
        logging.info("loaded data!")

        # init epd
        epd = init_epd()

        himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        himage = himage.transpose(Image.ROTATE_90)
        draw = ImageDraw.Draw(himage)
        draw_skeleton(draw=draw)
        logging.info("drawed skeleton!")

        # draw data
        # upper content ----------------------------------------------------------------------
        # weather content --------480/2=240 (x) 120/2=60 (y)
        draw.text((50, 10), weather_data.get('time'), font = font58, fill = 0)
        icon = load_weather_icon_and_resize(weather_data.get('icon'))
        himage.paste(icon, (35, 65))
        draw.text((90, 75), weather_data.get('temp'), font = font28, fill = 0)
        draw.text((280, 15), weather_data.get('day'), font = font35, fill = 0)
        draw.text((240, 60), weather_data.get('date'), font = font32, fill = 0)
        # end of weather content ---------------------------
        
        # forecast content -------480/2=240 (x) 200/2=100 (y)
        x = 20
        y = 130
        i = 0
        for forecast in forecast_data:
            if i == 5:
                y = 220
                x = 20
            draw.text((x, y), forecast, font = font12, fill = 0)
            icon = load_weather_icon_and_resize(forecast_data[forecast][1])
            himage.paste(icon, (x + 5, y + 15))
            draw.text((x + 10, y + 65), forecast_data[forecast][0], font = font12, fill = 0)
            x = x + 95
            i = i + 1
        # end if forecast content --------------------------
        # end of upper content ---------------------------------------------------------------

        # left content -----------------------------------------------------------------------
        y = 335
        x = 25
        if 'overdue' in task_data:
            y = loop_tasks('OVER', 'overdue', y)
        if 'today' in task_data:
            y = loop_tasks('TODAY', 'today', y)
        if 'futuredue' in task_data:
            loop_tasks('FUTURE', 'futuredue', y)
        # end of left content ----------------------------------------------------------------

        # right content ----------------------------------------------------------------------
        y = 335
        for electricity in electricity_data:
            draw.text((250, y), electricity, font = font22, fill = 0)
            draw.text((385, y), str(electricity_data[electricity]), font = font22, fill = 0)
            y = y + 25
        # end of right content ---------------------------------------------------------------
        logging.info("drawed data!")

        epd.display(epd.getbuffer(himage))
        logging.info("printed in display!")
        time.sleep(20)

        logging.info("Clear...")
        epd.init()
        epd.Clear()

        logging.info("Goto Sleep...")
        epd.sleep()


except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
