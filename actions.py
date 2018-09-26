from rasa_core.actions import Action
from rasa_core.events import AllSlotsReset
from rasa_core.events import Restarted
import sqlite3
import time
import datetime
from basic_data import *



class ActionNoneWeather(Action):
    def name(self):
        return 'action_none_weather'
    def run(self, dispatcher, tracker, domain):
        weather_dot = tracker.get_slot("weather_dot")
        if weather_dot == None:
            dispatcher.utter_template("utter_please_ask_weather", tracker)
        return[AllSlotsReset()]

class ActionSearchBlurryWeather(Action):
    def name(self):
        return 'action_search_blurry_weather'

    def run(self, dispatcher, tracker, domain):
        cursor = get_weather_db(wea_db_path)
        local = tracker.get_slot("location")
        # item = extract_item(item)
        if local is None:
            local = basic_location

        blurry_date  = tracker.get_slot("blurry_time")
        # if blurry_date is None:
        #     dispatcher.utter_template("utter_ask_blurry_time",tracker)
        #     return []
        # query database here using item and time as key. but you may normalize time format first.
        date = get_time(blurry_date)
        res = select_blurry_weather(cursor,date,local)
        if not res ==None:
            dispatcher.utter_message(show_weather_information(date,res))
        else:
            dispatcher.utter_template("utter_select_none", tracker)
        return []


class ActionSearchPreciseWeather(Action):
    def name(self):
        return 'action_search_precise_weather'

    def run(self, dispatcher, tracker, domain):
        cursor = get_weather_db(wea_db_path)
        local = tracker.get_slot("location")
        # item = extract_item(item)
        if local is None:
            local = basic_location
        # if ((month == None ) or (day == None)):
        #     dispatcher.utter_template("utter_ask_blurry_time", tracker)
        #     return []
        month = tracker.get_slot("month")
        day = tracker.get_slot("day")
        date = get_precise_date(month,day)
        res = select_blurry_weather(cursor, date, local)
        cursor.close()
        if not res ==None:
            dispatcher.utter_message(show_weather_information(date,res))
        else:
            dispatcher.utter_template("utter_select_none", tracker)
        return []


class ActionSearchSpecialItem(Action):
    def name(self):
        return 'action_search_special_item'

    def run(self, dispatcher, tracker, domain):
        cursor = get_weather_db(wea_db_path)
        # dispatcher.utter_message("还没写")
        local = tracker.get_slot("location")
        special_item = tracker.get_slot("special_item")
        # item = extract_item(item)
        if local is None:
            local = basic_location


        # if special_item is None:
        #     dispatcher.utter_template("utter_ask_special_item",tracker)
        #     return []
        # # query database here using item and time as key. but you may normalize time format first.
        special_item = get_special_item(special_item)
        res = select_special_item(cursor,special_item,local)
        cursor.close()
        if not res ==None:
            dispatcher.utter_message(show_special_item(special_item,res))
        else:
            dispatcher.utter_template("utter_select_none", tracker)
        return []

class ActionSearchPollution(Action):
    def name(self):
        return 'action_search_pollution'

    def run(self, dispatcher, tracker, domain):
        cursor = get_weather_db(wea_db_path)
        local = tracker.get_slot("location")
        # item = extract_item(item)
        if local is None:
            local = basic_location
        #
        pollution  = tracker.get_slot("pollution")
        # if pollution is None:
        #     dispatcher.utter_template("utter_ask_blurry_time",tracker)
        #     return []
        # # query database here using item and time as key. but you may normalize time format first.
        res = select_pollution(cursor,local)
        cursor.close()
        if not res ==None:
            dispatcher.utter_message(show_pollution(res))
        else:
            dispatcher.utter_template("utter_select_none", tracker)
        return []


class ActionRestarted(Action):
    def name(self):
        return 'action_restarted'
    def run(self, dispatcher, tracker, domain):
        return[Restarted()]

class ActionSlotReset(Action):
    def name(self):
        return 'action_slot_reset'
    def run(self, dispatcher, tracker, domain):
        return[AllSlotsReset()]


def get_weather_db(wea_db_path):
    conn = sqlite3.connect(wea_db_path)
    cursor = conn.cursor()
    return cursor

def select_blurry_weather(cursor,date,location):
    res = None
    if date == "未来一周":
        cursor.execute('SELECT * FROM weather WHERE city_name="{}"'.format(location))
        res = cursor.fetchall()
    elif date == get_time("今天"):
        cursor.execute('SELECT * FROM weather WHERE city_name="{}" and date ="{}"'.format(location, date))
        res1 = cursor.fetchall()
        cursor.execute('SELECT * FROM pm WHERE city="{}" '.format(location))
        res2 = cursor.fetchall()
        res = res1+res2
    else:
        cursor.execute('SELECT * FROM weather WHERE city_name="{}" and date ="{}"'.format(location,date))
        res = cursor.fetchall()
    return res

