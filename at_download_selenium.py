# -*- coding: utf-8 -*-
import unittest
import time
import re

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

book = '43816/342319'
baseUrl = 'https://author.today/reader/'
directory = 'books/'
nextElement = "li.next"


class DownloadAt(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(r'D:\Project/chromedriver.exe')
        self.driver.maximize_window()

    def test_download_at(self):
        print("")
        driver = self.driver
        driver.get(baseUrl + book)
        title = driver.title
        bookName = re.match(r'^.{12}[^,]+', title).group(0)
        fileName = directory + bookName + '.html'
        data = driver.find_element_by_id("text-container").get_attribute('innerHTML')
        self.writeFile(data, fileName)

        while self.hasNextPage():
            nextPageElement = driver.find_element_by_css_selector(nextElement)
            nextPageLink= driver.find_element_by_css_selector('li.next>a')
            Hover = ActionChains(driver).move_to_element(nextPageElement).move_to_element(nextPageLink)
            Hover.click(nextPageLink).perform()
            time.sleep(2)
            data = driver.find_element_by_id("text-container").get_attribute('innerHTML')
            self.writeFile(data, fileName)

    def tearDown(self):
        self.driver.quit()

    def hasNextPage(self):
        try:
            element = self.driver.find_element_by_css_selector(nextElement)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return True
        except:
            return False

    def writeFile(self, data, fileName):
        with open(fileName, 'a') as file:
            file.write(data)


if __name__ == "__main__":
    unittest.main()
