import requests
from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime as dt


def read_file():
    """
    Reads a CSV file containing City/State combos to scrape

    return:
        list of lists of State[0] and City[1]
    """

    with open('citylist.csv', newline='') as csvfile:
        cities = []
        cityfile = csv.reader(csvfile, delimiter = ',')
        for row in cityfile:
            cities.append(row[:2])

        return cities[1:] #remove the header!


def construct_urls(citystate):
    """
    Constructs a URL to scrape from a city/state combo.
    Sample URL: 'https://www.bestplaces.net/city/utah/price'

    input:
        List of lists of State[0] and City[1]

    return:
        Above list with URLs added [3]
    """

    base_url = 'https://www.bestplaces.net/city/STATE/CITY'
    urls = []
    for place in citystate:
        url = base_url.replace('STATE', place[0]).replace('CITY', place[1]).replace(' ', '')
        place.append(url)

    return citystate


def overview_parse(insoup):
    """
    Parses the grid on the overview page.
    input: 
        BeautifulSoup object of the requested page (Overview page)

    return:
        List containing the following values:
            0 Population
            1 Population Change (since 2010)
            2 Unemployment Rate
            3 Median Income
            4 Median Home Price
            5 Median Age
            6 Comfort Index (Climate)
    """
    ### Extract fields

    # Find the table
    grid = insoup.find_all('div', class_= 'col-md-4 px-1')
    
    # Find our 3 values from the first column
    population = grid[0].find_all(class_='text-center py-0 my-0')[0].contents[0]
    popchange = grid[0].find_all(class_='text-center py-0 my-0')[1].contents[0]
    unemploy = grid[0].find(lambda tag: tag.name == 'p' and tag.get('class') == ['text-center']).contents[0]

    # Find our 2 values from the second column
    medincome = grid[1].find_all(lambda tag: tag.name == 'p' and tag.get('class') == ['text-center'])[0].contents[0]
    medhomeprice = grid[1].find_all(lambda tag: tag.name == 'p' and tag.get('class') == ['text-center'])[1].contents[0]

    # Find our 2 values from the second column
    medage = grid[2].find_all(lambda tag: tag.name == 'p' and tag.get('class') == ['text-center'])[0].contents[0]
    comfortidx = grid[2].find_all(lambda tag: tag.name == 'p' and tag.get('class') == ['text-center'])[1].contents[0]

    # Classic python debugging
    if False:
        print(f'medincome: {medincome}, medhomeprice: {medhomeprice}')
        print(f'pop: {population}, popchange: {popchange}, unemploy: {unemploy}')
        print(f'medage: {medage}, comfortidx: {comfortidx}')

    ### Transform fields

    population = int(population.replace(',', ''))
    popchange = float(popchange.replace('+', '').replace('%', '').replace(' since 2010', ''))
    unemploy = float(unemploy.replace('%', ''))
    medincome = int(medincome.replace('$', '').replace(',', ''))
    medhomeprice = int(medhomeprice.replace('$', '').replace(',', ''))
    medage = float(medage)
    comfortidx = float(comfortidx.split('/')[0])

    return [population, popchange, unemploy, medincome, medhomeprice, medage, comfortidx]

def scrape_stuff(cities):
    """
    Iterate through the locations to scrape, and scrape them.

    input:
        list of cities with URLs[3]
    
    return:
        list of cities with new data appended[3:]
    """
    newdata = []
    for place in cities:
        req = requests.get(place[2], verify=False)
        soup = BeautifulSoup(req.content, 'html.parser')
        ovw = overview_parse(soup)
        newdata.append(place + ovw)

    return newdata

def write_to_file(info):
    timestamp = dt.now().strftime('%Y%m%d%H%M%S')
    with open('newdata_' + timestamp + '.csv', 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(info)



if __name__ == '__main__':
    """
    3/4/2021 Read cities/states from a file
    3/4/2021 Write data to a file
    Read other pages:
        Cost of Living
        Crime
        Climate?
        Economy
        Housing Stats
        Rankings
    """
    cities = read_file()

    cities = construct_urls(cities)

    data = scrape_stuff(cities)
    print(data)

    write_to_file(data)
