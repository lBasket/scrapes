import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.bestplaces.net/city/utah/vernal'

req = requests.get(url, verify=False)

soup = BeautifulSoup(req.content, 'html.parser')


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
    # Find the table
    grid = soup.find_all('div', class_= 'col-md-4 px-1')
    
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
    print(f'medincome: {medincome}, medhomeprice: {medhomeprice}')
    print(f'pop: {population}, popchange: {popchange}, unemploy: {unemploy}')
    print(f'medage: {medage}, comfortidx: {comfortidx}')

    return [population, popchange, unemploy, medincome, medhomeprice, medage, comfortidx]

