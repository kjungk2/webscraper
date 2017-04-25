# scrape a webpage
# source: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# source: automatetheboringstuff ch.11

import webbrowser, sys
import requests
import bs4
from bs4 import BeautifulSoup
import re

# empty list to populate each rider's details
rider_rank = []
rider_country = []
rider_name = []
rider_team = []

# open a file to test write to
rider_rank_txt = open('C:\Users\Kevin\Desktop\webscraper\_rank.txt', 'w')
rider_country_txt = open('C:\Users\Kevin\Desktop\webscraper\_country.txt', 'w')
rider_name_txt = open('C:\Users\Kevin\Desktop\webscraper\_name.txt', 'w')
rider_team_txt = open('C:\Users\Kevin\Desktop\webscraper\_team.txt', 'w')

# use requests library to
url = "http://www.procyclingstats.com/race/Tirreno-Adriatico_2017_Stage_7"
res = requests.get(url)

# make sure request.get is successful
try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' % (exc))

# use BS4 library to parse
data = res.text
soup = BeautifulSoup(data, "html.parser")

# finds all divs with class of result, use class_ to avoid conflict with python kw class
class_to_find = re.compile("^resultdiv show")
result_div = soup.find_all("div", class_ = class_to_find)


# result_div is a ResultSet object of length 1;
# result_div[0] is a tag object
# result_div[0].contents is a list of length 2, we want index 1 aka the div class="result"
result_parent = result_div[0].contents[1]

country_to_find = re.compile("^flags ")

# go through child (each being a Tag object)
for child in result_parent.children:
    # append anything within a span tag with string inside
    rider_rank.append(child.span.string)

    # set country to a ResultSet, [0] is a tag object
    country = child.find_all("span", class_ = country_to_find)

    # country[0] is a tag object, 'class' will access each class of the span tag, and
    # the index 1 is the two letter country code of the rider; append that
    rider_country.append(country[0]['class'][1])

    # get rider's name similarly
    name = child.find_all(href=re.compile("^rider/"))
    # append only after the 6th character, effectively chopping off 'rider/'
    rider_name.append(name[0]['href'][6:])

    team = child.find_all(href=re.compile("^team/"))
    rider_team.append(team[0]['href'][5:])

rider_rank_txt.write(str(rider_rank))
rider_country_txt.write(str(rider_country))
rider_name_txt.write(str(rider_name))
rider_team_txt.write(str(rider_team))

# for rider_div in result_parent.contents:
#     print rider_div.next_element.next_element.next_element.next_element
#     print "\n"
#     print "\n"


#myFile.write(str(final))

rider_rank_txt.close()
