import sys
import requests
from bs4 import BeautifulSoup
import webbrowser
import re
import string
import pandas as pd
from collections import defaultdict
import time
import datetime as dt

WAIT_TIME = 5
base_url = 'http://www.boxofficemojo.com'

def main(argv):
    field_dict = {'release_date': 'Release Date:', 'distributor': 'Distributor',
                  'rating': 'MPAA Rating', 'genre': 'Genre: ',
                  'runtime': 'Runtime:', 'budget': 'Production Budget:'}
    records = list()
    # the years 2007 through 2018 for the top 100 movies url
    for year in range(2018, 2007, -1):
        url = '%s/yearly/chart/?yr=%d&p=.htm' % (base_url, year)
        print ('Scraping %d Data (%s)...' % (year, url), end='')
        response = requests.get(url)
        if response.status_code != 200:
            print('HTTP Status Code Error: %d\nUrl:%s' (response.code, url))
            sys.exit(1)
        soup = BeautifulSoup(response.text, 'html5lib')
        text_pat = re.compile('Movie.*Title.*(click.*to.*view)')
        row_iter = (soup.find('td', text=text_pat).parent.next_siblings)
        end_pat = re.compile('Summary.*of.*Movies on Chart')
        row = next(row_iter)
        count = 0
        while row and end_pat.search(row.text) is None:
            tag = row.find('a')
            url = tag['href']
            title = tag.text
            count += 1
            record = movie_scrape(title, url, field_dict)
            if record:
                records.append(record)
            time.sleep(WAIT_TIME)
            row = next(row_iter)
        print('Complete')

    fname = (  'data/box_office_mojo_data_%s.csv'
             % dt.datetime.now().isoformat()[0:-7])
    pd.DataFrame(records).to_csv(fname, index=False)
    print('See file located at: %s' % fname)

def movie_scrape(title, url, field_dict):
    response = requests.get(base_url + url)
    if response.status_code != 200:
        print("HTTP Error %s: %s" (e.code, e.url))
        return None
    soup = BeautifulSoup(response.text, 'html5lib')
    record = dict()
    record['title'] = title
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
