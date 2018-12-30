import requests
from bs4 import BeautifulSoup
import webbrowser
import re

"""
Use Big Lebowski as example
"""
mojo_url = 'http://boxofficemojo.com/movies/?id=biglebowski.htm'
imdb_url = 'https://www.imdb.com/title/tt0118715/'
webbrowser.open_new_tab(mojo_url)
webbrowser.open_new_tab(imdb_url)

response = requests.get(mojo_url)
response.status_code

page = response.text
soup = BeautifulSoup(page, 'html5lib')

def movie_val(soup, field_name):
    '''Grab a value from boxofficemojo HTML
    
    Takes a string attribute of a movie on the page and
    returns the string in the next sibling object
    (the value for that attribute)
    or None if nothing is found.
    '''
    obj = soup.find(text=re.compile(field_name))
    if not obj: 
        return None
    # this works for most of the values
    next_sibling = obj.findNextSibling()
    if next_sibling:
        return next_sibling.text 
    else:
        return None

field_dict = {'release_date': 'Release Date', 'distributor': 'Distributor',
              'genre': 'Genre', 'rating': 'MPAA Rating',
              'runtime': 'Runtime', 'budget': 'Production Budget',
              'director': 'Director', 'actors': 'Actors',
              'num_theaters': 'Number of Theaters',
              'opening_wkend_gross': 'Opening Weekend'}

"""
Test fields
"""
for col, field_name in field_dict.items():
    print('%-20s%-50s' % (col, movie_val(soup, field_name))) 

