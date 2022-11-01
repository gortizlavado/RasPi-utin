from util.font_factory import *

from PIL import Image,ImageDraw

import logging

class Display:
    def __init__(self, electricity, task, forecast, weather):
        self.electricity = electricity
        self.task = task
        self.forecast = forecast
        self.weather = weather

    def transform_data_into_image(self): 
        self.himage = Image.new('1', (800, 480), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(self.himage)
        self.draw_skeleton(draw)
        logging.info("drawed skeleton!")

        # load fonts
        font58 = font_size_58()
        font35 = font_size_35()
        font32 = font_size_32()
        font28 = font_size_28()
        font22 = font_size_22()
        font12 = font_size_12()
        logging.info("loaded fonts!")


        # draw data
        # upper content ----------------------------------------------------------------------
        # weather content --------480/2=240 (x) 120/2=60 (y)
        weather_data = self.weather
        draw.text((50, 10), weather_data.get('time'), font = font58, fill = 0)
        icon = self.load_weather_icon_and_resize(weather_data.get('icon'))
        self.himage.paste(icon, (35, 65))
        draw.text((90, 75), weather_data.get('temp'), font = font28, fill = 0)
        draw.text((280, 15), weather_data.get('day'), font = font35, fill = 0)
        draw.text((240, 60), weather_data.get('date'), font = font32, fill = 0)
        # end of weather content ---------------------------
        
        # forecast content -------480/2=240 (x) 200/2=100 (y)
        forecast_data = self.forecast
        x = 20
        y = 130
        i = 0
        for forecast in forecast_data:
            if i == 5:
                y = 220
                x = 20
            draw.text((x, y), forecast, font = font12, fill = 0)
            icon = self.load_weather_icon_and_resize(forecast_data[forecast][1])
            self.himage.paste(icon, (x + 5, y + 15))
            draw.text((x + 10, y + 65), forecast_data[forecast][0], font = font12, fill = 0)
            x = x + 95
            i = i + 1
        # end if forecast content --------------------------
        # end of upper content ---------------------------------------------------------------

        # left content -----------------------------------------------------------------------
        task_data = self.task
        y = 335
        x = 25
        if 'overdue' in task_data:
            y = self.loop_tasks(draw, task_data['overdue'], 'OVER', y, x)
        if 'today' in task_data:
            y = self.loop_tasks(draw, task_data['today'], 'TODAY', y, x)
        if 'futuredue' in task_data:
            self.loop_tasks(draw, task_data['futuredue'], 'FUTURE', y, x)
        # end of left content ----------------------------------------------------------------

        # right content ----------------------------------------------------------------------
        electricity_data = self.electricity
        y = 335
        for electricity in electricity_data:
            draw.text((250, y), electricity, font = font22, fill = 0)
            draw.text((385, y), str(electricity_data[electricity]), font = font22, fill = 0)
            y = y + 25
        # end of right content ---------------------------------------------------------------
        logging.info("drawed data!")

    def draw_skeleton(self, draw):
        # Draw one rectangle for weather data
        draw.rectangle([(0, 0),(479, 120)], outline = 0)
        # And another for the tasks
        draw.rectangle([(0, 320),(239, 799)], outline = 0)
        # And a third for the electric
        draw.rectangle([(241, 320),(479, 799)], outline = 0)

    def loop_tasks(self, draw, data, name, value_y, value_x):
        y = value_y
        x = value_x
        draw.text((60, y), name, font = font_size_35(), fill = 0)
        y = y + 10
        for item in data:
            y = y + 30
            draw.text((x, y), item, font = font_size_22(), fill = 0)
        y = y + 40
        return y

    def load_weather_icon_and_resize(self, name):
        icon_name = name.replace("n", "d")
        weather_icon = Image.open(picdir + icon_name + '.png')
        icon_resized = weather_icon.resize(size=(50, 50))
        return icon_resized
