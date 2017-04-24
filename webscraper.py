# scrape a webpage
# source: https://automatetheboringstuff.com/chapter11/

import webbrowser, sys
import requests
import bs4
from bs4 import BeautifulSoup

myFile = open('C:\Users\Kevin\Desktop\myFile.txt', 'w')


url = "http://www.procyclingstats.com/race/Tirreno-Adriatico_2017_Stage_7"

res = requests.get(url)

# make sure request.get is successful
try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' % (exc))

data = res.text

                    #pass in data here
soup = BeautifulSoup(data, "html.parser")
# for link in soup.find_all('a'):
#     myFile.write(link.get('href'))
#
# tag = soup.div
#
# divList = tag['class']
#
# test = len(divList)
# myFile.write(str(test))
#
# for div in divList:
#     myFile.write(div)
#     if div == 'lol':
#         myFile.write('it worked!')

# finds all divs with class of result, use class_ to avoid conflict with python kw class
result_div = soup.find_all("div", class_ = "resultdiv show res170994 subs0")
print len(result_div)

myFile.write(str(result_div))

myFile.close()
