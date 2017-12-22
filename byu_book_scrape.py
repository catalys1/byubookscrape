from bs4 import BeautifulSoup
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import numpy
import re
import json


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
time.sleep(2)

# --------------------------------------------------------------
def process_page():
	divs = browser.find_elements_by_xpath('//div[contains(@data-bind, "with: item")]')
	books = []
	for d in divs:
		BOOK = {}
		prof,title,isbn = d.text.split('\n')[:3]
		BOOK['prof'] = prof
		BOOK['title'] = title
		BOOK['isbn'] = isbn
		
		byu_prices = d.find_element_by_xpath('//div[contains(@data-bind,"foreach: variants")]').text
		byu_new = re.search(r'New Price: ([$0-9.]+)', byu_prices)
		byu_used = re.search(r'Used Price: ([$0-9.]+)', byu_prices)
		if byu_new:
			BOOK['byu_new'] = byu_new.groups()
		if byu_used:
			BOOK['byu_used'] = byu_used.groups()
		
		amazon = d.find_element_by_xpath('.//tbody[contains(@data-bind,"foreach: sources")]')
		if amazon.text:
			options = amazon.find_elements_by_xpath('.//option')
			for o in options:
				o.click()
				time.sleep(1)
				price = amazon.find_elements_by_xpath('.//span[contains(@data-bind,"text: price")]')
				if o.text == 'New':
					BOOK['amazon_new'] = price.text
				elif o.text == 'Used':
					BOOK['amazon_used'] = price.text
		books.append(BOOK)
	return books

# ---------------------------------------------------------------

department_selector = browser.find_elements_by_xpath('//select')[1]
departments = department_selector.find_elements_by_xpath('.//option')

out_file = 'scrape.json'
results = {}
print 'Starting departments'
for dept in departments[1:]:
	dept.click()
	classes = dept.find_elements_by_xpath('//select')[-1]
	classes = classes.find_elements_by_xpath('.//option')
	class_dict = {}
	print dept.text
	for cls in classes[1:]:
		print '  {}'.format(cls.text)
		cls.click()
		time.sleep(4)
		browser.find_element_by_xpath("//input[@type='text']").click()
		time.sleep(1)
		browser.find_element_by_xpath("//input[@type='checkbox']").click()
		time.sleep(3)
		books = process_page()
		class_dict[cls.text] = books
	results[dept.text] = class_dict
	json.dump(results, open(out_file, 'w'))
	time.sleep(5)












