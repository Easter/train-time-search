import pymysql

import json
import dataframe
import datetime
conn = pymysql.connect(host='localhost', port=3306, user='bforta', passwd='p@$$word', db='train')

create_table_all_train = """\
CREATE TABLE all_train(
train_id varchar(10) PRIMARY KEY,
model VARCHAR(10),
start VARCHAR(20),
start_time varchar(20),
stop_time varchar(20),
total_time varchar(20),
stop varchar(20)
)
"""

with open("G:\软件工程课程设计\全国高铁信息\高铁全程信息.json", "r", encoding="utf-8")as jf:
    results = json.load(jf)

insert_table_all_train = """
INSERT INTO all_train(train_id,model,start,start_time,stop_time,total_time,stop)
  VALUES(%s,%s,%s,%s,%s,%s,%s)
"""

with open("G:\软件工程课程设计\全国高铁信息\高铁全程信息.json", "r", encoding="utf-8")as jf:
    results = json.load(jf)

def insert_to_all_train():

    try:
        with conn.cursor() as cursor:
            # cursor.execute(create_table_all_train)
            for result in results:
                cursor.execute(insert_table_all_train,
                               (result["train_id"], result["model"], result["start"], result["start_time"], result["stop_time"], result["total_time"],
                                result["stop"]))
            conn.commit()

    finally:
        conn.close()


create_table_all_station = """\
create table example(
train_id varchar(10) PRIMARY KEY,
start_station VARCHAR(10),
stop_station1 varchar(10),
stop_station2 varchar(10),
stop_station3 varchar(10),
stop_station4 varchar(10),
stop_station5 varchar(10),
stop_station6 varchar(10),
stop_station7 varchar(10),
stop_station8 varchar(10),
stop_station varchar(10)
)
"""

def create_table():

    with open("G:\软件工程课程设计\全国高铁信息\高铁车站出发信息.json", "r", encoding="utf-8") as jf:
        results = json.load(jf)
        print(results.keys())

        try:
            with conn.cursor() as cursor:
                for station in results.keys():
                    print("create_table" + str(station))
                    sql = create_table_all_station.replace("example",station)
                    cursor.execute(sql)

        finally:
            conn.close()

insert_to_station_tables = """\
INSERT INTO example(train_id,start_station,stop_station1,stop_station2,stop_station3,stop_station4,stop_station5,
stop_station6,stop_station7,stop_station8,stop_station)
  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

def insert_to_station_table(): # 向车站数据库中插入车次数据
    try:
        with conn.cursor() as cursor:
            with open("G:\软件工程课程设计\全国高铁信息\高铁车站出发信息.json", "r", encoding="utf-8") as jf:
                results = json.load(jf)

                for station in results.keys():
                    sql = insert_to_station_tables.replace("example",station)

                    for train in list(results[station].keys()):
                        station_train = []
                        station_train.append(train)

                        if train in results[station]:

                            for station_stop in results[station][train]:
                                station_train.append(station_stop)

                        if len(station_train) < 11:

                            for i in range(11-len(station_train)):
                                station_train.append("null")

                        print(station_train)

                        cursor.execute(sql,(station_train))
                conn.commit()
    finally:
        conn.close()

create_train_table_sql = """\
create table example(
train_time int PRIMARY KEY,
train_id VARCHAR(10),
train_station VARCHAR(10),
arrival_time varchar(10),
driving_time varchar(10),
residence_time varchar(10)
)
"""

def create_table_train():
    try:
        with conn.cursor() as cursor:

            with open("G:\软件工程课程设计\全国高铁信息\高铁具体信息.json", "r", encoding="utf-8") as jf:
                results = json.load(jf)
                # print(results.keys())

                for train in list(results.keys()):
                    sql = create_train_table_sql.replace("example",train)
                    cursor.execute(sql)

            conn.commit()
    finally:
        conn.close()


insert_to_train_table= """\
INSERT INTO example(train_time,train_id,train_station,arrival_time,driving_time,residence_time)
  VALUES(%s,%s,%s,%s,%s,%s)
"""

def insert_to_table_train():
    try:
        with conn.cursor() as cursor:
            with open("G:\软件工程课程设计\全国高铁信息\高铁具体信息.json","r",encoding="utf-8") as jf:
                results = json.load(jf)

                for train in results.keys():
                    for station in results[train]:
                        sql = insert_to_train_table.replace("example",train)
                        list = []
                        list.append(int(station["train_time"]))
                        list.append(station["station_id"])
                        list.append(station["train_station"])
                        list.append(station["arrival_time"])
                        list.append(station["driving_time"])
                        list.append(station["residence_time"])
                        cursor.execute(sql,list)
                        print(list)

            conn.commit()

    finally:
        conn.close()


if __name__ == '__main__':
    # insert_to_all_train()
    # create_table()
    # insert_to_station_table()
    # create_table_train()
    # with open("G:\软件工程课程设计\全国高铁信息\高铁具体信息.json", "r", encoding="utf-8") as jf:
    #     results = json.load(jf)
    #     print(len(results.keys())

    insert_to_table_train()
