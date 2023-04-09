from APIModule import getLists, getCities
from PyQt6 import QtWidgets,QtGui, QtCore, sip
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox
from PyQt6.QtCore import QTimer
from PyQt6.uic import loadUi
from enum import Enum
import resources
import sys
import datetime
import os


WINDOW_HEIGHT = 478
WINDOW_WIDTH = 692
PATH = os.path.join("dark_icons","icon.png")
INDEX_HOME = 0
INDEX_SEARCH = 1
INDEX_WEATHER = 2
DARK_MODE = 0
INFO_TEXT = """Prognoza Pogody\n\n
Jest to aplikacja okienkowa z interfejsem graficznym, która umożliwia sprawdzenie prognozy pogody na kolejne siedem dni. Możliwe jest wyszukanie, 
a następnie wybór z listy miejscowośći, która interesuje użytkownika. Po nakliknięciu pojawi się nazwa miejscowości w prawym górnym rogu wraz z 
aktualnym czasem. Poniżej wyświetlana jest prognoza pogody dla każdego dnia w formie kafelków z intuicyjnie dobraną grafiką. Każdy kafelek umożliwia 
sprawdzenie temperatury dla odpowiedniej godziny za pomocą scrolla. Możliwe jest również przesuwanie się między dniami za pomocą strzałek. Aplikacja 
pozwala także na korzystanie z trybu ciemnego.\n\n
Autor: Natalia Brzózka"""

class Week(Enum):
    Niedziela = 0
    Poniedziałek = 1
    Wtorek = 2
    Środa = 3
    Czwartek = 4
    Piątek = 5
    Sobota = 6   

WeatherCode = {
    "0": "clear_sky.png",
    "1": "mainly_clear.png",
    "2": "mainly_clear.png",
    "3": "mainly_clear.png",
    "45": "fog.png",
    "48": "fog.png",
    "51": "rain.png",
    "53": "rain.png",
    "55": "rain.png",
    "56": "rain.png",
    "57": "rain.png",
    "61": "rain.png",
    "63": "rain.png",
    "65": "rain.png",
    "66": "rain.png",
    "67": "rain.png",
    "80": "rain.png",
    "81": "rain.png",
    "82": "rain.png",
    "71": "snow.png",
    "73": "snow.png",
    "75": "snow.png",
    "77": "snow.png",
    "85": "snow.png",
    "86": "snow.png",
    "95": "thunder.png",
    "96": "thunder.png",
    "99": "thunder.png"
}


def DarkMode():
    global DARK_MODE
    if DARK_MODE:
        for i in range(INDEX_WEATHER + 1):
            stackedWidget.widget(i).setStyleSheet('background-color: rgb(232, 232, 232);'
                                                  'color: rgb(0, 0, 0);')
            stackedWidget.widget(i).graphicsView.setStyleSheet('border-image: url(:/czarne/dark_icons/dark_mode.png) 0 0 0 0 stretch stretch;'
                                                               'background-repeat: no-repeat;')
            stackedWidget.widget(i).checkBox.setChecked(False)
        stackedWidget.widget(INDEX_WEATHER).graphicsView_2.setStyleSheet('border-image: url(:/czarne/dark_icons/location_on.png)')
        stackedWidget.widget(INDEX_WEATHER).pushButton_2.setStyleSheet('border-image: url(:/czarne/dark_icons/arrow_circle_left.png)')
        stackedWidget.widget(INDEX_WEATHER).pushButton_3.setStyleSheet('border-image: url(:/czarne/dark_icons/arrow_circle_right.png)')

        DARK_MODE = 0
    else:
        for i in range(INDEX_WEATHER + 1):
            stackedWidget.widget(i).setStyleSheet('background-color: rgb(35, 32, 57);'
                                                  'color: rgb(255, 255, 255);')
            stackedWidget.widget(i).graphicsView.setStyleSheet('border-image: url(:/biale/icons_white/dark_mode.png) 0 0 0 0 stretch stretch;'
                                                               'background-repeat: no-repeat;')
            stackedWidget.widget(i).checkBox.setChecked(True)
        stackedWidget.widget(INDEX_WEATHER).graphicsView_2.setStyleSheet('border-image: url(:/biale/icons_white/location_on.png)')
        stackedWidget.widget(INDEX_WEATHER).pushButton_2.setStyleSheet('border-image: url(:/biale/icons_white/arrow_circle_left.png)')
        stackedWidget.widget(INDEX_WEATHER).pushButton_3.setStyleSheet('border-image: url(:/biale/icons_white/arrow_circle_right.png)')
        DARK_MODE = 1

