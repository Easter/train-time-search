#coding=utf-8
import requests
import json
from bs4 import BeautifulSoup

def get_Trainid():
    headers = {
        "Accept-Language": "zh-CN,zh;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }

    result = requests.get(url="http://www.jt2345.com/huoche/checi", headers=headers)
    html = result.text.encode("ISO-8859-1")
    soup = BeautifulSoup(html.decode("gbk"),"html.parser")
    columns = soup.find("center")
    results = columns.find("table").find_all("tr")

    del results[0].contents[0]
    del results[644].contents[-1]

    for result in results:
        get_Info(result)

def get_Info(result):

    for i in result:

        href = "http://www.jt2345.com" + i.find("a").attrs["href"]

        train_name_info = {
            "id":i.string,
            "href":href,
        }

        all_trains.append(train_name_info)

if __name__ == '__main__':
    all_trains = []
    get_Trainid()
    print(all_trains)

    jsObj = json.dumps(all_trains, ensure_ascii=False, indent=4)
    fileObject = open("G:\软件工程课程设计\全国高铁信息\高铁代号信息.json", "w", encoding="utf-8")
    fileObject.write(jsObj)
    fileObject.close()