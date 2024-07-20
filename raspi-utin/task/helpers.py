from util.time_helper import *
from settings import PROJECT_ID
from settings import TOKEN
import task.constants as c
import json

def do_request(http):
    
    filter = c.FILTER_PROJECT_ID.replace(c.PROJECT_PLACEHOLDER, PROJECT_ID) + c.FILTER_BY_DUE
    headers = {c.HEADER_AUTH: c.HEADER_BEARER + TOKEN}

    response = http.request(c.HTTP_GET_METHOD, c.API_URL + filter, headers=headers)
    print(response.status)
    return json.loads(response.data.decode('utf-8'))

def parse_response(task):
    tasks = task.response
    date_now = fetch_date_now()

    overdue = set()
    futuredue = set()
    todaydue = set()
    
    data = dict()
    for task in tasks:
        dueTime = string_to_date(task["due"]["date"])
        if (date_now > dueTime) :
            overdue.add(task["content"])
        elif(date_now < dueTime) :
            futuredue.add(task["content"])
        else :
            todaydue.add(task["content"])

    if overdue :
        data['overdue'] = overdue
    if todaydue :
        data['today'] = todaydue
    if futuredue :    
        data['futuredue'] = futuredue
    
    return data
