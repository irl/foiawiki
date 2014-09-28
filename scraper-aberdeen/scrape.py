"""scrape.py
data scraping module for aberdeen disclosure log page
"""
from bs4 import BeautifulSoup as BS
from bs4 import ResultSet
from urllib2 import urlopen

def scrape(url):
    """ Scrapes data from Aberdeen City Disclosure Log subject page
    returns an array of all tds from list of items 
    """
    tds = []
    # get data from site
    soup = BS(urlopen(url).read())
    # separate into table rows
    for row in soup('table')[0].findAll('tr'):
        # get individual table columns
        for item in row('td'):
            # add each column to list of tds
            tds.append(str(item))
        for string in tds:
            string = string.split(",")
        #flatten list
        [item for sublist in tds for item in sublist]
    return tds

def dictify_scrape(url):
    db = {}
    columns = scrape(url)
    db['prices'] = columns[3]
    db['ids'] = columns[2].split(" - ")[0]
    db['titles'] = columns[2].split(" - ")[1]
    return db

