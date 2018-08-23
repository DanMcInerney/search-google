#!/usr/bin/env python2
# -*- coding: utf8 -*-

import sys
import time
import random
import argparse

from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchFrameException
from selenium.webdriver.common.keys import Keys

# If this script no longer fetches any results check the XPath

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--search', help='Enter the search term')
    parser.add_argument('-p', '--pages', default='1', help='Enter how many pages to scrape (1 page = 100 results)')
    return parser.parse_args()

def start_browser():
    br = webdriver.Firefox()
    br.implicitly_wait(10)
    return br

def get_ua():
    ua_list = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0',
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0']
    ua = random.choice(ua_list)
    return ua

def scrape_results(br):
    # Xpath will find a subnode of h3, a[@href] specifies that we only want <a> nodes with
    # any href attribute that are subnodes of <h3> tags that have a class of 'r'
    links = br.find_elements_by_xpath("//h3[@class='r']/a[@href]")
    results = []
    for link in links:
        title = link.text.encode('utf8')
        url = link.get_attribute('href')
        title_url = (title, url)
        results.append(title_url)
    return results

def go_to_page(br, page_num, search_term):
    page_num = page_num - 1
    start_results = page_num * 100
    start_results = str(start_results)
    url = 'https://www.google.com/webhp?#num=100&start='+start_results+'&q='+search_term
    print '[*] Fetching 100 results from page '+str(page_num+1)+' at '+url
    br.get(url)
    time.sleep(2)

def main():
    args = parse_args()
    br = start_browser()
    if not args.search:
        sys.exit("[!] Enter a term or phrase to search with the -s option: -s 'dan mcinerney'")
    search_term = args.search
    pages = args.pages

    all_results = []
    for page_num in xrange(int(pages)):
        page_num = page_num+1 # since it starts at 0
        go_to_page(br, page_num, search_term)
        titles_urls = scrape_results(br)
        for title in titles_urls:
            all_results.append(title)

    for result in all_results:
        title = result[0]
        url = result[1]
        print '[+]', title, '--', url
    br.quit()

main()
