# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 23:09:43 2019

@author: Brendan Non-Admin

"""

import os
import json
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

driver_file = os.path.join(os.path.expanduser('~'), 'Downloads', 'chromedriver.exe')

def main():
    urls_fname = r'Data/kickstarter_urls.csv'
    urls = (pd.read_csv(urls_fname)
        .assign(url=lambda x: x.url.str.split('?', expand=True)[0])
    )
    
    print("Commencing Web Crawl")
    kickstarter_data = list()
    fname = r'Data/kickstarter_data.json'
    
    for index, url in urls.url.iteritems():
        print('  {:<10.0f} {}'.format(index, url))
        page_data = ks_scrape(url)
        if page_data:
            kickstarter_data.append(page_data)
            assert(write_json(fname, kickstarter_data))
            
    write_json(fname, kickstarter_data)
    print('Kickstarter Scraping Successful')
    return 1

def ks_scrape(url):
    driver = webdriver.Chrome(driver_file)
    driver.get(url)
    time.sleep(3)
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
    project_name = None
    while project_name is None:
        project_name = scrape_project_name(driver, url)
    try:
        project_description = driver.find_element_by_css_selector("div.NS_project_profiles__blurb").text
    except NoSuchElementException:
        project_description = driver.find_element_by_css_selector("p.project-description").text
    try:
        story = driver.find_element_by_class_name("rte__content").text
    except NoSuchElementException:
        #c = input('No Story :( Continue?' + ' ' * 8)
        c = 'Yes'
        if c == 'Yes':
            story = None
        else:
            raise NoSuchElementException()
    try:
        risks = driver.find_element_by_css_selector("div#risksAndChallenges").text
    except NoSuchElementException:
        try:
            risks = driver.find_element_by_css_selector("div.js-risks").text
        except NoSuchElementException:
            risks = None
    try:
        goal_and_pledged_backers = driver.find_element_by_css_selector("div.spotlight-project-video-archive").text
    except NoSuchElementException:
        xpath_str = '//div[@role="progressbar"]/following-sibling::div[1]'
        goal_and_pledged_backers = driver.find_element_by_xpath(xpath_str).text
    category_url = (driver.find_element_by_css_selector("a[href*='/discover/categories']")
        .get_attribute("href")
    )
    """ Unload Data """
    row = {'url': url,
           'project_name': project_name,
           'project_description': project_description,
           'story': story,
           'risks': risks,
           'goal_and_pledged_backers': goal_and_pledged_backers,
           'category_url': category_url,}
    driver.quit()
    return row

def write_json(fname, data):
    with open(fname, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)
    return True

def scrape_project_name(driver, url):
    try:
        project_name = driver.find_element_by_css_selector("div.NS_project_profile__title").text
        return project_name
    except NoSuchElementException:
        try:
            project_name =  driver.find_element_by_css_selector("h2.project-name").text
            return project_name
        except NoSuchElementException:
            driver.close()
            driver = webdriver.Chrome(driver_file)
            driver.get(url)
            time.sleep(3)
            return None

if __name__ == '__main__':
    main()