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
  url = "https://restapi.amap.com/v3/weather/weatherInfo?city=130281&key=0585d5f62dbbb2d1a98ede613a459885&extensions=all"
  res = requests.get(url).json()
  return res['forecasts'][0]['casts'][0]['dayweather'],res['forecasts'][0]['casts'][0]['nightweather'],res['forecasts'][0]['casts'][0]['daytemp'],res['forecasts'][0]['casts'][0]['nighttemp'],res['forecasts'][0]['casts'][1]['dayweather'],res['forecasts'][0]['casts'][1]['nightweather'],res['forecasts'][0]['casts'][1]['daytemp'],res['forecasts'][0]['casts'][1]['nighttemp']
  

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
    # 发送请求获取数据
    response = requests.get("http://api.tianapi.com/everyday/index?key=d6dc42eacf22161cc5536076302cc0e1")
    
    # 检查请求是否成功
    if response.status_code != 200:
        return get_words()  # 如果请求失败，递归调用自身重试
    
    # 解析 JSON 数据
    data = response.json()
    
    # 提取 content 和 note 字段
    content = data['newslist'][0]['content']
    note = data['newslist'][0]['note']
    
    return content, note

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
content, note = get_words()
jdayweather,jnightweather,jdaytemp,jnighttemp,mdayweather,mnightweather,mdaytemp,mnighttemp= get_weather()
data = {"jdayweather":{"value":jdayweather},"jnightweather":{"value":jnightweather},"jdaytemp":{"value":jdaytemp},"jnighttemp":{"value":jnighttemp},"mdayweather":{"value":mdayweather},"mnightweather":{"value":mnightweather},"mdaytemp":{"value":mdaytemp},"mnighttemp":{"value":mnighttemp},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"zwords":{"value":content},"ywords":{"value":note}}
res = wm.send_template(user_id, template_id, data)
print(res)
