#library 
import request3                                                            #http pip requests
from bs4 import BeautifulSoup                                               #scrape website
from win10toast_click import ToastNotifier                                       #notif win10


#create object notif to class
n = ToastNotifier()

#define function
def getdata(url):
    r = request3.get(url)
    return r.text
#scraping website
htmldata = getdata("https://weather.com/weather/today/l/8608d9458c3c5a2be69f0fa015ec036b93432cfed3dc4a2cc44e239e3cda011f")        

soup = BeautifulSoup(htmldata, 'lxml')                                                   #change html parser to lxml

#find detail from scrapimg and filler it

current_temp = soup.find_all("span",
							class_=" _-_-components-src-organism-CurrentConditions-CurrentConditions--tempValue--MHmYY")
chances_rain = soup.find_all("div",
							class_= "_-_-components-src-organism-CurrentConditions-CurrentConditions--precipValue--2aJSf")

temp = (str(current_temp))
temp_rain = str(chances_rain)

result = "current_temp " + temp[128:-9] + " in Lenggong, Perak" + "\n" +temp_rain[131:-14]


#print out notification window
n.show_toast("live weather update", result, duration = 20)