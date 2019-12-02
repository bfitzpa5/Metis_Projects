# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 23:09:43 2019

@author: Brendan Non-Admin

"""

import os
import json
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def main():
    urls_fname = r'Data/kickstarter_urls.csv'
    urls = (pd.read_csv(urls_fname)
        .assign(url=lambda x: x.url.str.split('?', expand=True)[0])
    )
    driver = os.path.join(os.path.expanduser('~'), 'Downloads', 'chromedriver.exe')
    driver = webdriver.Chrome(driver)
    
    print("Commencing Web Crawl")
    kickstarter_data = list()
    for index, url in urls.url[1431:].iteritems():   
        print(url)
        page_data = ks_scrape(driver, url)
        if page_data:
            kickstarter_data.append(page_data)
    
    fname = r'Data/kickstarter_data.json'
    with open(fname, "w") as f:
        json.dump(kickstarter_data, f, indent=4, sort_keys=True)
    print('Kickstarter Scraping Successful')
    return 1

def ks_scrape(driver, url):
    driver.get(url)
    removal_str = ("This project has been removed from visibility at the "
    "request of the creator. It will remain permanently out of view.")
    copyright_str = "is the subject of an intellectual property dispute and is currently unavailable."
    try:
        exception_str = ("//*[contains(text(),'{}') or contains(text(),'{}')]"
                              .format(removal_str, copyright_str))
        driver.find_element_by_xpath(exception_str)
        return None
    except NoSuchElementException:
        pass
    """ Scrape Page """
    try:
        project_name = driver.find_element_by_css_selector("div.NS_project_profile__title").text
    except NoSuchElementException:
        project_name = driver.find_element_by_css_selector("h2.project-name").text
    try:
        project_description = driver.find_element_by_css_selector("div.NS_project_profiles__blurb").text
    except NoSuchElementException:
        project_description = driver.find_element_by_css_selector("p.project-description").text
    try:
        story = driver.find_element_by_class_name("rte__content").text
    except NoSuchElementException:
        story = None
    try:
        risks = driver.find_element_by_css_selector("div#risksAndChallenges").text
    except NoSuchElementException:
        risks = None
    try:
        goal_and_pledged_backers = driver.find_element_by_css_selector("div.spotlight-project-video-archive").text
    except NoSuchElementException:
        goal_and_pledged_backers = driver.find_element_by_xpath('//*[@id="react-project-header"]/div/div/div[3]/div').text
    category_url = (driver.find_element_by_css_selector("a[href*='/discover/categories']")
        .get_attribute("href"))
    """ Unload Data """
    row = {'url': url,
           'project_name': project_name,
           'project_description': project_description,
           'story': story,
           'risks': risks,
           'goal_and_pledged_backers': goal_and_pledged_backers,
           'category_url': category_url,}
    return row

if __name__ == '__main__':
    main()