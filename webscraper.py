# scrapes procyclingstats.com results page
# source: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# source: automatetheboringstuff ch.11
# Note: all BeautifulSoup output is unicode. This is why there are 'u' characters
# in front of output. It's okay

import webbrowser, sys
import requests
import bs4
from bs4 import BeautifulSoup
import re


def equal_length(a,b,c,d,e):
    return len(a) == len(b) == len(c) == len(d) == len(e)


# empty list to populate each rider's details
rider_rank = []
rider_country = []
rider_name = []
rider_team = []
rider_time = []

# open files for test writing
rider_rank_txt = open('C:\Users\Kevin\Desktop\webscraper\_rank.txt', 'w')
rider_country_txt = open('C:\Users\Kevin\Desktop\webscraper\_country.txt', 'w')
rider_name_txt = open('C:\Users\Kevin\Desktop\webscraper\_name.txt', 'w')
rider_team_txt = open('C:\Users\Kevin\Desktop\webscraper\_team.txt', 'w')
rider_time_txt = open('C:\Users\Kevin\Desktop\webscraper\_time.txt', 'w')

url = "http://www.procyclingstats.com/race/Paris-Roubaix_2017"
res = requests.get(url)

# make sure request.get is successful
try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' % (exc))

# use BS4 library to parse into a BeautifulSoup object
data = res.text
soup = BeautifulSoup(data, "html.parser")


# finds all divs with class of result, using regex to find specific div
# use class_ to avoid conflict with python kw 'class'
result_div = soup.find_all("div", class_ = re.compile("^resultdiv show"))


# result_div is a ResultSet object, access the 'tag' object with result_div[0]
# result_div[0].contents is a list of length 2, we want index 1 aka the div class="result"
result_parent = result_div[0].contents[1]


# iterate through the children (each being a Tag object for each rider in results table)
for child in result_parent.children:

    # append the first span that has a string inside
    rider_rank.append(child.span.string)

    # set country to find_all spans, using regex to find flags
    country = child.find_all("span", class_ = re.compile("^flags "))

    # country[0] is a tag object, 'class' will access each class of the span tag, and
    # the index 1 is the two letter country code of the rider; append that
    rider_country.append(country[0]['class'][1])

    # get rider's name similarly, and then append [6:] to chop off 'rider/'
    name = child.find_all(href=re.compile("^rider/"))
    rider_name.append(name[0]['href'][6:])

    # get rider's team similarly
    team = child.find_all(href=re.compile("^team/"))
    rider_team.append(team[0]['href'][5:])

    # and time
    time = child.find_all("span", class_ = "time")
    rider_time.append(time[0].string[1:])


# if all lists are equal (they should be), build a list of lists
if equal_length(rider_rank, rider_country, rider_name, rider_team, rider_time):
    full_results = []

    for ix in range(len(rider_rank)):
        full_results.append([rider_rank[ix],rider_country[ix],rider_name[ix],rider_team[ix],rider_time[ix]])

    for element in full_results:
        print element



# write each list to corresponding text file for checking
# rider_rank_txt.write(str(rider_rank))
# rider_country_txt.write(str(rider_country))
# rider_name_txt.write(str(rider_name))
# rider_team_txt.write(str(rider_team))
# rider_time_txt.write(str(rider_time))

rider_rank_txt.close()
rider_country_txt.close()
rider_name_txt.close()
rider_team_txt.close()
rider_time_txt.close()