def displayInfo():
    msg = QMessageBox()
    msg.setWindowTitle("O Aplikacji")
    msg.setText(INFO_TEXT)
    x = msg.exec()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("landing_page.ui",self)
        self.pushButton.clicked.connect(self.Search)
        self.checkBox.clicked.connect(DarkMode)
        self.actionO_aplikacji.triggered.connect(displayInfo)

    def Search(self):
        inputLocation = self.lineEdit.text()
        cityList, countryList = getCities(inputLocation)
        stackedWidget.widget(INDEX_SEARCH).passingInformation(cityList, countryList, inputLocation)
        stackedWidget.setCurrentIndex(INDEX_SEARCH)


class SearchWindow(QMainWindow):
    def __init__(self):
        super(SearchWindow,self).__init__()
        loadUi("search_page.ui",self)
        self.pushButton.clicked.connect(self.Search)
        self.cityList, self.countryList = [], []
        self.listView.clicked[QtCore.QModelIndex].connect(self.on_clicked)
        self.checkBox.clicked.connect(DarkMode)
        self.actionO_aplikacji.triggered.connect(displayInfo)
        
    def passingInformation(self, cityList, countryList, inputLocation):
        self.lineEdit.setText(inputLocation)
        self.cityList = cityList
        self.countryList = countryList
        self.Display()

    def Search(self):
        inputLocation = self.lineEdit.text()
        self.cityList, self.countryList = getCities(inputLocation)
        self.Display()

    def SearchWeather(self, name):
        self.weatherWindow = WeatherWindow()
        daysTemperature, daysCodes = getLists(name)
        stackedWidget.widget(INDEX_WEATHER).passingInformation(daysTemperature, daysCodes, name)
        stackedWidget.setCurrentIndex(INDEX_WEATHER)

    def Display(self):
        self.model = QtGui.QStandardItemModel()
        self.listView.setModel(self.model)
        for (i, j) in zip(self.cityList, self.countryList):
            item = QtGui.QStandardItem(f"{i} ({j})")
            item.setEditable(False)
            self.model.appendRow(item)

    def on_clicked(self, index):
        item = self.model.itemFromIndex(index)
        self.SearchWeather(item.text().split(" (")[0])


