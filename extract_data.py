import datetime
from datetime import datetime, timedelta
import os
from urllib.request import Request, urlopen
import urllib.request
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import time
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_county_data(county: str):
    '''
    look at https://www.worldometers.info/coronavirus/usa/california/ to get values of total cases, new cases,
    total deaths, new deaths, active cases, total tests, etc.
    :param county: string of the county in California that we want to extract data from
    :return: a list of the data
    '''

    county = county.title()

    # open url page
    req = Request('https://www.worldometers.info/coronavirus/usa/california/', headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    page = BeautifulSoup(page, 'html.parser')

    # split each line of html into a list
    page_list = str(page).split('\n')

    # only the desired lines of html will be stored in this list
    county_numbers_html = []
    # only the final values will be stored in this list
    county_numbers = []

    count = 0
    inlines = False
    # iterate through page_list which is all lines of html
    for line in page_list:
        if county in line:
            inlines = True
        # when inlines==True, add desired lines of html to our list
        if inlines == True:
            county_numbers_html.append(line)
            count += 1
        # once 13 lines have been added, stop
        if count == 13:
            break

    ############## Now we extract the numbers from our desired list of html lines ########

    # for california total the html is formatted slightly different
    if county == "California Total":
        for line in county_numbers_html:
            finder = re.compile(r'\b\d[\d,.]*\b')
            # use regular expression to extract numbers from desired html lines and append them list
            if re.search(finder, line) is not None:
                county_numbers.append(re.search(finder, line).group())
            else:
                # if no match, append an empty string to country_numbers list
                # instead
                county_numbers.append("")
        # sometimes empty strings get appended, we get rid of them here
        county_numbers.pop(0)
        county_numbers.pop(0)
        county_numbers = county_numbers[0:7]

    # use this for all california counties
    else:
        for line in county_numbers_html:
            finder = re.compile(r'\b\d[\d,.]*\b')
            # use regular expression to extract numbers from desired html lines and append them list
            if re.search(finder, line) is not None:
                county_numbers.append(re.search(finder, line).group())
            else:
                # if no match, append an empty string to country_numbers list
                # instead
                county_numbers.append("")
        # sometimes empty strings get appended, we get rid of them here
        county_numbers.pop(0)
        county_numbers.pop(1)
        county_numbers.pop(2)
        county_numbers.pop(4)
        county_numbers.pop(5)
    county_numbers = county_numbers[0:6]
    mydict = {"Total Cases": county_numbers[0], "New Cases": county_numbers[1], "Total Deaths": county_numbers[2], "New Deaths": county_numbers[3], "Active Cases": county_numbers[4], "Total Tests": county_numbers[5]}
    return mydict

def get_county_climate(county: str, month: str):
    '''
    gets avg temp, dew point, humidity, wind speed, pressure, precipitation
    :param county: string of county to be inputted
    :return: a list of values
    '''
    county = county.lower().replace(" ", "-")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    driver = webdriver.Chrome(dir_path + '/chromedriver')
    url = 'https://www.wunderground.com/history/monthly/us/ca/' + county + '/date/2020-' + str(month)
    driver.get(url)
    time.sleep(5)
    driver_page = driver.page_source
    page = BeautifulSoup(driver_page, 'html.parser')
    page_list = str(page).split('\n')

    avg_numbers_html = []
    avg_numbers = []

    for line in page_list:
        if '</span><div class="mat-ripple mat-button-ripple" matripple=""></div><div class="mat-button-focus-overlay"></div></button><!-- --><mat-menu class=""><!-- --></mat-menu></menu-item-more></nav></lib-menu><!-- --><div _ngcontent-app-root-c137=""></div><lib-search _ngcontent-app-root-c137="" _nghost-app-root-c135="" ' in str(line):
            avg_numbers_html.append(line)
    for line in avg_numbers_html:
        finder = re.compile(r'\s\b\d[\d,.]*\b\s')
        if re.findall(finder, line) is not None:
            avg_numbers = (re.findall(finder, line))

    avg_numbers_stripped = []
    for i in avg_numbers:
        avg_numbers_stripped.append(i.strip())

    date_aot = str(datetime.today())[0:10]
    day = int(date_aot[-2:])

    index = avg_numbers_stripped.index('5,0') + 6
    avg_temp_list = avg_numbers_stripped[index + day::3]
    avg_temp_list = avg_temp_list[:day]

    avg_dewpoint_list = avg_numbers_stripped[index + day + (day*3)::3]
    avg_dewpoint_list = avg_dewpoint_list[:day]

    avg_humidity_list = avg_numbers_stripped[index + day + (day*6)::3]
    avg_humidity_list = avg_humidity_list[:day]

    avg_windspeed_list = avg_numbers_stripped[index + day + (day*9)::3]
    avg_windspeed_list = avg_windspeed_list[:day]

    avg_pressure_list = avg_numbers_stripped[index + day + (day*12)::3]
    avg_pressure_list = avg_pressure_list[:day]

    avg_temp_list = list(map(float, avg_temp_list))
    avg_dewpoint_list = list(map(float, avg_dewpoint_list))
    avg_humidity_list = list(map(float, avg_humidity_list))
    avg_windspeed_list = list(map(float,avg_windspeed_list))
    avg_pressure_list = list(map(float, avg_pressure_list))

    dir_path = dir_path + '/csv/' + county + '.csv'
    if not os.path.exists(dir_path):
        with open(dir_path, 'a') as f:
            f.write("test")

    print("avg temps",avg_temp_list)
    print("avg dew points", avg_dewpoint_list)
    print("avg humidities", avg_humidity_list)
    print("avg windspeeds", avg_windspeed_list)
    print("avg pressures", avg_pressure_list)

def get_county_data_30(county: str):
    '''
    gets covid-19 data of past 30 days from csv file https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv
    :param county: county to input
    :return: 2 lists of
    '''

    datafile = urllib.request.urlopen('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
    # a list of lists
    full_county_list = []
    dates_list = []
    cases_list = []
    deaths_list = []
    for line in datafile.readlines():
        line = line.decode('utf-8').strip()
        row = line.split(",")
        if county.title() in str(row):
            full_county_list.append(row)

    for list in full_county_list:
        dates_list.append(list[0])
        cases_list.append(list[-2])
        deaths_list.append(list[-1])

    # print(full_county_list)
    print(dates_list)
    print(cases_list)
    print(deaths_list)
get_county_data_30("Los Angeles")
get_county_climate("Los Angeles", '5')



# counties = ['California Total', 'Los Angeles', 'Riverside', 'San Diego', 'Orange', 'San Bernardi', 'Alameda', 'Santa Clara', 'San Francisco', 'San Mateo', 'Kern', 'Tulare', 'Santa Barbara', 'Fresno', 'Imperial', 'Contra Costa', 'Sacramento', 'Ventura', 'San Joaquin', 'Kings', 'Stanislaus', 'Sonoma', 'Solano', 'Monterey', 'Marin', 'Merced', 'San Luis Obispo', 'Yolo', 'Santa Cruz', 'Placer', 'Napa', 'Humboldt', 'Madera', 'El Dorado', 'San Benito', 'Del Norte', 'Sutter', 'Nevada', 'Butte', 'Shasta', 'Mono', 'Mendocino', 'Yuba', 'Lake', 'Inyo', 'Mariposa', 'Calaveras', 'Glenn', 'Amador', 'Siskiyou', 'Colusa', 'Lassen', 'Tehama', 'Plumas', 'Tuolumne', 'Alpine', 'Modoc', 'Sierra', 'Trinity', 'Alameda - Berk', 'Yuba-Sutter']
# for county in counties:
#     print(county, get_county_data(county))

# counties = ['Los Angeles', 'Riverside', 'San Diego', 'Orange', 'San Bernardi', 'Alameda', 'Santa Clara', 'San Francisco', 'San Mateo', 'Kern', 'Tulare', 'Santa Barbara', 'Fresno', 'Imperial', 'Contra Costa', 'Sacramento', 'Ventura', 'San Joaquin', 'Kings', 'Stanislaus', 'Sonoma', 'Solano', 'Monterey', 'Marin', 'Merced', 'San Luis Obispo', 'Yolo', 'Santa Cruz', 'Placer', 'Napa', 'Humboldt', 'Madera', 'El Dorado', 'San Benito', 'Del Norte', 'Sutter', 'Nevada', 'Butte', 'Shasta', 'Mono', 'Mendocino', 'Yuba', 'Lake', 'Inyo', 'Mariposa', 'Calaveras', 'Glenn', 'Amador', 'Siskiyou', 'Colusa', 'Lassen', 'Tehama', 'Plumas', 'Tuolumne', 'Alpine', 'Modoc', 'Sierra', 'Trinity', 'Alameda - Berk', 'Yuba-Sutter']
# for county in counties:
#     print(county)
#     print(county, get_county_climate(county, '5'))
#     print('\n')
# https://stackoverflow.com/questions/36129963/use-beautifulsoup-to-obtain-view-element-code-instead-of-view-source-code

# </span><div class="mat-ripple mat-button-ripple" matripple=""></div><div class="mat-button-focus-overlay"></div></button><!-- --><mat-menu class=""><!-- --></mat-menu></menu-item-more></nav></lib-menu><!-- --><div _ngcontent-app-root-c137=""></div><lib-search _ngcontent-app-root-c137="" _nghost-app-root-c135=""