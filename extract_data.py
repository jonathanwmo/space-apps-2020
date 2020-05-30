import datetime
from datetime import datetime, timedelta
import os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import time
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

def get_county_climate(county: str):
    '''
    gets avg temp, dew point, humidity, wind speed, pressure, precipitation
    :param county: string of county to be inputted
    :return: a list of values
    '''
    county = county.title()

    driver = webdriver.Chrome(os.path.dirname(os.path.realpath(__file__)) + '/chromedriver')
    driver.get('https://www.wunderground.com/history/monthly/us/ca/los-angeles/KLAX/date/2020-4')
    time.sleep(5)
    driver_page = driver.page_source
    page = BeautifulSoup(driver_page, 'html.parser')
    page_list = str(page).split('\n')

    avg_numbers_html = []
    avg_numbers = []

    count = 0
    inlines = False
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

    # print(avg_numbers_html)
    # print(avg_numbers_html)
    print(avg_numbers_stripped)
    # for line in page_list:
    #     print(line)
    #     print("\n")

get_county_climate("Los Angeles")



# counties = ['California Total', 'Los Angeles', 'Riverside', 'San Diego', 'Orange', 'San Bernardi', 'Alameda', 'Santa Clara', 'San Francisco', 'San Mateo', 'Kern', 'Tulare', 'Santa Barbara', 'Fresno', 'Imperial', 'Contra Costa', 'Sacramento', 'Ventura', 'San Joaquin', 'Kings', 'Stanislaus', 'Sonoma', 'Solano', 'Monterey', 'Marin', 'Merced', 'San Luis Obispo', 'Yolo', 'Santa Cruz', 'Placer', 'Napa', 'Humboldt', 'Madera', 'El Dorado', 'San Benito', 'Del Norte', 'Sutter', 'Nevada', 'Butte', 'Shasta', 'Mono', 'Mendocino', 'Yuba', 'Lake', 'Inyo', 'Mariposa', 'Calaveras', 'Glenn', 'Amador', 'Siskiyou', 'Colusa', 'Lassen', 'Tehama', 'Plumas', 'Tuolumne', 'Alpine', 'Modoc', 'Sierra', 'Trinity', 'Alameda - Berk', 'Yuba-Sutter']
#
# for county in counties:
#     print(county, get_county_data(county))


# https://stackoverflow.com/questions/36129963/use-beautifulsoup-to-obtain-view-element-code-instead-of-view-source-code

# </span><div class="mat-ripple mat-button-ripple" matripple=""></div><div class="mat-button-focus-overlay"></div></button><!-- --><mat-menu class=""><!-- --></mat-menu></menu-item-more></nav></lib-menu><!-- --><div _ngcontent-app-root-c137=""></div><lib-search _ngcontent-app-root-c137="" _nghost-app-root-c135=""