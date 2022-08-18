# settings.py
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# TASK
PROJECT_ID = os.environ.get("PROJECT_ID")
TOKEN = os.getenv('TOKEN_TASK')

# WEATHER
APP_ID = os.getenv('APP_ID')
LATITUDE = os.getenv('LAT')
LONGITUDE = os.getenv('LON')
