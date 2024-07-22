import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QTableWidgetItem
import pyqtgraph as pg
from parsamd import parse_amd
from parsbaba import parse_baba
from parsapple import parse_apple
from parsanystock import parse_any
import sqlite3
import time
from parscrypt import parse_crypt


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('wind.ui', self)
        # self.pushButton.clicked.connect(self.run)
        self.con = sqlite3.connect("svdb.db", check_same_thread=False)
        self.pushButton_4.clicked.connect(self.run)
        self.pushButton_10.clicked.connect(self.upd_amd)
        self.pushButton_11.clicked.connect(self.upd_baba)
        self.pushButton_9.clicked.connect(self.upd_apple)

        self.pushButton_16.clicked.connect(self.upd_any)
        self.pushButton_13.clicked.connect(self.upd_any_bd)
        self.pushButton_14.clicked.connect(self.do_graph_any)
        self.pushButton_15.clicked.connect(self.clear_bd_any)
        # --------crypt
        self.pushButton_20.clicked.connect(self.upd_crypt)
        self.pushButton_19.clicked.connect(self.upd_crypt_bd)
        self.pushButton_17.clicked.connect(self.do_graph_crypt)
        self.pushButton_18.clicked.connect(self.clear_bd_crypt)
        # --------crypt
        self.pushButton.clicked.connect(self.do_graph_amd)
        self.pushButton_2.clicked.connect(self.do_graph_baba)
        self.pushButton_3.clicked.connect(self.do_graph_apple)
        # ---------
        self.pushButton_7.clicked.connect(self.clear_bd_amd)
        self.pushButton_6.clicked.connect(self.clear_bd_baba)
        self.pushButton_5.clicked.connect(self.clear_bd_apple)
        # --------
        self.pushButton_8.clicked.connect(self.clear_all_bd)
        self.cur = self.con.cursor()
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.plotWdgt = pg.PlotWidget()
        data, tata = [2, 5, 5, 2, 2, 5, 8, 10], [1, 1, 4, 4, 7, 7, 1, 7]
        self.plot_item = self.plotWdgt.plot(data, tata)

        self.pushButton_12.clicked.connect(self.update_result)
        self.modified = {}
        self.titles = None

        self.proxy_widget = self.scene.addWidget(self.plotWdgt)
        self.sql = "INSERT INTO stocks (name, price, time) VALUES (?, ?, ?)"

    def run(self):
        self.progressBar.setValue(0)
        self.lineEdit.setText(parse_amd())
        self.progressBar.setValue(33)
        self.lineEdit_2.setText(parse_baba())
        self.progressBar.setValue(66)
        self.lineEdit_3.setText(parse_apple())
        self.progressBar.setValue(100)
        # print(self.lineEdit.text())

    def upd_amd(self):
        self.progressBar.setValue(0)
        self.lineEdit.setText(parse_amd())
        self.progressBar.setValue(33)
        self.cur.execute(self.sql, ["amd", float(self.lineEdit.text().replace(',', '.')), int(time.time())])
        self.progressBar.setValue(66)
        self.con.commit()
        self.progressBar.setValue(100)

    def upd_baba(self):
        self.progressBar.setValue(0)
        self.lineEdit_2.setText(parse_baba())
        self.progressBar.setValue(33)
        self.cur.execute(self.sql, ["baba", float(self.lineEdit_2.text().replace(',', '.')), int(time.time())])
        self.progressBar.setValue(66)
        self.con.commit()
        self.progressBar.setValue(100)

    def upd_apple(self):
        self.progressBar.setValue(0)
        self.lineEdit_3.setText(parse_apple())
        self.progressBar.setValue(33)
        self.cur.execute(self.sql, ["apple", float(self.lineEdit_3.text().replace(',', '.')), int(time.time())])
        self.progressBar.setValue(66)
        self.con.commit()
        self.progressBar.setValue(100)

    def upd_any(self):
        self.progressBar.setValue(0)
        if 'https://ru.investing.com/equities/' in self.lineEdit_5.text() and parse_any(
                self.lineEdit_5.text()) != 'error':
            self.label_6.setText('')
            self.progressBar.setValue(50)
            self.lineEdit_4.setText(parse_any(self.lineEdit_5.text()))
            self.progressBar.setValue(100)
            self.name_of_any = self.lineEdit_5.text()[34:]
            self.label_4.setText(f'{self.name_of_any}')
            self.price_of_any = parse_any(self.lineEdit_5.text())
            # print(self.price_of_any)
        else:
            self.label_6.setText('Неверная ссылка')

    def upd_crypt(self):
        self.progressBar.setValue(0)
        if 'https://ru.investing.com/crypto/' in self.lineEdit_7.text() and parse_crypt(
                self.lineEdit_7.text()) != 'error':
            self.label_9.setText('')
            self.progressBar.setValue(50)
            self.lineEdit_6.setText(parse_crypt(self.lineEdit_7.text()))
            self.progressBar.setValue(100)
            self.name_of_crypt = self.lineEdit_7.text()[32:]
            self.label_7.setText(f'{self.name_of_crypt}')
            self.price_of_crypt = parse_crypt(self.lineEdit_7.text())
            # print(self.price_of_any)
        else:
            self.label_9.setText('Неверная ссылка')

    def upd_any_bd(self):
        self.lineEdit_4.setText(parse_any(self.lineEdit_5.text()))
        if '.' in self.lineEdit_4.text():
            pr = self.lineEdit_4.text().replace('.', '').replace(',', '.')
        else:
            pr = self.lineEdit_4.text().replace(',', '.')
        self.cur.execute(self.sql,
                         [f"{self.name_of_any}", float(pr), int(time.time())])
        self.con.commit()

    def upd_crypt_bd(self):
        self.lineEdit_6.setText(parse_crypt(self.lineEdit_7.text()))
        if '.' in self.lineEdit_6.text():
            pr = self.lineEdit_6.text().replace('.', '').replace(',', '.')
        else:
            pr = self.lineEdit_6.text().replace(',', '.')
        self.cur.execute(self.sql,
                         [f"{self.name_of_crypt}", float(pr),
                          int(time.time())])
        self.con.commit()

    def do_txt_browser(self, mas_x, mas_y):
        max_price = max(mas_x)
        min_price = min(mas_x)
        if mas_x[-1] >= mas_x[0]:
            dinam = 'положительная | рост:'
            prcnt = round((mas_x[-1] - mas_x[0])/mas_x[0] * 100, 5)
        else:
            dinam = 'отрицательная | падение:'
            prcnt = round(-((mas_x[-1] - mas_x[0]) / mas_x[0] * 100), 5)
        begin_time = time.ctime(min(mas_y))
        end_time = time.ctime(max(mas_y))
        timings = ''
        n = 0
        for item in mas_x:
            timings += str(item) + '|' + str(time.ctime(mas_y[n])) + '--->'
            n += 1
            if n % 3 == 0:
                timings += '\n'
        n = 0
        self.textBrowser.setText(f'''        max price: {max_price}
                min price: {min_price}
                динамика: {dinam} {prcnt}%
                Период времени
                с: {begin_time} |цена в этот момент {mas_x[0]}
                по: {end_time} |цена в этот момент {mas_x[-1]}
                Значения в вершинах со временем(цена|время):
                {timings}''')

    def do_graph_crypt(self):
        self.plotWdgt.close()
        self.plotWdgt = pg.PlotWidget()
        res = list(self.cur.execute(f"""SELECT price, time FROM stocks WHERE name="{self.name_of_crypt}" """))
        mas_x = []
        mas_y = []
        for i in res:
            if i[0] not in mas_y:
                mas_y.append(i[0])
                mas_x.append(i[1])
        print(res)
        self.plot_item = self.plotWdgt.plot(mas_x, mas_y)
        self.proxy_widget = self.scene.addWidget(self.plotWdgt)
        # ------------
        self.do_txt_browser(mas_y, mas_x)

    def do_graph_any(self):
        self.plotWdgt.close()
        self.plotWdgt = pg.PlotWidget()
        res = list(self.cur.execute(f"""SELECT price, time FROM stocks WHERE name="{self.name_of_any}" """))
        mas_x = []
        mas_y = []
        for i in res:
            if i[0] not in mas_y:
                mas_y.append(i[0])
                mas_x.append(i[1])
        print(res)
        self.plot_item = self.plotWdgt.plot(mas_x, mas_y)
        self.proxy_widget = self.scene.addWidget(self.plotWdgt)
        # ------------
        self.do_txt_browser(mas_y, mas_x)

    def clear_bd_any(self):
        self.cur.execute(f'DELETE from stocks where name="{self.name_of_any}"')
        self.con.commit()

    def do_graph_amd(self):
        self.plotWdgt.close()
        self.plotWdgt = pg.PlotWidget()
        res = list(self.cur.execute("""SELECT price, time FROM stocks WHERE name="amd" """))
        mas_x = []
        mas_y = []
        for i in res:
            if i[0] not in mas_y:
                mas_y.append(i[0])
                mas_x.append(i[1])
        # print(res)
        self.plot_item = self.plotWdgt.plot(mas_x, mas_y)
        self.proxy_widget = self.scene.addWidget(self.plotWdgt)
        # ------------
        self.do_txt_browser(mas_y, mas_x)

    def do_graph_baba(self):
        self.plotWdgt.close()
        self.plotWdgt = pg.PlotWidget()
        res = list(self.cur.execute("""SELECT price, time FROM stocks WHERE name="baba" """))
        mas_x = []
        mas_y = []
        for i in res:
            if i[0] not in mas_y:
                mas_y.append(i[0])
                mas_x.append(i[1])
        # print(res)
        self.plot_item = self.plotWdgt.plot(mas_x, mas_y)
        self.proxy_widget = self.scene.addWidget(self.plotWdgt)
        # ------------
        self.do_txt_browser(mas_y, mas_x)

    def do_graph_apple(self):
        self.plotWdgt.close()
        self.plotWdgt = pg.PlotWidget()
        res = list(self.cur.execute("""SELECT price, time FROM stocks WHERE name="apple" """))
        mas_x = []
        mas_y = []
        for i in res:
            if i[0] not in mas_y:
                mas_y.append(i[0])
                mas_x.append(i[1])
        # print(res)
        self.plot_item = self.plotWdgt.plot(mas_x, mas_y)
        self.proxy_widget = self.scene.addWidget(self.plotWdgt)
        # ------------
        self.do_txt_browser(mas_y, mas_x)

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = list(cur.execute("SELECT * FROM stocks"))
        # Заполнили размеры таблицы
        # print(list(result))
        self.tableWidget.setRowCount(len(result))
        # Если запись не нашлась, то не будем ничего делать
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        else:
            self.statusBar().showMessage("Нашлась запись с id")
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def clear_bd_amd(self):
        self.cur.execute('DELETE from stocks where name="amd"')
        self.con.commit()

    def clear_bd_baba(self):
        self.cur.execute('DELETE from stocks where name="baba"')
        self.con.commit()

    def clear_bd_apple(self):
        self.cur.execute('DELETE from stocks where name="apple"')
        self.con.commit()

    def clear_all_bd(self):
        self.cur.execute('DELETE from stocks where time > 0')
        self.con.commit()

    def clear_bd_crypt(self):
        self.cur.execute(f'DELETE from stocks where name="{self.name_of_crypt}"')
        self.con.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
