# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 23:09:43 2019

@author: Brendan Non-Admin

Datapoints
---------------
Name
Project Title         X
Project Description   X
Location              X
About                 X
Risks                 X
Goal                  X
Amount Pledged        X
Days to go            X
Backers               X
Category              X
SubCategory           X
Comments Count        X
"""


import requests
import re
import pprint
import json
from bs4 import BeautifulSoup

base_url = r'https://www.kickstarter.com/discover'

url = (r'https://www.kickstarter.com/projects/953146955/sleeping-gods')
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

def ks_page_scrape(soup):
    di = json.loads(soup.find('div', id='react-project-header')['data-initial'])


    project_name = extract_project_name(soup)
    project_description = extract_project_description(soup)
    location = extract_location(soup)
    about = extract_about(soup)
    risks = extract_risks(soup)
    goal = ctoi(soup.find("span", class_="money").text)
    amount_pledged = ctoi(soup.find("span", class_="ksr-green-700").text)
    backers = extract_backers(soup)
    days_to_go = extract_days_to_go(soup)
    category = di['project']['category']['parentCategory']['name']
    subcategory = extract_subcategory(soup)
    comments_count = di['project']['commentsCount']

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
           'comments_count' = comments_count}
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
