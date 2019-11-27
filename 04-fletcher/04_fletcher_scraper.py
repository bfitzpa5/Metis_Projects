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

import os
import requests
import re
import pprint
import json
from bs4 import BeautifulSoup
import webbrowser
import pprint
from selenium import webdriver
import time
import pandas as pd

base_url = (r'https://www.kickstarter.com/discover/advanced'
            r'?state=live&sort=end_date&seed=2611991&page=1')
executable_path = '{}/Downloads/chromedriver'.format(os.path.expanduser('~'))
browser = webdriver.Chrome(executable_path = executable_path)
browser.get(base_url)
xpath = '//*[@id="projects"]/div[4]/a'
for i in range(1, 200):
    load_more_btn = browser.find_element_by_xpath(xpath)
    if load_more_btn:
       load_more_btn.click()
       time.sleep(5)
urls = list()
for a in browser.find_elements_by_xpath("//a[@href]"):
    url = a.get_attribute("href")
    if r'kickstarter.com/projects/' in url and url not in urls:
        urls.append(url)
        print(url)
        print("Number of URLs:{:>10,d}".format(len(urls)))

(pd.DataFrame(urls, columns=['urls'])
 .to_csv(r'Data/kickstarter_urls.csv'))





response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

url = (r'https://www.kickstarter.com/projects/104470591'
       r'/joyscube-interactive-gaming-system-with-hybrid-cube-consoles')
webbrowser.open_new_tab(url)
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

def ks_page_scrape(soup):
    """ Scrape Page """
    di = json.loads(soup.find('div', id='react-project-header')['data-initial'])
    project_name = extract_project_name(soup)
    project_description = extract_project_description(soup)
    location = extract_location(soup)
    about = extract_about(soup)
    risks = extract_risks(soup)
    goal = soup.find("span", class_="money").text
    amount_pledged = soup.find("span", class_="ksr-green-700").text
    backers = extract_backers(soup)
    days_to_go = extract_days_to_go(soup)
    category = di['project']['category']['parentCategory']['name']
    subcategory = extract_subcategory(soup)
    comments_count = di['project']['commentsCount']
    """ Unload Data """
    row = {'project_name': project_name,
           'project_description': project_description,
           'location': location,
           'about': about,
           'risks': risks,
           'goal': goal,
           'amount_pledged': amount_pledged,
           'backers': backers,
           'days_to_go': days_to_go,
           'category': category,
           'subcategory': subcategory,
           'comments_count': comments_count}
    return row


def extract_project_name(soup):
    class_pat = re.compile(r'project-name')
    return soup.find('h2', class_=class_pat).text

def extract_project_description(soup):
    class_pat = re.compile(r'project-description')
    return soup.find('p', class_=class_pat).text

def extract_location(soup):
    class_pat = re.compile(r'map-pin')
    return soup.find('svg', class_=class_pat).next_sibling.text

def extract_about(soup):
    class_pat = re.compile(r'full-description')
    return soup.find('div', class_=class_pat).text

def extract_risks(soup):
    class_pat = re.compile(r'risks')
    return soup.find('div', class_=class_pat).text

def extract_days_to_go(soup):
    return ctoi(soup.find("div", class_='flex flex-column-lg mb4 mb5-sm')
                .find("div", class_="ml5 ml0-lg")
                .find("span")
                .text)

def extract_backers(soup):
    return soup.find('span', string='backers').previous

def extract_subcategory(soup):
    child_iter = (soup.find(class_="svg-icon__icon--compass icon-20 fill-soft-black")
                  .next_sibling
                  .children)
    return next(child_iter).text

def ctoi(s):
    return int(s.replace('$', '').replace(',', ''))
