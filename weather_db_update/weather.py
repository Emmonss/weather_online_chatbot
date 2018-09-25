import urllib.request
import re
import urllib.error
import time
from bs4 import BeautifulSoup

headers=("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36")
opener = urllib.request.build_opener()
opener.addheaders=[headers]

def get_PM25(city):
    try:
        #天气网站地址
        url = "http://pm25.in/"+city
        data = urllib.request.urlopen(url).read().decode("utf-8")
        # print("城市：{}".format(city))

        data_time = '<div class="live_data_time">\s{1,}<p>数据更新时间：(.*?)</p>'
        datatime = re.compile(data_time, re.S).findall(data)

        #先爬PM2.5的
        data_pm25 = '<div class="span1">\s{1,}<div class="value">\n\s{1,}(.*?)\s{1,}</div>'
        data_o3 = '<div class="span1">\s{1,}<div class ="value">\n\s{1,}(.*?)\s{1,}</div>'
        pm25list = re.compile(data_pm25, re.S).findall(data)
        o3list = re.compile(data_o3, re.S).findall(data)
        pm25list.append(o3list[0])

        #再爬一些单日数据
        url = 'https://www.tianqi.com/{}/'.format(city)
        data = urllib.request.urlopen(url).read().decode("utf-8")
        soup = BeautifulSoup(data, 'html.parser')
        li_shidu = soup.find('dd',attrs={'class':'shidu'}).find_all('b')

        #数据保存
        pm_list = {"AQI": pm25list[0]+"μg/m3", "PM25": pm25list[1]+"μg/m3", "PM10": pm25list[2]+"μg/m3", "CO": pm25list[3]+"mg/m3", "NO2": pm25list[4]+"μg/m3",
                   "SO2": pm25list[5]+"μg/m3", "O3": pm25list[6]+"μg/m3",
                   "humidty": li_shidu[0].string.split("：")[1],
                   "wind": li_shidu[1].string.split("：")[1].split()[0],
                   "wind_inten": li_shidu[1].string.split("：")[1].split()[1],
                   "ultra_ray": li_shidu[2].string.split("：")[1],
                   "date": datatime[0]}
        return pm_list
    except urllib.error.URLError as e:
        print("出现URLERROR！一分钟后重试……")
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        time.sleep(60)
    except Exception as e:
        print(e)
        time.sleep(5)

def get_Weather(city):
    try:
        weatherlist = []
        url='https://www.tianqi.com/{}/'.format(city)
        data=urllib.request.urlopen(url).read().decode("utf-8")
        soup = BeautifulSoup(data,'html.parser')

        li_date = soup.find('ul',attrs={'class':'week'}).find_all('li')
        li_shidu = soup.find('dd', attrs={'class': 'shidu'}).find_all('b')
        li_weather = soup.find('ul', attrs={'class': 'txt txt2'}).find_all('li')
        li_temp = soup.find('div', attrs={'class': 'zxt_shuju'}).find('ul').find_all('li')
        for i in range (len(li_weather)):
            slot = [];
            slot.append({'日期': li_date[i].find('b').string,'星期': li_date[i].find('span').string,'天气':li_weather[i].string,'最高气温': li_temp[i].find('span').string+"℃",'最低气温': li_temp[i].find('b').string+"℃"})
            weatherlist.append(slot)
        return weatherlist

    except urllib.error.URLError as e:
        print("出现URLERROR！一分钟后重试……")
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
        time.sleep(60)
        # get_Weather(city)
    except Exception as e:
        print("Exception："+str(e))
        # time.sleep(10)

def get_all_attr(city):
    res = get_PM25(city)
    # get_Weather(city)

if __name__ == '__main__':
    get_all_attr("hefei")

