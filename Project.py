import sys

import calendar
import sqlite3

from PIL.ImageQt import ImageQt
from PIL import Image
from PyQt5.QtCore import QSize, QSettings
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QTableWidgetItem, QAbstractItemView
from geopy.exc import GeocoderTimedOut

from AppWindow import Ui_MainWindow
from HistoryOfRequests import Ui_Form
from Settings import Ui_Form as Ui_Form2

from datetime import datetime
from geopy import geocoders
from tzwhere import tzwhere
from pytz import timezone

KEY = 'settings1'
KEY2 = 'settings2'


class Application(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Application, self).__init__()
        self.setupUi(self)
        self.ToExecute.clicked.connect(self.run)
        self.ToHistoryOfRequests.clicked.connect(self.open_history)
        self.to_settings_btn.clicked.connect(self.open_settings)
        self.geocoder = None
        self.town = None
        self.name_of_timezone = None
        self.object_of_timezone = None
        self.local_datetime = None
        self.list = []
        self.str_local_date = None
        self.str_local_time = None
        self.dop_info = None
        self.image = None
        self.pixmap = None
        self.part_of_the_world = None
        self.country = None
        self.subject = None
        self.con = sqlite3.connect('History_of_requests_BD.db')
        self.cur = self.con.cursor()

        self.w2 = HistoryOfRequests()
        self.w3 = Settings()
        self.to_settings_btn.setIcon(QIcon('icon.jpg'))
        self.to_settings_btn.setIconSize(QSize(62, 28))
        self.to_settings_btn.setStyleSheet('background: rgb(255,255,255);')
        if self.w3.comboBox.currentText() == 'Design 1':
            self.setStyleSheet("#MainWindow{border-image:url(bg.jpg)}")
        elif self.w3.comboBox.currentText() == 'Design 2':
            self.setStyleSheet("#MainWindow{border-image:url(bg2.jpg)}")
        else:
            self.setStyleSheet("#MainWindow{border-image:url(bg3.jpg)}")

    def run(self):
        self.statusbar.clearMessage()
        try:
            self.town = self.Input.text()
            self.geocoder = geocoders.Photon()
            place, coordinates = self.geocoder.geocode(self.town, language="en")
            self.dop_info = place.split(', ')
            print(self.dop_info)
            time_zone_definition = tzwhere.tzwhere()  # определитель таймзоны
            self.name_of_timezone = time_zone_definition.tzNameAt(coordinates[0],
                                                                  coordinates[1])  # таймзона в текстовом виде
            self.part_of_the_world = self.name_of_timezone.split('/')[0]
            self.object_of_timezone = timezone(self.name_of_timezone)
            self.local_datetime = datetime.now(self.object_of_timezone)
            self.str_local_date = self.local_datetime.date().strftime('%d %Y')
            self.list = self.str_local_date.split()
            self.str_local_date = calendar.month_name[self.local_datetime.month] + ' ' + \
                                  self.list[0] + ', ' + self.list[1]
            self.str_local_time = self.local_datetime.time().strftime('%H:%M')
            self.OutputWindow.setText(f'City/Town: {self.town}. Now: {self.str_local_date}; {self.str_local_time}')
            self.country = self.dop_info[-1]
            try:
                if str(self.dop_info[-2]).isdigit():
                    raise SubjectCountryError
                self.subject = self.dop_info[-2]
            except (IndexError, SubjectCountryError):
                self.subject = 'Not Found'
            self.Country.setText(f'Country: {self.country}')
            self.SubjetOFtheCountry.setText(f'Subject of the country: {self.subject}')

            try:
                self.image = Image.open(f'./flags/{self.country}.png')
                self.pixmap = QPixmap.fromImage(ImageQt(self.image))
                self.Flag.setPixmap(self.pixmap)
                self.Flag.setScaledContents(True)
            except FileNotFoundError:
                self.Flag.setText('Flag not found')

            self.cur.execute("""INSERT INTO countries(country) VALUES(?)""", (self.country,))
            self.cur.execute("""INSERT INTO parts_of_the_world(part_of_the_world) 
                                    VALUES(?)""", (self.part_of_the_world,))
            self.cur.execute("""INSERT INTO tzs(tz) VALUES(?)""", (self.name_of_timezone,))
            self.cur.execute("""INSERT INTO main(city_town, country, 
                part_of_the_world, tz) VALUES(?, (SELECT id FROM countries WHERE country = (?)),
                    (SELECT id FROM parts_of_the_world WHERE part_of_the_world = (?)),
                    (SELECT id FROM tzs WHERE tz = (?)))""", (self.town.capitalize(), self.country,
                                                              self.part_of_the_world, self.name_of_timezone))
            self.con.commit()
        except (GeocoderTimedOut, TypeError):
            self.statusbar.showMessage('Invalid value entered')

    def open_history(self):
        self.w2.show()

    def open_settings(self):
        self.w3.show()

    def keyPressEvent(self, event):
        if event.key() in (16777220, 16777221):
            self.run()

    def closeEvent(self, event):
        if self.w3.checkBox.isChecked():
            self.cur.execute("""DELETE FROM main""")
            self.cur.execute("""UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'main'""")
            self.con.commit()


