# -*- coding: utf-8 -*-
import requests
from datetime import datetime
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    html = r.text
    return html


def parser(html):
    s = BeautifulSoup(html, 'lxml')
    return s


def write_to_file(data, fname):
    with open(fname, 'w') as fl:
        fl.write(data)


def main():
    base_url = 'http://www.trident-supply.com'
    html = get_html(base_url)
    print(parser(html))


if __name__ == '__main__':
    main()
