from weather.helpers import *

import logging

logging.basicConfig(level=logging.DEBUG)

class Forecast:
    def __init__(self, http):
        self.http = http

    def request_forecast(self):
        self.response = do_request_forecast(self.http)
        logging.debug("response: " + str(self.response))
        data = parse_response_forecast(self)
        logging.info("The Forecast: " + str(data) + ". Length: " + str(len(data)))
        return data