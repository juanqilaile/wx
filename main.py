from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "https://restapi.amap.com/v3/weather/weatherInfo?city=130802&key=0585d5f62dbbb2d1a98ede613a459885&extensions=all"
  res = requests.get(url).json()
  return res['forecasts'][0]['casts'][1]['dayweather'],res['forecasts'][0]['casts'][1]['nightweather'],res['forecasts'][0]['casts'][1]['daytemp'],res['forecasts'][0]['casts'][1]['nighttemp'],res['forecasts'][0]['casts'][2]['dayweather'],res['forecasts'][0]['casts'][2]['nightweather'],res['forecasts'][0]['casts'][2]['daytemp'],res['forecasts'][0]['casts'][2]['nighttemp']
  

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  oneDay = datetime(datetime.today().year+","+birthday)
  return oneDay.toordinal()-today.toordinal()

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
jdayweather,jnightweather,jdaytemp,jnighttemp,mdayweather,mnightweather,mdaytemp,mnighttemp= get_weather()
data = {"jdayweather":{"value":jdayweather},"jnightweather":{"value":jnightweather},"jdaytemp":{"value":jdaytemp},"jnighttemp":{"value":jnighttemp},"mdayweather":{"value":mdayweather},"mnightweather":{"value":mnightweather},"mdaytemp":{"value":mdaytemp},"mnighttemp":{"value":mnighttemp},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
