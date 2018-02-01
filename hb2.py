# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import csv
# import requests
# import multiprocessing
from grab import Grab
from bs4 import BeautifulSoup
from datetime import datetime


# TODO не авторизируется
# def get_html(url, url1, login, password):
#     r = requests.get(url1, auth=(login, password), verify=False)
#     html = r.text
#     return html


def get_html(url, login, password):
    g = Grab()
    g.go(url)
    # print g.xpath_text("//title")
    g.set_input("LoginForm[username]", login)
    g.set_input("LoginForm[password]", password)
    g.submit()
    # print g.xpath_text("//title")
    html = g.response.body
    return html


def get_next_page(html):
    s = BeautifulSoup(html, 'lxml')
    try:
        link_to_next_page = "https://handbook2-stage.uttc-usa.com" + s.find('li', class_='next').find('a').get('href')
    except:
        link_to_next_page = None
    return link_to_next_page


def parser(html):
    s = BeautifulSoup(html, 'lxml')
    rows = s.find('tbody').find_all('tr')
    data = []
    for row in rows:
        try:
            number = row.find('td', class_="number").text.strip()
        except:
            number = ""
        try:
            link = "https://handbook2-stage.uttc-usa.com" + row.find('td', class_="number").find('a').get("href")
        except:
            link = ""
        try:
            title = row.find('td', class_="title").text.strip()
        except:
            title = ""
        try:
            status = row.find('td', class_="status").text.strip()
        except:
            status = ""
        try:
            employee = row.find('td', class_="employee").text.strip()
        except:
            employee = ""


        data.append({
            'number': number,
            'link': link,
            'title': title,
            'status': status,
            'employee': employee
        })
    return data


def write_to_csv(data):
    with open("pars.csv", "w") as parsf:
        fieldnames = ['number', 'link', 'title', 'status', 'employee']
        writer = csv.DictWriter(parsf, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def main():
    start = datetime.now()
    url = 'https://handbook2-stage.uttc-usa.com/corporation/issues?statuses=new+in-work+discussion-required&employees='
    login = 'aokunev'
    password = '7777777'
    data = []
    index = 1
    while url is not None:
        html = get_html(url, login, password)
        data.extend(parser(html))
        url = get_next_page(html)
        print("Parsing " + str(index) + " page")
        index += 1
    print("Save file")
    write_to_csv(data)
    end = datetime.now()
    print("Total duration: " + str(end - start))


if __name__ == '__main__':
    main()
