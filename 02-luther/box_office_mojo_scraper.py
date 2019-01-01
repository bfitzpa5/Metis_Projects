import sys
import requests
from bs4 import BeautifulSoup
import webbrowser
import re
import string
import pandas as pd
from collections import defaultdict
import time

WAIT_TIME = 5
base_url = 'http://www.boxofficemojo.com'

"""
Use Big Lebowski as example
star_wars_url = 'https://www.boxofficemojo.com/movies/?id=starwars8.htm'
lebow_url = 'http://boxofficemojo.com/movies/?id=biglebowski.htm'
yr_url = 'https://www.boxofficemojo.com/yearly/'
webbrowser.open_new_tab(lebow_url)
webbrowser.open_new_tab(star_wars_url)
"""

def main(argv):
    field_dict = {'release_date': 'Release Date:', 'distributor': 'Distributor',
                  'rating': 'MPAA Rating', 'genre': 'Genre: ',
                  'runtime': 'Runtime:', 'budget': 'Production Budget:'}
    records = list()
    url = 'https://www.boxofficemojo.com/yearly/chart/?yr=2018&p=.htm'
    response = requests.get(url)
    if response.status_code != 200:
        raise HttpStatusCodeError(url, code)
    soup = BeautifulSoup(response.text, 'html5lib')
    text_pat = re.compile('Movie.*Title.*(click.*to.*view)')
    row_iter = (soup.find('td', text=text_pat).parent.next_siblings)
    end_pat = re.compile('Summary.*of.*Movies on Chart')
    row = next(row_iter)
    count = 0
    while row and end_pat.search(row.text) is None:
        tag = row.find('a')
        url = tag['href']
        movie = tag.text
        count += 1
        print('Scraping Movie #%d:\t%s...' % (count, movie), end='')
        record = movie_scrape(movie, url, field_dict)
        if record:
            records.append(record)
            print('Complete')
        time.sleep(WAIT_TIME)
        row = next(row_iter)
    
    pd.DataFrame(records).to_csv('data/test_18.csv', index=False)

def movie_scrape(movie, url, field_dict):
    response = requests.get(base_url + url)
    if response.status_code != 200:
        print("HTTP Error %s: %s" (e.code, e.url))
        return None
    soup = BeautifulSoup(response.text, 'html5lib')
    record = dict()
    record['movie'] = movie
    record['url'] = url
    for col, field_name in field_dict.items():
        record[col] = movie_val(soup, field_name)
    record['director'] = table_list(soup, 'Director')
    record['actors'] = table_list(soup, 'Actors')

    rows = table_rows(soup, re.compile('Domestic.*Summary'))
    record['open_wkend_gross'] = table_val(rows, 'Opening.*Weekend')
    record['widest_release'] = (table_val(rows, 'Widest.*Release')
                             .replace(' theaters', ''))
    record['in_release'] = table_val(rows, 'In.*Release')
    return record

def movie_val(soup, field_name):
    """Grab a value from boxofficemojo HTML

    Takes a string attribute of a movie on the page and
    returns the string in the next sibling object
    (the value for that attribute)
    or None if nothing is found.
    """
    obj = soup.find(text=re.compile(field_name))
    if obj: 
        next_sibling = obj.findNextSibling()
        if next_sibling:
            return next_sibling.text
    return None

def table_list(soup, pat):
    td = soup.find('td', text=re.compile(pat))
    if td:
        actor_tags =  td.findNextSibling().find_all('a')
        return ', '.join([x.text for x in actor_tags])
    return None

def table_rows(soup, pat):
    return (soup.find('div', text=pat)
            .findNextSibling()
            .find_all('tr'))

def table_val(rows, pat):
    for tr in rows:
        for td in tr.find_all('td'):
            if re.compile(pat).search(td.text):
                t = td.findNextSibling().text
                return ''.join([x if ord(x) < 128 else ' ' for x in t]).strip()
    return None

if __name__ == '__main__':
    main(sys.argv)
