from APIModule import getLists, getCities
import gi
import threading
import time
import datetime
from enum import Enum
import sys
from gi.repository.GdkPixbuf import Pixbuf
gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk, Gdk, GdkPixbuf

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

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.add(Gtk.Label(label=data, xalign=0))

class Handler:
    def __init__(self):
        self.cityList, self.countryList, self.daysTemperature, self.daysCodes = [], [], [], []
        self.timer = True
        self.darkModeOn = True
        self.offSet = 0

    def onDestroy(self, *args): 
        self.timer = False
        Gtk.main_quit()

    def darkMode(self, button):
        if (self.darkModeOn):
            css = b"""
            window, button, #listbox {
                background-color: rgb(35, 32, 57);
                color: rgb(255, 255, 255);
            }
            #listbox {
                border: 1px solid white;
            }
            #textBlack {
                color: rgb(0, 0, 0);
            }
            #textBlack1 {
                color: rgb(0, 0, 0);
                background-color: rgb(255, 255, 255);
            }
            """
            builder.get_object("darkmode1").set_from_pixbuf(Pixbuf.new_from_file("icons_white/dark_mode.png"))
            builder.get_object("darkmode2").set_from_pixbuf(Pixbuf.new_from_file("icons_white/dark_mode.png"))
            builder.get_object("darkmode3").set_from_pixbuf(Pixbuf.new_from_file("icons_white/dark_mode.png"))
            builder.get_object("locationimage").set_from_pixbuf(Pixbuf.new_from_file("icons_white/location_on.png"))
            builder.get_object("toggleimage1").set_from_pixbuf(Pixbuf.new_from_file("icons_white/toggle_on.png"))
            builder.get_object("toggleimage2").set_from_pixbuf(Pixbuf.new_from_file("icons_white/toggle_on.png"))
            builder.get_object("toggleimage3").set_from_pixbuf(Pixbuf.new_from_file("icons_white/toggle_on.png"))
            builder.get_object("rightimage").set_from_pixbuf(Pixbuf.new_from_file("icons_white/arrow_circle_right.png"))
            builder.get_object("leftimage").set_from_pixbuf(Pixbuf.new_from_file("icons_white/arrow_circle_left.png"))
            self.darkModeOn = False
        else:
            css = b"""
            window, button, #listbox {
                background-color: rgb(232, 232, 232);
                color: rgb(0, 0, 0); 
            }
            #listbox {
                border: 1px solid black;
            }
            """
            builder.get_object("darkmode1").set_from_pixbuf(Pixbuf.new_from_file("dark_icons/dark_mode.png"))
            builder.get_object("darkmode2").set_from_pixbuf(Pixbuf.new_from_file("dark_icons/dark_mode.png"))
            builder.get_object("darkmode3").set_from_pixbuf(Pixbuf.new_from_file("dark_icons/dark_mode.png"))
            builder.get_object("locationimage").set_from_pixbuf(Pixbuf.new_from_file("dark_icons/location_on.png"))
            builder.get_object("toggleimage1").set_from_pixbuf(Pixbuf.new_from_file("dark_icons/toggle_off.png"))
            builder.get_object("toggleimage2").set_from_pixbuf(Pixbuf.new_from_file("dark_icons/toggle_off.png"))
            builder.get_object("toggleimage3").set_from_pixbuf(Pixbuf.new_from_file("dark_icons/toggle_off.png"))
            builder.get_object("rightimage").set_from_pixbuf(Pixbuf.new_from_file("dark_icons/arrow_circle_right.png"))
            builder.get_object("leftimage").set_from_pixbuf(Pixbuf.new_from_file("dark_icons/arrow_circle_left.png"))
            self.darkModeOn = True
        provider.load_from_data(css)

    def searchCitiesMain(self, button):
        inputLocation = builder.get_object("search1").get_text()
        self.searchCities(inputLocation)
        mainWindow.hide()
        searchWindow.show()
        
    def searchCitiesWeather(self, button):
        inputLocation = builder.get_object("search3").get_text()
        self.searchCities(inputLocation)
        weatherWindow.hide()
        searchWindow.show()
        
    def searchCitiesSearch(self, button):
        inputLocation = builder.get_object("search2").get_text()
        self.searchCities(inputLocation)
        
    def searchCities(self, inputLocation):
        self.cityList, self.countryList = getCities(inputLocation)
        builder.get_object("search2").set_text(inputLocation)
        self.displayCities()

    def displayCities(self):
        self.clearListbox()
        for (i, j) in zip(self.cityList, self.countryList):
            item = str(f"{i} ({j})")
            listbox.add(ListBoxRowWithData(item))
        listbox.show_all()

    def infoButtonClicked(self, button):
        infoWindow.show()

    def infoOkClicked(self, button, *args):
        infoWindow.hide()
        return True
    
    def chooseCity(self, list, row):
        if row:# is not None and " (" in row.data:
            city = row.data.split(" (")[0]
            self.searchWeather(city)
            builder.get_object("citytext").set_text(city)
        self.displayWeather()
        
    def displayWeather(self):
        searchWindow.hide()
        self.startTimer()
        weatherWindow.show()
        builder.get_object("search3").set_text(""),
        builder.get_object("citytext").set_xalign(1)
        dayOfTheWeek = datetime.datetime.now().isoweekday()
        currenthour = int(datetime.datetime.now().strftime('%H'))
        if self.offSet == 0:
            builder.get_object("day1").set_text('Dzisiaj')
            builder.get_object("temp1").set_text(str(self.daysTemperature[0][currenthour-1]) + '°')
            image1 = Pixbuf.new_from_file(f'images/{WeatherCode[f"{self.daysCodes[0][currenthour-1]}"]}')
            
            builder.get_object("day2").set_text('Jutro')
        else:
            builder.get_object("day1").set_text(Week((dayOfTheWeek+self.offSet)%7).name)
            builder.get_object("temp1").set_text(str(self.daysTemperature[0+self.offSet][11]) + '°')
            image1 = Pixbuf.new_from_file(f'images/{WeatherCode[f"{self.daysCodes[0+self.offSet][11]}"]}')
            builder.get_object("day2").set_text(Week((dayOfTheWeek+self.offSet+1)%7).name)
        image2 = Pixbuf.new_from_file(f'images/{WeatherCode[f"{self.daysCodes[1+self.offSet][11]}"]}')
        image3 = Pixbuf.new_from_file(f'images/{WeatherCode[f"{self.daysCodes[2+self.offSet][11]}"]}')
        image1 = image1.scale_simple(251, 288, GdkPixbuf.InterpType.BILINEAR)
        image2 = image2.scale_simple(251, 288, GdkPixbuf.InterpType.BILINEAR)
        image3 = image3.scale_simple(251, 288, GdkPixbuf.InterpType.BILINEAR)
        builder.get_object("Image1").set_from_pixbuf(image1)
        builder.get_object("Image2").set_from_pixbuf(image2)
        builder.get_object("Image3").set_from_pixbuf(image3)
        builder.get_object("day3").set_text(Week((dayOfTheWeek+self.offSet+2)%7).name)  
        builder.get_object("temp2").set_text(str(self.daysTemperature[1+self.offSet][11]) + '°')
        builder.get_object("temp3").set_text(str(self.daysTemperature[2+self.offSet][11]) + '°')
        self.displayTemperature()

    def displayTemperature(self):
        self.clearBoxes()
        box1 = builder.get_object("box1")
        box2 = builder.get_object("box2")
        box3 = builder.get_object("box3")
        box1.set_size_request(800, 20)
        box2.set_size_request(800, 20)
        box3.set_size_request(800, 20)
        for j in range(24):
            boxV1 = Gtk.VBox()
            boxV2 = Gtk.VBox()
            boxV3 = Gtk.VBox()
            if j < 10:
                time1 = Gtk.Label(label=f"0{j}:00")
                time2 = Gtk.Label(label=f"0{j}:00")
                time3 = Gtk.Label(label=f"0{j}:00")
            else:
                time1 = Gtk.Label(label=f"{j}:00")
                time2 = Gtk.Label(label=f"{j}:00")
                time3 = Gtk.Label(label=f"{j}:00")
            temp1 = Gtk.Label(label=str(self.daysTemperature[0+self.offSet][j]) + '°')
            temp2 = Gtk.Label(label=str(self.daysTemperature[1+self.offSet][j]) + '°')
            temp3 = Gtk.Label(label=str(self.daysTemperature[2+self.offSet][j]) + '°')
            boxV1.pack_start(time1, True, True, 0)
            boxV1.pack_start(temp1, True, True, 0)
            boxV2.pack_start(time2, True, True, 0)
            boxV2.pack_start(temp2, True, True, 0)
            boxV3.pack_start(time3, True, True, 0)
            boxV3.pack_start(temp3, True, True, 0)
            box1.add(boxV1)
            box2.add(boxV2)
            box3.add(boxV3)
        box1.show_all()
        box2.show_all()
        box3.show_all()
            
    def clearBoxes(self):
        box1 = builder.get_object("box1")
        box2 = builder.get_object("box2")
        box3 = builder.get_object("box3")
        for (i, j, k) in zip(box1.get_children(), box2.get_children(), box3.get_children()):
            box1.remove(i)
            box2.remove(j)
            box3.remove(k)
            
    def rightClick(self, button):
        self.offSet = (self.offSet + 1)%5
        self.displayWeather()

    def leftClick(self, button):
        self.offSet = (self.offSet - 1)%5
        self.displayWeather()

    def startTimer(self):
        thread = threading.Thread(target=self.updateTime)
        thread.daemon = True
        thread.start()

    def updateTime(self):
        while(self.timer):    
            currentTime = datetime.datetime.now().strftime('%H:%M')
            builder.get_object("timetext").set_text(currentTime)
            time.sleep(10)

    def searchWeather(self,name):
        self.daysTemperature, self.daysCodes = getLists(name)

    def clearListbox(self):
        children = listbox.get_children()
        for child in children:
	        listbox.remove(child)


    
builder = Gtk.Builder()
builder.add_from_file("widgetyGTK.glade")
builder.connect_signals(Handler())
screen = Gdk.Screen.get_default()
provider = Gtk.CssProvider()
style_context = Gtk.StyleContext()
style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
mainWindow = builder.get_object("main_window")
searchWindow = builder.get_object("search_window")
weatherWindow = builder.get_object("weather_window")
infoWindow = builder.get_object("infodialog")
listbox = builder.get_object("searchList")
mainWindow.show()

Gtk.main()


# cityName = input("City: ")
# daysLists, codesLists = getLists(cityName)