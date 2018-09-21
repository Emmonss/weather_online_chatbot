import json
import sqlite3
from weather import get_Weather,get_PM25
import time
import datetime
import random

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

def insert_weatherdata(path,data,cp,cn):
    try:
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
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
                                cn,
                                data[i][0]['星期'],
                                cp,
                                data[i][0]['天气'],
                                data[i][0]['最高气温'],
                                data[i][0]['最低气温']
                            )
            )
        conn.commit()
        cursor.close()
        print("{}一周天气数据已经成功插入！".format(cn))
    except Exception as e:
        print(e)

def insert_PMdata(path,data,cn):
    try:
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
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
                                cn,
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
        conn.commit()
        cursor.close()
        print("{}PM最新数据已经成功插入！".format(cn))
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

if __name__ == '__main__':
    path = 'weather.db'
    js = load_json('city.json')

    # delete_yesterday(path)

    for i in range(len(js)):
            res = get_Weather(js[i]['pinyin'].lower())
            insert_weatherdata(path,res,js[i]['pinyin'],js[i]['name'])

            rest_time = random.randint(2, 5)
            print("休息{}秒数秒防止被封IP".format(rest_time))
            time.sleep(rest_time)

            res = get_PM25(js[i]['pinyin'].lower())
            insert_PMdata(path,res,js[i]['name'])

            rest_time = random.randint(2, 5)
            print("休息{}秒数秒防止被封IP".format(rest_time))
            time.sleep(rest_time)
            print("已抓城市/所有城市：{}/{}/".format(i+1,len(js)))
    delete_yesterday(path)