class HistoryOfRequests(QWidget, Ui_Form):
    def __init__(self):
        super(HistoryOfRequests, self).__init__()
        self.setupUi(self)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # отключение редактирования ячеек таблицы
        self.get_info.clicked.connect(self.get_inf)
        self.clear.clicked.connect(self.clear_inf)
        self.tableWidget.cellClicked.connect(self.show_val)
        self.con = sqlite3.connect('History_of_requests_BD.db')
        self.cur = self.con.cursor()
        self.quantity = 0
        self.result = None
        self.titles = None
        self.headline = None

    def get_inf(self):
        self.result = self.cur.execute("""SELECT * FROM main""").fetchall()
        if not self.result:
            self.statusbar.setText('History is empty')
            self.tableWidget.clearContents()
            return
        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.setColumnCount(len(self.result[0]))
        self.titles = [description[0] for description in self.cur.description]
        self.tableWidget.setHorizontalHeaderLabels(self.titles)
        self.quantity = self.cur.execute("""SELECT COUNT(*) FROM main""").fetchone()[0]
        self.tableWidget.setVerticalHeaderLabels(['' for i in range(self.quantity + 1)])
        for i, elem in enumerate(self.result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.result = None

    def clear_inf(self):
        self.cur.execute("""DELETE FROM main""")
        self.cur.execute("""UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'main'""")
        self.con.commit()
        self.get_inf()

    def show_val(self, row, col):
        self.headline = self.tableWidget.horizontalHeaderItem(col).text()
        try:
            if self.headline == 'id' or self.headline == 'city_town':
                pass
            elif self.headline == 'country':
                self.result = self.cur.execute("""SELECT country 
                FROM countries WHERE id = ?""", (int(self.tableWidget.item(row, col).text()),))
            elif self.headline == 'part_of_the_world':
                self.result = self.cur.execute("""SELECT part_of_the_world 
                            FROM parts_of_the_world WHERE id = ?""", (int(self.tableWidget.item(row, col).text()),))
            elif self.headline == 'tz':
                self.result = self.cur.execute("""SELECT tz 
                                        FROM tzs WHERE id = ?""", (int(self.tableWidget.item(row, col).text()),))
        except ValueError:
            pass
        if self.result:
            self.result = list(self.result)
            self.tableWidget.setItem(row, col, QTableWidgetItem(self.result[0][0]))
            self.result = None


class Settings(QWidget, Ui_Form2):
    def __init__(self):
        super(Settings, self).__init__()
        self.setupUi(self)
        self.settings_checkb = QSettings()
        self.settings_combob = QSettings()
        self.checkBox.clicked.connect(self.change_checkbox_settings)
        self.comboBox.addItems(['Design 1', 'Design 2', 'Design 3'])
        self.comboBox.currentIndexChanged.connect(self.change_combobox_settings)
        with open('state_cb.txt', encoding='utf-8') as file:
            if file.read() == 'False':
                self.state_checkb = self.settings_checkb.value(KEY, False, type=bool)
            else:
                self.state_checkb = self.settings_checkb.value(KEY, True, type=bool)
            self.checkBox.setChecked(self.state_checkb)
        with open('state_combob.txt', encoding='utf-8') as file2:
            self.state_combob = self.settings_combob.value(KEY2, file2.read(), type=str)
            self.comboBox.setCurrentText(self.state_combob)

    def change_checkbox_settings(self):
        with open('state_cb.txt', 'w', encoding='utf-8') as file:
            file.write(str(self.checkBox.isChecked()))

    def change_combobox_settings(self):
        with open('state_combob.txt', 'w', encoding='utf-8') as file:
            file.write(str(self.comboBox.currentText()))


class SubjectCountryError(Exception):
    pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w1 = Application()
    w1.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
