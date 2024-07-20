from weather.helpers import *

import logging

logging.basicConfig(level=logging.DEBUG)

class Weather:
    def __init__(self, http):
        self.http = http

    def request_current_weather(self):
        self.response = do_request_weather(self.http)
        logging.debug("response: " + str(self.response))
        data = parse_response_weather(self)
        logging.info("The Current Weather: " + str(data))

        return data