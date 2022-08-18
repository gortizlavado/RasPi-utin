from task.helpers import *

import logging

logging.basicConfig(level=logging.DEBUG)

class Task:
    def __init__(self, http):
        self.http = http
    
    def request_task(self):
        self.response = do_request(self.http)
        logging.debug("response: " + str(self.response))
        data = parse_response(self)
        logging.info("The tasks : " + str(data) + ". Length: " + str(len(data)))

        return data