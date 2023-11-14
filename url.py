from datetime import datetime, timedelta
import re

import requests
from bs4 import BeautifulSoup

from SETTINGS import *

def create_url(type:str ,city:str, rooms:list = None, m_2_from:str = None, m_2_to:str = None, price_from:str = None, price_to:str = None,subcategory:str = None) -> str:
    if type == "stancje-pokoje":
        url = BASE_URL + f"{type}/" + f"{city}/"
    else:
        url = BASE_URL + f"{type}/"
        if subcategory:
            subcategory = subcategory.replace("ż","z")
            url += f"{subcategory}/" + f"{city}/"
        else:
            url += f"{city}/"

    url += "?"

    if price_from:
        url += PRICE_STR_FROM + f"{price_from}&"
    if price_to:
        url += PRICE_STR_TO + f"{price_to}&"
    if m_2_from:
        url += M_2_STR_FROM + f"{m_2_from}&"
    if m_2_to:
        url += M_2_STR_TO + f"{m_2_to}&"
    if rooms:
        room_counter = 0
        for room in rooms:
            url += f"{ROOMS}[{room_counter}]"
            if room == "Kawalerka":
                url += "=one&"
            if room == "2 pokoje":
                url += "=two&"
            if room == "3 pokoje":
                url += "=three&"
            if room == "4 i więcej":
                url += "=four&"
            room_counter += 1

    if url[-1] == "&":
        url = url[:-1]
    return url

def modify_time(current_time:datetime, is_string:bool = False, delta:int = timedelta(hours=2) ) -> datetime:
    if is_string:
        new_datetime = (datetime.combine(datetime.today(), current_time) + delta).time()
        new_time_str = new_datetime.strftime('%H:%M')
        return new_time_str

    current_timedelta = timedelta(hours=current_time.hour, minutes=current_time.minute)
    new_timedelta = current_timedelta - delta
    new_hour = new_timedelta.seconds // 3600
    new_minute = (new_timedelta.seconds % 3600) // 60
    today = datetime.today()
    new_datetime = datetime(today.year, today.month, today.day, new_hour, new_minute)

    return new_datetime


def get_room_olx(url:str,city:str, current_time:datetime) -> (datetime,list):
    new_current_time = modify_time(current_time)
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    rooms = soup.find_all("div", class_ = 'css-1sw7q4x')
    room_list = []

    time_end = datetime.now()
    end_time = time_end.time()

    for room in rooms:
        date_added = room.find("p", class_ = "css-veheph er34gjf0")
        if (not date_added) or (city not in date_added.get_text()):
            continue
        if re.search("Dzisiaj",date_added.get_text()):
            time_added = date_added.get_text()[-5:]
            h_m_time_added = datetime.strptime(time_added, "%H:%M").time()
            if h_m_time_added >= new_current_time.time():
                a_class = room.find("a", class_ = "css-rc5s2u")
                link = a_class["href"]
                h_m_time_added_2 = modify_time(h_m_time_added, True)
                new_room = [link, h_m_time_added_2]
                room_list.append(new_room)

    return end_time, room_list