def select_special_item(cursor,special_item,location):
    res = None
    if special_item == 'wind' or special_item == 'wind_inten':
        cursor.execute('SELECT {},{} FROM pm WHERE city="{}"  '.format('wind','wind_inten', location))
    else:
        cursor.execute('SELECT {} FROM pm WHERE city="{}"  '.format(special_item,location))
    res = cursor.fetchall()
    return res

def select_pollution(cursor, local):
    res = None
    cursor.execute('SELECT * FROM pm WHERE city="{}"  '.format(local))
    res = cursor.fetchall()
    return res

def get_time(label):
    res = None
    now_time = datetime.datetime.now()
    if label =='今天':
        c = time.strftime('%Y %m %d').split()
        res = "{}月{}日".format(c[1],c[2])
    elif label =='明天':
        yes_time = now_time + datetime.timedelta(days=+1)
        c = yes_time.strftime('%Y %m %d').split()
        res = "{}月{}日".format(c[1],c[2])
    elif label =='后天':
        yes_time = now_time + datetime.timedelta(days=+2)
        c = yes_time.strftime('%Y %m %d').split()
        res = "{}月{}日".format(c[1],c[2])
    elif label =='大后天':
        yes_time = now_time + datetime.timedelta(days=+3)
        c = yes_time.strftime('%Y %m %d').split()
        res = "{}月{}日".format(c[1],c[2])
    elif label =='未来一周':
        res = label
    return res

def get_precise_date(month,day):
    if month in trans_month.keys():
        month = trans_month.get(month)
    if day in trans_day.keys():
        day = trans_day.get(day)
    return month+day

def get_special_item(special_item):
    if special_item in trans_special.keys():
        special_item = trans_special.get(special_item)
    return special_item

def show_weather_information(date,res):
    out = "------------------------------------------\n"
    if res ==[]:
        out+="不好意思，暂时还没有当前数据\n"
        return out
    if date == get_time("今天"):
        out += "location:" + res[0][1] + "\t\tdate:" + res[0][0] + "\t\tweek:" + res[0][2] + "\n"
        out += "weather:" + res[0][4] + "\t\thigh_temp:" + res[0][5] + "\t\tlow_temp:" + res[0][6] + "\n"
        out += "last_update_time:" + res[1][1]+"\t\t"
        out += "AQI:" + res[1][2] + "\t\tPM2.5:" + res[1][3] + "\t\tPM10:" + res[1][4] + "\n"
        out += "CO:" + res[1][5] + "\t\tNO2:" + res[1][6] + "\t\tSO2:" + res[1][7] + "\t\tO3:" + res[1][8] + "\n"
        out += "humidty:" + res[1][9] + "\t\twind:" + res[1][10] + "\t\twind_inten:" + res[1][11] + "\t\tultra_ray:" + res[1][12] + "\n"
    else:
        for row in res:
            out+="location:"+row[1]+"\t\tdate:"+row[0]+"\t\tweek:"+row[2]+"\n"
            out += "weather:" + row[4] + "\t\thigh_temp:" + row[5] + "\t\tlow_temp:" + row[6] + "\n\n\n"
    out += "------------------------------------------\n"
    return out

def show_special_item(sp_item,res):
    out = "------------------------------------------\n"
    if res ==[]:
        out+="不好意思，暂时还没有当前数据\n"
        return out
    for row in res:
        if sp_item == 'wind' or sp_item == 'wind_inten':
            out += "special_item:" + sp_item + "\t\twind:" + row[0] +"\t\twind_inten:" + row[1] +  "\n\n"
        else:
            out+="special_item:"+sp_item+"\t\tvalue:"+row[0]+"\n\n"
    out += "------------------------------------------\n"
    return out

def show_pollution(res):
    out = "------------------------------------------\n"
    if res ==[]:
        out+="不好意思，暂时还没有当前数据\n"
        return out
    for row in res:
        out+="location:"+row[0]+"\t\tlast_update_time:"+row[1]+"\n"
        out += "AQI:" + row[2] + "\t\tPM2.5:" + row[3] + "\t\tPM10:" + row[4] + "\n"
        out += "CO:" + row[5] + "\t\tNO2:" + row[6] + "\t\tSO2:" + row[7] + "\t\tO3:" + row[8]+"\n"
    out += "------------------------------------------\n"
    return out

if __name__ == '__main__':
    wea_db_path = './db_data/weather.db'
    cursor = get_weather_db(wea_db_path)
    date = "今天"
    # special_item = "CO"
    location = "上海"
    # res = select_pollution(cursor,location)
    # res = select_special_item(cursor,special_item,location)
    res = select_blurry_weather(cursor,get_time(date),location)
    print(res)

    print(show_weather_information(get_time(date),res))
    # print(show_special_item(special_item,res))

