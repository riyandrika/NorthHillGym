import requests
import time
import os
from telebot import TeleBot

api_token = os.environ["telebot_token"]
chat_id = 584775448

bot = TeleBot(api_token)
url = f"https://api.telegram.org/bot{api_token}/getUpdates"
updates = requests.get(url).json()
current_offset = updates["result"][-1]["update_id"]
bot.send_message(chat_id = chat_id, text = "Enter booking date <DD MMM>")

def get_update():
    text = updates["result"][-1]["message"]["text"]
    return text

while True:
    updates = requests.get(url).json()
    new_offset = updates["result"][-1]["update_id"]
    if new_offset != current_offset:
        break
    time.sleep(.5)

current_offset = new_offset
booking_date = get_update()

booking_date = f"{booking_date} 2021"
if len(booking_date) < 11:
    booking_date = "0" + booking_date
booking_date = booking_date.replace(" ", "-")

bot.send_message(chat_id = chat_id, text = "Enter booking time")

while True:
    updates = requests.get(url).json()
    new_offset = updates["result"][-1]["update_id"]
    if new_offset != current_offset:
        break
    time.sleep(.5)

booking_hour = get_update()
encode_time = {hour:hour+5 for hour in range(1,13)}
for hour in encode_time.values():
    if hour >= 8:
        encode_time[hour] -= 12
booking_time = booking_hour[:-2]
booking_time = str(encode_time[int(booking_time)])