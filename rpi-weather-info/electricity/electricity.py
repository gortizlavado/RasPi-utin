from util.time_helper import *
from electricity.helpers import do_request, parse_response, filter_data_by_time, resize_data

import logging

logging.basicConfig(level=logging.DEBUG)

class Electricity:
    def __init__(self, http):
        self.http = http
        self.now = fetch_datetime_now()
        self.filter_hour = None
        self.response_size = None

    def request_price(self):
        self.response = do_request(self.http, self.now)
        logging.debug("response: " + str(self.response))
        data = parse_response(self)
        logging.info("The prices : " + str(data) + ". Length: " + str(len(data)))
        if self.filter_hour is not None :
            data = filter_data_by_time(data, self.filter_hour)
            logging.info("The prices are filtered by " + self.filter_hour + " :" + str(data) + ". Length: " + str(len(data)))
        if self.response_size is not None :
            data = resize_data(data, self.response_size)
            logging.info("The prices are resized by " + str(self.response_size) + " :" + str(data) + ". Length: " + str(len(data)))    
        return data