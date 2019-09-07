import json

with open("G:\软件工程课程设计\全国高铁信息\高铁代号信息.json", "r", encoding="utf-8")as jf:

    results = json.load(jf)
    train_ids = []

    for result in results:
        train_ids.append(result["id"])

    with open("D:\软件工程课程设计\全国高铁信息\高铁具体信息.json", "r", encoding="utf-8")as jf:

        all_stations = json.load(jf)
        all_infos = dict(zip(train_ids,all_stations))

        jsObj = json.dumps(all_infos, ensure_ascii=False, indent=4)
        fileObject = open("G:\软件工程课程设计\全国高铁信息\高铁具体信息.json", "w", encoding="utf-8")
        fileObject.write(jsObj)
        fileObject.close()


