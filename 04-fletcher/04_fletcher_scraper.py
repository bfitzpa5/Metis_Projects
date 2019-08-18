# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 23:09:43 2019

@author: Brendan Non-Admin

Datapoints
---------------
Name
Project Description   O
Location              O
About                 O
Risks                 O
Goal                  O
Amount Pledged        X
Days to go            O
Backers               O
Category              O
Subcateogry           O
"""


import requests
from bs4 import BeautifulSoup

base_url = r'https://www.kickstarter.com/discover'

url = (r'https://www.kickstarter.com/projects/953146955/sleeping-gods'
       r'?ref=discovery_category')
response = requests.get(url)  

soup = BeautifulSoup(response.text, 'html.parser')

def ks_page_scrape(soup):
amount_pledged = ctoi(soup.find("span", class_="ksr-green-700").text)
goal = ctoi(soup.find("span", class_="money").text)
subgenre = soup.find(class_="svg-icon__icon--compass icon-20 fill-soft-black")
days_to_go = extract_days_to_go(soup)
print(soup.find("div", class_="description-container").text)


def ctoi(s):
    return int(s.replace('$', '').replace(',', ''))

def extract_days_to_go(soup):
    return ctoi(soup.find("div", class_='flex flex-column-lg mb4 mb5-sm')
                .find("div", class_="ml5 ml0-lg")
                .find("span")
                .text)