import json
import sqlite3
from weather import get_Weather,get_PM25
import time
import datetime
import random
import os

def load_json(path):
    fw = open(path,encoding='utf-8').read()
    js = json.loads(fw)
    return js


def create_dataDB(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    sql_weather = '''
            CREATE TABLE IF NOT EXISTS weather(
            date text,
            city_name text,
            week text,
            city_pinyin text,
            weather text,
            high_temp text,
            low_temp text,
            primary key (date,city_name)
            )'''

    sql_pm = '''
            CREATE TABLE IF NOT EXISTS pm(
            city text,
            date text,
            AQI text,
            PM25 text,
            PM10 text,
            CO text,
            NO2 text,
            SO2 text,
            O3 text,
            humidty text,
            wind text,
            wind_inten text,
            ultra_ray text,
            primary key(city)
            )'''
    cursor.execute(sql_weather)
    cursor.execute(sql_pm)
    cursor.close()
    print("database has created!")

def insert_weatherdata(conn,cursor,data):
    try:
        for i in range(len(data)):
            cursor.execute(
                '''
                    replace into weather
                                    (date,
                                    city_name,
                                    week,
                                    city_pinyin,
                                    weather,
                                    high_temp,
                                    low_temp)
                    values
                        ('{}','{}','{}','{}','{}','{}','{}')
                '''.format(
                                data[i][0]['日期'],
                                data[i][0]['城市'],
                                data[i][0]['星期'],
                                data[i][0]['拼音'],
                                data[i][0]['天气'],
                                data[i][0]['最高气温'],
                                data[i][0]['最低气温']
                            )
            )
    except Exception as e:
        print(e)

def insert_PMdata(conn,cursor,data):
    try:
        cursor.execute(
                '''
                    replace into pm
                                (city,
                                date,
                                AQI,
                                PM25,
                                PM10,
                                CO,
                                NO2,
                                SO2,
                                O3,
                                humidty,
                                wind,
                                wind_inten,
                                ultra_ray)
                    values
                        ('{}','{}','{}','{}','{}',
                        '{}','{}','{}','{}','{}',
                        '{}','{}','{}')
                '''.format(
                                data.get("city"),
                                data.get("date"),
                                data.get("AQI"),
                                data.get('PM25'),
                                data.get('PM10'),
                                data.get('CO'),
                                data.get('NO2'),
                                data.get('SO2'),
                                data.get('O3'),
                                data.get('humidty'),
                                data.get('wind'),
                                data.get('wind_inten'),
                                data.get('ultra_ray'),
                            )
            )
    except Exception as e:
        print(e)



def get_yesterday_date():
    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-1)
    c = yes_time.strftime('%Y %m %d').split()
    res = "{}月{}日".format(c[1], c[2])
    return res

def delete_yesterday(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    date = get_yesterday_date()
    cursor.execute('DELETE FROM weather WHERE date="{}"'.format(date))
    conn.commit()
    cursor.close()
    print("{}-昨日天气数据已经清空！".format(datetime.datetime.now()))

def get_randomtime():
    return random.randint(2, 3)



def update_weatherDB(time_now,path,city):
    try:
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        weather_all = []
        for i in range(len(city)):
            res = get_Weather(city[i]['pinyin'].lower(),city[i]['name'])
            weather_all.append(res)
            time.sleep(get_randomtime())
            print("已抓城市/所有城市：{}/{}".format(i + 1, len(city)))

        #print(weather_all)
        for item in weather_all:
            insert_weatherdata(conn, cursor, item)

        conn.commit()
        cursor.close()
    except Exception as e:
        print("{}时报错：{}".format(time_now, e))

def update_PM25(time_now,path,city):
    try:
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        weather_all = []
        for i in range(len(city)):
            res = get_PM25(city[i]['pinyin'].lower(),city[i]['name'])
            weather_all.append(res)
            time.sleep(get_randomtime())
            print("已抓城市/所有城市：{}/{}".format(i + 1, len(city)))

        for item in weather_all:
            insert_PMdata(conn, cursor, item)

        conn.commit()
        cursor.close()
    except Exception as e:
        print("{}时报错：{}".format(time_now,e))


def get_current_hour():
    now_time = datetime.datetime.now()

    hour = now_time.strftime('%Y %m %d %H %M %S').split()[3]
    return now_time,hour




def Main():
    sleep_hour = 3600
    path = 'weather.db'
    js = load_json('city_test.json')

    if not os.path.exists(path):
        create_dataDB(path)

    while True:
        time_now,hour = get_current_hour()
        print("当前时间{}".format(time_now))

        if hour == '09':
            print('{}:{}点的天气数据已经开始更新'.format(time_now, hour))
            update_weatherDB(time_now,path,js)
            delete_yesterday(path)
            print('{}:{}点的天气数据已经全部更新'.format(time_now,hour))

        elif hour == '09' or hour == '16' :
            print('{}:{}点的空气数据已经开始更新'.format(time_now, hour))
            update_PM25(time_now,path,js)
            print('{}:{}点的空气数据已经全部更新'.format(time_now, hour))

        else:
            print('{}:{}点无数据更新'.format(time_now, hour))

        time.sleep(sleep_hour)


if __name__ == '__main__':
    Main()




    # while True:
    #     time_now =
    # conn = sqlite3.connect(path)
    # cursor = conn.cursor()
    # # delete_yesterday(path)
    # weather_all = []
    # data_all = []
    #
    # for i in range(len(js)):
    #         res = get_Weather(js[i]['pinyin'].lower(),js[i]['name'])
    #         weather_all.append(res)
    #         time.sleep(get_randomtime())
    #
    #         res = get_PM25(js[i]['pinyin'].lower(),js[i]['name'])
    #         data_all.append(res)
    #         time.sleep(get_randomtime())
    #
    #         print("已抓城市/所有城市：{}/{}".format(i+1,len(js)))
    #
    # for item in weather_all:
    #     insert_weatherdata(conn,cursor, item)
    # for item in data_all:
    #     insert_PMdata(conn,cursor, item)
    #
    # conn.commit()
    # cursor.close()
    #
    # print("done!")
    #delete_yesterday(path)