from datetime import datetime
from electricity.helpers import *

import logging

logging.basicConfig(level=logging.DEBUG)

class Electricity:
    def __init__(self, http):
        self.http = http
        self.now = datetime.now()

    def request_price(self):
        self.response = do_request(self.http, self.now)
        logging.debug("response: " + str(self.response))
        data = parse_response(self)
        logging.info("The prices : " + str(data) + ". Length: " + str(len(data)))
        return data