import sys

import pymysql
from PyQt5.QtWidgets import QWidget,QApplication,QToolTip,QPushButton,QMessageBox,QDesktopWidget,QMainWindow,\
    QLabel,QHBoxLayout,QVBoxLayout,QLineEdit,QInputDialog,QTableWidget,QTableWidgetItem,QComboBox

from PyQt5.QtCore import QCoreApplication
from PyQt5.Qt import QLineEdit,QStringListModel,QCompleter
from PyQt5.QtSql import QSqlDatabase

from PyQt5.QtGui import QIcon,QFont

conn = pymysql.connect(host='localhost', port=3306, user='bforta', password='p@$$word', db='train')

search_table_station = """
select train_id,stop_station1,stop_station2,stop_station3,stop_station4,stop_station5,stop_station6,stop_station7,stop_station8,stop_station from example
"""

search_table_train = """
select * from example
"""

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.okButton = QPushButton("查询")
        self.cancelButton = QPushButton("退出")

        hbox = QHBoxLayout() # 水平布局
        hbox.addStretch(1) # 伸展因子
        hbox.addWidget(self.okButton) # 添加按钮
        hbox.addWidget(self.cancelButton) # 添加按钮


        vbox = QVBoxLayout() # 垂直布局
        vbox.addStretch(1)

        vbox.addLayout(hbox)

        self.cancelButton.clicked.connect(QCoreApplication.instance().quit)

        self.setLayout(vbox)

        self.lbl1 = QLabel("起始地",self)
        self.lbl1.resize(self.lbl1.sizeHint())
        self.lbl1.move(50,20)

        self.lbl2 = QLabel("目的地",self)
        self.lbl2.resize(self.lbl1.sizeHint())
        self.lbl2.move(300,20)

        self.textbox1 = QLineEdit(self)
        self.textbox1.move(50,40)
        self.textbox1.resize(self.textbox1.sizeHint())

        self.textbox2 = QLineEdit(self)
        self.textbox2.move(300,40)
        self.textbox2.resize(self.textbox2.sizeHint())

        self.okButton.clicked.connect(self.search)
        # self.cancelButton.clicked.connect(self.cancel)

        self.combobox = QComboBox(self)
        self.combobox.move(50, 400)
        self.combobox.addItem("出发最早")
        self.combobox.addItems(["出发最晚","时长最短"])
        self.combobox.hide()


        self.setGeometry(300, 300, 1000, 500)
        self.setWindowTitle('高铁动车查询')
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self,"Message","Are you sure to exit",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        self.conn.close()

    def search(self):
        # print(1)
        start = self.textbox1.text()
        stop = self.textbox2.text()
        print("正在搜索")
        print(start)
        print(stop)
        import json
        with conn.cursor() as cursor:
            with open("G:\软件工程课程设计\全国高铁信息\高铁车站出发信息.json","r",encoding="utf-8") as jf:
                results = json.load(jf)
                stations = list(results.keys())
                # print(stations)
                if start in stations:
                    sql = search_table_station.replace("example", start)
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    train_list = []
                    for trains in results:
                        # print(trains)
                        if stop in trains:
                            train_list.append(trains[0])
                    if len(train_list) == 0:
                        # print("没有从" + start + "到" + stop + "的高铁动车")
                        self.stop_no_train(start,stop)
                            # pass
                        # for station_train in trains:
                        #     print(station_train)
                        #     if stop in station_train:
                        #         train_list.append(trains[0])
                    travels = []
                    for train in train_list:
                        sql = search_table_train.replace("example",train)
                        cursor.execute(sql)
                        results = cursor.fetchall()

                        travel = {}
                        for train_station in results:
                            if start in train_station:
                                train_id = train_station[1]
                                start_station = train_station[2]
                                start_time = train_station[4]
                            if stop in train_station:
                                arrival_time = train_station[3]
                                time_start = start_time.split(":")
                                time_arrival = arrival_time.split(":")
                                # print(time_start)
                                # print(time_arrival)
                                time_total = []

                                if int(time_start[0])<=int(time_arrival[0]) and int(time_start[1])<int(time_arrival[1]):

                                    time_total.append(int(time_arrival[0])-int(time_start[0]))
                                    time_total.append(int(time_arrival[1])-int(time_start[1]))
                                if int(time_start[0])<=int(time_arrival[0]) and int(time_start[1])>int(time_arrival[1]):

                                    time_total.append(int(time_arrival[0]) - int(time_start[0]) - 1)
                                    time_total.append(int(time_arrival[1]) - int(time_start[1]) + 60)

                                if int(time_start[0])>int(time_arrival[0]) and int(time_start[1])<int(time_arrival[1]):
                                    time_total.append(int(time_arrival[0]) - int(time_start[0]) + 24)
                                    time_total.append(int(time_arrival[1]) - int(time_start[1]))
                                if int(time_start[0])>int(time_arrival[0]) and int(time_start[1])>int(time_arrival[1]):
                                    time_total.append(int(time_arrival[0]) - int(time_start[0]) + 24 -1)
                                    time_total.append(int(time_arrival[1]) - int(time_start[1]) + 60)
                                else:pass
                                total_time = "{}:{}".format(time_total[0],time_total[1])
                                travel = {
                                    "train_id":train_id,
                                    "start_station":start_station,
                                    "start_time":start_time,
                                    "arrival_time":arrival_time,
                                    "stop":stop,
                                    "total_time":total_time
                                }
                        travels.append(travel)

                    self.show_trains(travels)

                else:
                    self.station_no_train(start)

    def show_trains(self,travels):

        self.tableWidget = QTableWidget(self)  # 创建一个表格
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.move(50, 100)
        self.tableWidget.resize(700, 250)

        self.tableWidget.setRowCount(len(travels))
        self.tableWidget.setColumnCount(6)

        self.tableWidget.setHorizontalHeaderLabels(['列车', '出发站', '出发时间', '到达时间', '到达站','总时长'])

        if self.combobox.currentText() == "出发最早":
            start_times = []
            for travel in travels:
                start_time = travel["start_time"].split(":")
                start_time = int(start_time[0] + start_time[1])
                start_times.append(start_time)
            time_time = dict(zip(range(len(travels)), start_times))
            # start_times = list(time_time.values())
            # start_times.sort()
            results = sorted(time_time.items(), key=lambda item: item[1],reverse=False)
            sort_time = []
            for result in results:
                sort_time.append(result[0])

            for result in results:
                list = []
                list.append(travels[result[0]]["train_id"])
                list.append(travels[result[0]]["start_station"])
                list.append(travels[result[0]]["start_time"])
                list.append(travels[result[0]]["arrival_time"])
                list.append(travels[result[0]]["stop"])
                list.append(travels[result[0]]["total_time"])
                for info in list:
                    self.tableWidget.setItem(sort_time.index(result[0]), list.index(info), QTableWidgetItem(info))



        elif self.combobox.currentText() == "出发最晚":
            start_times = []
            for travel in travels:
                start_time = travel["start_time"].split(":")
                start_time = int(start_time[0] + start_time[1])
                start_times.append(start_time)
            time_time = dict(zip(range(len(travels)), start_times))

            results = sorted(time_time.items(), key=lambda item: item[1], reverse=True)
            sort_time = []
            for result in results:
                sort_time.append(result[0])

            for result in results:
                list = []
                list.append(travels[result[0]]["train_id"])
                list.append(travels[result[0]]["start_station"])
                list.append(travels[result[0]]["start_time"])
                list.append(travels[result[0]]["arrival_time"])
                list.append(travels[result[0]]["stop"])
                list.append(travels[result[0]]["total_time"])
                for info in list:
                    self.tableWidget.setItem(sort_time.index(result[0]), list.index(info), QTableWidgetItem(info))

        elif self.combobox.currentText() == "时长最短":
            start_times = []
            for travel in travels:
                start_time = travel["total_time"].split(":")
                start_time = int(start_time[0] + start_time[1])
                start_times.append(start_time)
            time_time = dict(zip(range(len(travels)), start_times))

            results = sorted(time_time.items(), key=lambda item: item[1], reverse=False)
            sort_time = []
            for result in results:
                sort_time.append(result[0])

            for result in results:
                list = []
                list.append(travels[result[0]]["train_id"])
                list.append(travels[result[0]]["start_station"])
                list.append(travels[result[0]]["start_time"])
                list.append(travels[result[0]]["arrival_time"])
                list.append(travels[result[0]]["stop"])
                list.append(travels[result[0]]["total_time"])
                for info in list:
                    self.tableWidget.setItem(sort_time.index(result[0]), list.index(info), QTableWidgetItem(info))
        self.combobox.show()
        self.tableWidget.show()

    def choose_soft(self,combobox_current_index,travels):
        print("已经被调用")
        print(combobox_current_index)
        if combobox_current_index == 0:
            start_times = []
            for travel in travels:
                start_time = travel["start_time"].split(":")
                start_time = int(start_time[0] + start_time[1])
                start_times.append(start_time)
            time_time = dict(zip(range(len(travels)),start_times))

            results = sorted(time_time.items(),key= lambda item:item[1])
            sort_time = []
            for result in results:
                sort_time.append(result[0])


            for result in results:
                list = []
                list.append(travels[result[0]]["train_id"])
                list.append(travels[result[0]]["start_station"])
                list.append(travels[result[0]]["start_time"])
                list.append(travels[result[0]]["arrival_time"])
                list.append(travels[result[0]]["stop"])
                for info in list:
                    self.tableWidget.setItem(sort_time.index(result[0]), list.index(info), QTableWidgetItem(info))
            self.tableWidget.show()

    def cancel(self):
        self.show()

    def station_no_train(self,start):
        self.tableWidget.hide()
        # if self.tableWidget:
        #     self.tableWidget.hide()
        self.lable = QLabel(start + "车站无高铁经过",self)
        self.lable.move(50,100)
        self.lable.resize(self.lable.sizeHint())
        self.lable.show()

    def stop_no_train(self,start,stop):
        self.tableWidget.hide()
        self.lable = QLabel("没有从" + start + "到" + stop + "的高铁动车",self)
        self.lable.move(50,100)
        self.lable.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    # ex.show()
    sys.exit(app.exec_())
