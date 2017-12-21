from bs4 import BeautifulSoup
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import numpy
import re


delay = 10

browser = webdriver.Chrome()
browser.get("https://my.byu.edu")

browser.find_element_by_xpath('//a[@href="https://cas.byu.edu/cas/login?service=https://my.byu.edu/uPortal/Login"]').click()


username = browser.find_element_by_id("netid")
password = browser.find_element_by_id("password")

username.send_keys("cvilorio")
password.send_keys("byu12345")

browser.find_element_by_xpath('//input[@class="submit"]').click()
time.sleep(delay)
browser.get("https://booklist.byu.edu/Home/ByCourse")

# --------------------------------------------------------------
def process_page():
	divs = browser.find_elements_by_xpath('//div[contains(@data-bind, "with: item")]')
	books = []
	for d in divs:
		BOOK = {}
		prof,title,isbn = d.split('\n')[:3]
		BOOK.prof = prof
		BOOK.title= title
		BOOK.isbn = isbn
		
		byu_prices = d.find_element_by_xpath('//div[contains(@data-bind,"foreach: variants")]').text
		byu_new = re.search(r'New Price: ([0-9.]+)', prices.text)
		byu_used = re.search(r'Used Price: ([0-9.]+)', prices.text)
		if byu_new:
			BOOK.byu_new = byu_new.groups()
		if byu_used:
			BOOK.byu_used = byu_used.groups()
		
		amazon = d.find_element_by_xpath('.//tbody[contains(@data-bind,"foreach: sources")]')
		if amazon.text:
			amazon

# ---------------------------------------------------------------

department_selector = browser.find_elements_by_xpath('//select')[1]
departments = department_selector.find_elements_by_xpath('.//option')
for dept in departments[1:]:
	dept.click()
	classes = dept.find_elements_by_xpath('.//select')
	for cls in classes[1:]:
		cls.click()
		browser.find_element_by_xpath("//input[@type='text']").click()
		browser.find_element_by_xpath("//input[@type='checkbox']").click()
		process_page()













