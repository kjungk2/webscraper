'''
Scrapes procyclingstats.com /race and /rider pages
Docs source: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
MySQL source: https://www.tutorialspoint.com/python/python_database_access.htm
Note: all BeautifulSoup output is unicode. This is why there are 'u' characters
in front of output.
'''

import webbrowser, sys
import requests
import bs4
from bs4 import BeautifulSoup
import re
import operator
import time
import csv
import MySQLdb

#CONSTANTS
PCS_HOME_URL = 'http://www.procyclingstats.com'
CSV_PATH = 'C:\Users\Kevin\Desktop\webscraper'

class Rider(object):
    '''
    Instantiates a rider object.
    Access to:
      raceday, rank, country_code, name, team, time, country_name, discipline
    '''
    def __init__(self, raceday, rank, country_code, name, team, time):
        self.raceday = raceday
        self.rank = rank
        self.country_code = country_code
        self.name = name
        self.team = team
        self.time = time

    def raceday(self):
        return self.raceday

    def rank(self):
        return str(self.rank)

    def country_code(self):
        return self.country_code

    def name(self):
        return self.name

    def team(self):
        return self.team

    def time(self):
        return self.time

	# Returns any discipline/s over 33% of total points by specialty
    def discipline(self):
        # parse rider page to get BeautifulSoup object
        # if PCS' markup changes, then this method will need to change
        soup = (parse_url(PCS_HOME_URL + '/rider/' + self.name))
        pbs_row_div = soup.find_all("div", style = re.compile("^display: inline-block;"))

		# create a discipline dictionary
        disc_dict = {"One-day-races" : pbs_row_div[0].string, "GC" : pbs_row_div[2].string, "Time-Trialist" : pbs_row_div[4].string, "Sprinter" : pbs_row_div[6].string}

		# Iterate through the dictionary to find best discipline/s
        points_sum = 0
        for points in disc_dict.values():
			# cast to float so we can get a decimal
            points_sum += float(points)

		# list that will be returned
        discipline_list = []

		# sets a threshhold, otherwise there is not a sufficient sample of data
        if points_sum < 400:
            discipline_list = ['Inexperienced']
            return discipline_list

        max_value = 0
		# the disc_dict[key] is a NavigableString so cast it to int
        for key in disc_dict.keys():
            discipline_ratio = int(disc_dict[key]) / points_sum
            if discipline_ratio >= 0.33:
                discipline_list.append(key)
            if int(disc_dict[key]) > max_value:
                max_value = disc_dict[key]

		# if list is empty, rider does not have a value > 33% so return the largest
        if not discipline_list:
            #find the maximum value and return that key, used stackflow for this
            discipline_list.append(disc_dict.keys()[disc_dict.values().index(max_value)])

        return discipline_list

def scrape_results_page(soup):
    '''
    Returns a list of lists: [0]=rank, [1]=country, [2]=name, [3]=team, [4]=time
    Requires a BeautifulSoup object, use parse_url function
    if PCS' markup changes, then this function will need to change
    '''
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

def equal_length(a,b,c,d,e):
    '''
    Returns True if 5 elements are of equal length
    To check if html parsing was done evenly and consistently
    '''
    return len(a) > 0 and len(a) == len(b) == len(c) == len(d) == len(e)

def parse_url(url):
    '''
    Returns BeautifulSoup object
    Requires a url of type string
    '''
    res = requests.get(url)

    # make sure request.get is successful
    try:
        res.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))

    # use BS4 library to parse into a BeautifulSoup object
    data = res.text
    return BeautifulSoup(data, "html.parser")

def write_to_csv():
    '''
    Write info to file
    Includes time and counts printed to terminal
    '''
    print '\nWebscraping for ' + raceday.replace('_', ' ') + ' has started...\n'
    start = time.time()
    scraped_results_page = scrape_results_page(parse_url(PCS_HOME_URL + '/race/' + raceday))

    myfile = open(CSV_PATH + '\\race_data.csv', 'w')

    count = 1
    for rider_result_list in scraped_results_page:
        new_rider = Rider(raceday, rider_result_list[0], rider_result_list[1], rider_result_list[2], rider_result_list[3], rider_result_list[4])

        myfile.write(new_rider.raceday)
        myfile.write(',')
        myfile.write(new_rider.rank)
        myfile.write(',')
        myfile.write(new_rider.country_code)
        myfile.write(',')
        myfile.write(new_rider.name)
        myfile.write(',')
        myfile.write(new_rider.team)
        myfile.write(',')
        myfile.write(new_rider.time)
        myfile.write(',')
        myfile.write(str(new_rider.discipline()))
        myfile.write('\n')
        count += 1

    myfile.close()
    end = time.time()
    print '\n' + str(count) + ' records | ' + str(end - start) + ' seconds\n'
    print raceday.replace('_', ' ') + ' results have been written to file.'

def load_csv_to_table():

    db = MySQLdb.connect(host='localhost', user='race_data', passwd='peloton', db='race_data')
    cursor = db.cursor()
    csv_data = csv.reader(file(CSV_PATH + '\\race_data.csv'))

    for row in csv_data:

        sql = 'INSERT INTO testdb (NAME, RANK, RACEDAY, TIME) VALUES(%s, %s, %s, %s)'
        cursor.execute(sql, (row[3], row[1], row[0], row[5]))

    db.commit()
    db.close()


# TO RUN IN CLI: C:\Python27\python.exe C:\Users\Kevin\Desktop\webscraper\webscraper.py
# This should be the only var to change for any new raceday
raceday = 'Vuelta_al_Pais_Vasco_2017_Stage_6'
write_to_csv()
load_csv_to_table()
