# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 12:50:37 2019

@author: Brendan Non-Admin
"""

import os
from selenium import webdriver
import time
import pandas as pd


def main():
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

if __name__ == '__main__':
    main()