class WeatherWindow(QMainWindow):
    def __init__(self):
        super(WeatherWindow,self).__init__()
        loadUi("wheather_page.ui",self)
        self.pushButton.clicked.connect(self.goToSearchPage)
        self.daysTemperature, self.daysCodes = [], []
        self.checkBox.clicked.connect(DarkMode)
        self.offSet = 0
        self.pushButton_2.clicked.connect(self.clickLeft)
        self.pushButton_3.clicked.connect(self.clickRight)
        self.actionO_aplikacji.triggered.connect(displayInfo)

    def passingInformation(self, daysTemperature, daysCodes, name):
        self.offSet = 0
        self.daysTemperature = daysTemperature
        self.daysCodes = daysCodes
        self.lineEdit.setText("")
        self.label_2.setText(name)
        self.startTimer()
        self.displayWeather()

    def goToSearchPage(self):
        inputLocation = self.lineEdit.text()
        cityList, countryList = getCities(inputLocation)
        stackedWidget.widget(INDEX_SEARCH).passingInformation(cityList, countryList, inputLocation)
        stackedWidget.setCurrentIndex(INDEX_SEARCH)

    def startTimer(self):
        self.updateTime()
        timer = QTimer(self)
        timer.timeout.connect(self.updateTime)
        timer.setInterval(1000)
        timer.start()

    def updateTime(self):
        currentTime = datetime.datetime.now().strftime('%H:%M')
        self.label_3.setText(currentTime)

    def displayWeather(self):
        dayOfTheWeek = datetime.datetime.now().isoweekday()
        currenthour = int(datetime.datetime.now().strftime('%H'))
        if self.offSet == 0:
            self.day_1.setText('Dzisiaj')
            self.temp_1.setText(str(self.daysTemperature[0][currenthour-1]) + '°')
            self.graphicsView_3.setStyleSheet(f'border-image: url(images/{WeatherCode[f"{self.daysCodes[0][currenthour-1]}"]})')
            self.day_2.setText('Jutro')
        else:
            self.day_1.setText(Week((dayOfTheWeek+self.offSet)%7).name)
            self.temp_1.setText(str(self.daysTemperature[0+self.offSet][11]) + '°')
            self.graphicsView_3.setStyleSheet(f'border-image: url(images/{WeatherCode[f"{self.daysCodes[0+self.offSet][11]}"]})')
            self.day_2.setText(Week((dayOfTheWeek+self.offSet+1)%7).name)
        self.day_3.setText(Week((dayOfTheWeek+self.offSet+2)%7).name)  
        self.temp_2.setText(str(self.daysTemperature[1+self.offSet][11]) + '°')
        self.temp_3.setText(str(self.daysTemperature[2+self.offSet][11]) + '°')
        self.graphicsView_4.setStyleSheet(f'border-image: url(images/{WeatherCode[f"{self.daysCodes[1+self.offSet][11]}"]})')
        self.graphicsView_5.setStyleSheet(f'border-image: url(images/{WeatherCode[f"{self.daysCodes[2+self.offSet][11]}"]})')
        self.displayTemperature()

    def displayTemperature(self):
        self.clearLayouts()
        layoutDay1 = QHBoxLayout()
        layoutDay2 = QHBoxLayout()
        layoutDay3 = QHBoxLayout()
        for j in range(24):
            layout1 = QVBoxLayout()
            layout2 = QVBoxLayout()
            layout3 = QVBoxLayout()
            if j < 10:
                layout1.addWidget(QLabel(f"0{j}:00"))
                layout2.addWidget(QLabel(f"0{j}:00"))
                layout3.addWidget(QLabel(f"0{j}:00"))
            else:
                layout1.addWidget(QLabel(f"{j}:00"))
                layout2.addWidget(QLabel(f"{j}:00"))
                layout3.addWidget(QLabel(f"{j}:00"))
            layout1.addWidget(QLabel(str(self.daysTemperature[0+self.offSet][j]) + '°'))
            layout2.addWidget(QLabel(str(self.daysTemperature[1+self.offSet][j]) + '°'))
            layout3.addWidget(QLabel(str(self.daysTemperature[2+self.offSet][j]) + '°'))
            layoutDay1.addLayout(layout1)
            layoutDay2.addLayout(layout2)
            layoutDay3.addLayout(layout3)
        self.frame.setLayout(layoutDay1)
        self.frame_2.setLayout(layoutDay2)
        self.frame_3.setLayout(layoutDay3)
         
    def deleteLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.deleteLayout(item.layout())
            sip.delete(layout)

    def clearLayouts(self):
        self.deleteLayout(self.frame.layout())
        self.deleteLayout(self.frame_2.layout())
        self.deleteLayout(self.frame_3.layout())

    def clickRight(self):
        self.offSet = (self.offSet + 1)%5
        self.displayWeather()
    
    def clickLeft(self):
        self.offSet = (self.offSet - 1)%5
        self.displayWeather()


app = QApplication(sys.argv)
stackedWidget = QtWidgets.QStackedWidget()
mainwindow = MainWindow()
searchWindow = SearchWindow()
weatherWindow = WeatherWindow()
stackedWidget.setWindowTitle("Prognoza Pogody")
stackedWidget.setWindowIcon(QtGui.QIcon(PATH))
stackedWidget.addWidget(mainwindow)
stackedWidget.addWidget(searchWindow)
stackedWidget.addWidget(weatherWindow)
stackedWidget.setFixedWidth(WINDOW_WIDTH)
stackedWidget.setFixedHeight(WINDOW_HEIGHT)
stackedWidget.show()
sys.exit(app.exec())