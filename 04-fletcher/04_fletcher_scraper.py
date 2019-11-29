# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 23:09:43 2019

@author: Brendan Non-Admin

Datapoints
---------------
Name
Project Title         0
Project Description   0
Location              0
About                 0
Risks                 0
Goal                  0
Amount Pledged        0
Days to go            0
Backers               0
Category              0
SubCategory           0
Comments Count        0
"""

import re
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

def main():
    urls_fname = r'Data/kickstarter_urls.csv'
    urls = (pd.read_csv(urls_fname)
        .assign(url=lambda x: x.url.str.split('?', expand=True)[0])
    )
    print("Commencing Web Crawl")
    kickstarter_data = list()
    for index, url in urls.url.iteritems():   
        print(url)
        page_data = ks_scrape(url)
        if page_data:
            kickstarter_data.append(page_data)
    
    fname = r'Data/kickstarter_data.csv'
    (pd.DataFrame(kickstarter_data)
        .to_csv(fname, index=False)
    )
    print('Kickstarter Scraping Successful')
    return 1

def ks_scrape(url):
    with urllib.request.urlopen(url) as response:
        html = response.read()
    soup = BeautifulSoup(html, 'html5lib')
    removal_str = ("This project has been removed from visibility at the "
    "request of the creator. It will remain permanently out of view.")
    copyright_str = ("is the subject of an intellectual property dispute and is currently unavailable.")
    if (   soup.find("p", string=re.compile(removal_str)) is not None
        or soup.find("strong", string=re.compile(copyright_str)) is not None):
        return None
    """ Scrape Page """
    project_name = soup.find('h3', class_="normal").text
    if soup.find('div', class_="NS_project_profiles__blurb") is not None:
        project_description = (soup.find('div', class_="NS_project_profiles__blurb")
            .text)
    else:
        project_description = None
    content = soup.find('section', class_=re.compile('project-content')).find('div').find('div').find('div').text
    if soup.find("div", class_="spotlight-project-video-archive") is not None:
        goal_and_pledged = (soup.find("div", class_="spotlight-project-video-archive")
            .text)
    else:
        goal_and_pledged = soup.find("div", role="progressbar").next_sibling.text
    if soup.find('div', string=re.compile('backers')) is not None:
        backers = (soup.find('div', string=re.compile('backers'))
            .parent.text)
    else:
        try:
            backers = soup.find('span', string=re.compile('backes')).previous_sibling.text
        except:
            backers = soup.find('span', string=re.compile('backer')).text
    category_url = (soup.find('a', href=re.compile('/discover/categories'))
        ['href'])
    """ Unload Data """
    row = {'url': url,
           'project_name': project_name,
           'project_description': project_description,
           'content': content,
           'goal_and_pledged': goal_and_pledged,
           'backers': backers,
           'category_url': category_url,}
    return row

if __name__ == '__main__':
    main()