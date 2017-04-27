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
import operator


# returns True if 5 elements are of equal length
# use to check if html parsing was done evenly and consistently
def equal_length(a,b,c,d,e):
    return len(a) > 0 and len(a) == len(b) == len(c) == len(d) == len(e)


# takes a URL of type string and returns BeautifulSoup object
def parse_url(url):

    res = requests.get(url)

    # make sure request.get is successful
    try:
        res.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))

    # use BS4 library to parse into a BeautifulSoup object
    data = res.text
    return BeautifulSoup(data, "html.parser")


# function that takes a BeautifulSoup object and empty lists as input
# soup is scraped and desired data is appended to lists
# return a list of lists: [0]=rank, [1]=country, [2]=name, [3]=team, [4]=time
# if changes are made in PCS' markup, then this fn will need to change
def scrape_results_page(soup):

    # empty list to populate each rider's details
    rider_rank = []
    rider_country = []
    rider_name = []
    rider_team = []
    rider_time = []

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

    # if all lists are equal (they should be), build a list of lists and return it
    if equal_length(rider_rank, rider_country, rider_name, rider_team, rider_time):
        full_results = []
        for ix in range(len(rider_rank)):
            full_results.append([rider_rank[ix],rider_country[ix],rider_name[ix],rider_team[ix],rider_time[ix]])
        return full_results

    else:
        print "ERROR: Something went wrong with the results page scrape"


# function that takes a BeautifulSoup object as input
# soup is scraped and desired data is inserted into a dict
# return a dict
# if changes are made in PCS' markup, then this fn will need to change
def scrape_rider_page(soup):
    # finds all divs with class of pbsRow, aka 'points by specialty'
    # use class_ to avoid conflict with python kw 'class'
    pbs_row_div = soup.find_all("div", style = re.compile("^display: inline-block;"))

    rider_discipline_dict = {
        "One-day-races" : pbs_row_div[0].string,
        "GC" : pbs_row_div[2].string,
        "Time-Trialist" : pbs_row_div[4].string,
        "Sprinter" : pbs_row_div[6].string
    }

    return rider_discipline_dict


# takes in a dictionary of GC: xx, Sprinter: xx, etc
# if any of those values are above 0.33333 of total points, that is a discipline for the rider
# returns a list of disciplines that comprise 33% of a rider's total PCS points
def get_discipline(dict):
    points_sum = 0
    for points in dict.values():
        # cast to float so we can get a decimal
        points_sum += float(points)

    # list that will be returned
    discipline_list = []

    # the dict[key] is a NavigableString so cast it to int
    for key in dict.keys():
        discipline_ratio = int(dict[key]) / points_sum
        if discipline_ratio >= 0.33:
            discipline_list.append(key)

    # if list is empty, rider does not have a value > 33% so retur the largest
    if not discipline_list:
        #find the maximum value and return that key, used stackflow for this
        discipline_list.append(max(dict.iteritems(), key=operator.itemgetter(1))[0])
    return discipline_list



# as a test, parse the tour de romandie page, scrape it, get each rider name
# parse that rider's page and get their points by specialty
romandie_stage_1_soup = parse_url('http://www.procyclingstats.com/race.php?id=163735')

# this var is a list of lists
romandie_stage_1_scraped = scrape_results_page(romandie_stage_1_soup)

my_file = open('C:\Users\Kevin\Desktop\webscraper\_rider_dict_romandie_1.txt', 'w')

for sub_list in romandie_stage_1_scraped:

    list_for_file = []

    curr_rider = sub_list[2]
    curr_rider_url = 'http://www.procyclingstats.com/rider/' + curr_rider
    curr_rider_soup = parse_url(curr_rider_url)
    curr_rider_scraped = scrape_rider_page(curr_rider_soup)
    curr_rider_discipline = get_discipline(curr_rider_scraped)

    my_file.write(curr_rider)
    my_file.write(" --- ")

    for element in curr_rider_discipline:
        my_file.write(element + " ")
    my_file.write("\n")
    my_file.write("\n")


my_file.close()
