import json

import random
def find_all_station():

    with open("D:\软件工程课程设计\全国高铁信息\高铁具体信息.json" ,"r",encoding="utf-8") as jf:
        results = json.load(jf)

        for stations in results:

            for station in stations:
                train_station = station["train_station"]

                if train_station in all_stations.keys():
                    all_stations[train_station].append(station["station_id"])
                else:
                    all_stations[train_station] = [station["station_id"]]

def find_max_time():
    times = []
    with open("G:\软件工程课程设计\全国高铁信息\高铁具体信息.json" ,"r",encoding="utf-8") as jf:
        results = json.load(jf)

        for train in results.keys():
            times.append(len(results[train]))

    return min(times)


def handle_data():

    all_Infos = {}

    for station in all_stations.keys():
        all_Infos[station] = {}

    for station in all_Infos.keys():

        for results in all_stations[station]:
            all_Infos[station][results] = []

    with open("G:\软件工程课程设计\全国高铁信息\高铁具体信息.json", "r", encoding="utf-8") as jf:

        results = json.load(jf)
        for station_start in all_Infos:

            for train in all_Infos[station_start]:
                stations = []

                if len(results[train]) > 10:
                    pass

                else:
                    for station_info in results[train]:

                        stations.append(station_info["train_station"])

                    for station in stations:

                        if station == station_start:
                            i = stations.index(station)

                            for n in stations[i:]:
                                all_Infos[station_start][train].append(n)

    for station in all_Infos:
        for train in list(all_Infos[station].keys()):
            if len(all_Infos[station][train]) <= 1:
                del all_Infos[station][train]
            else:pass
    times = []

    for station in list(all_Infos.keys()):
        if len(all_Infos[station]) == 0:
            del all_Infos[station]

    for station in list(all_Infos.keys()):
       if len(all_Infos[station]) == 0:
            print(station)

    for station in list(all_Infos.keys()):

        for train in all_Infos[station].keys():
            times.append(len(all_Infos[station][train]))

    print(max(times))

    return all_Infos

if __name__ == '__main__':
    all_stations = {}
    find_all_station()

    all_Infos = handle_data()

    print(all_Infos)

    jsObj = json.dumps(all_Infos, ensure_ascii=False, indent=4)
    fileObject = open("G:\软件工程课程设计\全国高铁信息\高铁车站出发信息.json", "w", encoding="utf-8")
    fileObject.write(jsObj)
    fileObject.close()