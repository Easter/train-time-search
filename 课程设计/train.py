import json
import requests
from bs4 import BeautifulSoup

def get_info():

    with open("G:\软件工程课程设计\全国高铁信息\高铁代号信息.json","r",encoding="utf-8") as jf:
        results = json.load(jf)

    urls = []

    for result in results:
        urls.append(result["href"])

    for url in urls[:]:
        parse_url(url)


def parse_url(url):

    headers = {
        "Accept-Language": "zh-CN,zh;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }

    results = requests.get(url)
    html = results.text.encode("ISO-8859-1")
    soup = BeautifulSoup(html.decode("gbk"),"html.parser")
    tables = soup.find_all("table")
    infos = tables[0].find_all("tr")
    stations = tables[1].find_all("tr")
    train_id = infos[0].find_all("td")[2].string

    del stations[0]
    # parse_html(infos)

    parse(stations,train_id)

# def parse_html(infos):
#     train_id = infos[0].find_all("td")[2].string
#     model = infos[1].find_all("td")[1].string
#     start = infos[2].find_all("td")[1].string
#     start_time = infos[3].find_all("td")[1].string
#     stop_time = infos[4].find_all("td")[1].string
#     total_time = infos[5].find_all("td")[1].string
#     stop = infos[6].find_all("td")[1].string
#
#     train = {
#         "train_id": train_id,
#         "model": model,
#         "start": start,
#         "start_time": start_time,
#         "stop_time": stop_time,
#         "total_time": total_time,
#         "stop": stop
#     }
#     print(train)
#     general_trains.append(train)

def parse(stations,station_id):

    train_info = []

    for station in stations:

        train_time = station.find_all("td")[0].string
        train_station = station.find_all("td")[1].string
        arrival_time = station.find_all("td")[2].string
        driving_time = station.find_all("td")[3].string
        residence_time = station.find_all("td")[4].string

        train_times = {
            "station_id": station_id,
            "train_time": train_time,
            "train_station": train_station,
            "arrival_time": arrival_time,
            "driving_time": driving_time,
            "residence_time": residence_time
        }

        train_info.append(train_times)

    print(train_info)

    train_all_infos.append(train_info)

if __name__ == '__main__':

    general_trains = []
    train_all_infos = []

    get_info()
    # print(general_trains)
    print(train_all_infos)
    # jsObj = json.dumps(general_trains, ensure_ascii=False, indent=4)
    # fileObject = open("G:\软件工程课程设计\全国高铁信息\高铁全程信息.json", "w", encoding="utf-8")
    # fileObject.write(jsObj)
    # fileObject.close()
    jsObj = json.dumps(train_all_infos, ensure_ascii=False, indent=4)

    fileObject = open("G:\软件工程课程设计\全国高铁信息\高铁具体信息.json", "w", encoding="utf-8")
    fileObject.write(jsObj)
    fileObject.close()
