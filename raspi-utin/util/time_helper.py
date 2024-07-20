from datetime import datetime
from datetime import timedelta

def fetch_datetime_now():
    return datetime.now()

def fetch_hour_now():
    return datetime.now().strftime("%H")

def fetch_date_now():
    return datetime.now().date()

def fetch_date_tomorrow():
    tomorrow = fetch_datetime_now() + timedelta(days=1)
    return tomorrow.date()

def string_to_date_time(str_datetime):
    return datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%f")

def string_to_date(str_date):
    datetime_parsed = datetime.strptime(str_date, "%Y-%m-%d")
    return datetime_parsed.date()

def timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp, tz=None)