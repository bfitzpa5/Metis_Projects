import requests
from bs4 import BeautifulSoup
import webbrowser


url = 'http://boxofficemojo.com/movies/?id=biglebowski.htm'
webbrowser.open_new_tab(url)
response = requests.get(url)
response.status_code

page = response.text
soup = BeautifulSoup(page, 'html5lib')
print(soup.prettify)

print('%s\n%s' % (soup.find('a'), soup.a))
for a in soup.find_all('a'):
    print(a)

soup.find('title').text

soup.find(text="Domestic Total Gross: ")
