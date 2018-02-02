# -*- coding: utf-8 -*-
from random import uniform
from datetime import datetime
from time import sleep
import requests
from bs4 import BeautifulSoup


def open_file(input_file):
    with open(input_file, 'r') as file:
        input_data = [row.strip().split(";") for row in file.readlines()]
        return input_data


def get_html(url):
    r = requests.get(url)
    html = r.text
    return html


def search_product_result(html):
    s = BeautifulSoup(html, 'lxml')
    all_links = s.find('table', class_='v65-productDisplay').find_all_next('a', limit=7)
    links = []
    for i in all_links:
        if i.get('href') == "#":
            continue
        links.append(i.get('href'))
    return links


def check_part_number(html):
    s = BeautifulSoup(html, 'lxml')
    try:
        part_number = s.find('span', class_='product_code').text
    except:
        part_number = None
    return part_number


def get_price(html):
    s = BeautifulSoup(html, 'lxml')
    try:
        price = s.find('span', itemprop='price').text
    except:
        price = "0"
    return price


def write_to_file(brand, part_number, result_file, price="0", link="n/a"):
    with open(result_file, 'a') as fl:
        fl.write(brand + ";" + part_number + ";" + price + ";" + link + "\n")


def main():
    start = datetime.now()
    base_url = 'http://www.trident-supply.com'
    input_file = "input.txt"
    result_file = "res.txt"
    input_data = open_file(input_file)
    rand = uniform(1, 3)
    for i in input_data:
        brand = i[0]
        part_number = i[1]
        # wrong_purt_number = "00001P"    # для теста
        url = base_url + "/SearchResults.asp?Search=" + brand + "+" + part_number + "&Submit="
        html = get_html(url)
        links = search_product_result(html)
        is_product_find = False
        sleep(rand)
        for link in links:
            html = get_html(link)
            sleep(rand)
            if part_number == check_part_number(html):
                price = (get_price(html)).replace(",", "")
                write_to_file(brand, part_number, result_file, price, link)
                print(brand, part_number, price, link)
                is_product_find = True
                break
            else:
                continue
        if is_product_find is not True:
            write_to_file(brand, part_number, result_file)
            print(brand, part_number + " Not found")
    end = datetime.now()
    print("Готово")
    print("Время работы: " + str(end - start))


if __name__ == '__main__':
    main()
