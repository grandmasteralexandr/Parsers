# -*- coding: utf-8 -*-
from random import uniform
from datetime import datetime
from time import sleep
import requests
from bs4 import BeautifulSoup


def open_file(input_file):              # из файла получаем список данных с брендом и партномером в каждом элементе
    with open(input_file, 'r') as file:     # открываем файл
        input_data = [row.strip().split(";") for row in file.readlines()] # считываем в цикле каждую строку и разбиваем бренд и партномер по разделителю ;
        return input_data


def get_html(url):          # метод получения html кода страницы
    r = requests.get(url)   # подключение к сайту
    html = r.text           # получения html
    return html             # возращает html


def search_product_result(html):    # ищем ссылке на основе html полученого при генерации ссылки для поискового запроса
    s = BeautifulSoup(html, 'lxml')     # передаем html для BeautifulSoup
    all_links = s.find('table', class_='v65-productDisplay').find_all_next('a', limit=7)    # находим все теги a после нужной таблици, больше 7 нет смысла брать
    links = []
    for i in all_links:     # перебираем все ссылки и записываем в массив
        if i.get('href') == "#":  # иногда попадаются пустые ссылки такие отсекаем продолжая цикл
            continue
        links.append(i.get('href'))     # если ссылка не пустая добавляем в список
    return links


def check_part_number(html):    # получаем партномер из одного из результата поиска
    s = BeautifulSoup(html, 'lxml')     # передаем html для BeautifulSoup
    try:
        part_number = s.find('span', class_='product_code').text    # ищем партномер
    except:
        part_number = None  # если не находим возращаем null
    return part_number


def get_price(html):    # ищем цену товара
    s = BeautifulSoup(html, 'lxml')     # передаем html для BeautifulSoup
    try:
        price = s.find('span', itemprop='price').text   # ищем цену товара
    except:
        price = "0"     # если не находим то присваеваем 0
    return price


def write_to_file(brand, part_number, result_file, price="0", link="n/a"):    # записываем в файл, если товар не нашло то цену и ссылку запишет значениями по умолчанию
    with open(result_file, 'a') as fl:  # открываем файл
        fl.write(brand + ";" + part_number + ";" + price + ";" + link + "\n")   # записываем полученую строку с разделителем ;


def main():     # главный метод который все собирает
    start = datetime.now()  # время начала работы скрипта
    base_url = 'http://www.trident-supply.com'  # базовый url
    input_file = "input.txt"    # файл с которого берем данные которые нужно спарсить
    result_file = "result.txt"     # файл куда записываем результат
    input_data = open_file(input_file)  # получаем данные которые нужно спарсить
    rand = uniform(1, 3)    # задаем случаейное дробное число чтобы делать паузи перед запросамы, чтобы не забанили
    for i in input_data:    # в цикле перебираем каждую строчку с данными которые нужно спарисить
        brand = i[0]    # нам приходит список из 2-х элементов, бренд идет первым
        part_number = i[1]  # партномер идет 2-м элементом
        # wrong_purt_number = "00001P"    # для теста
        url = base_url + "/SearchResults.asp?Search=" + brand + "+" + part_number + "&Submit="  # формируем ссылку для поиска товара на сайте
        html = get_html(url)    # получаем html страници поиска
        links = search_product_result(html)     # получаем все ссылки на странице поиска
        is_product_find = False     # задаем по умолчанию метку что товар не найден
        sleep(rand)         # пауза
        for link in links:      # перебираем все ссылки найденые при поиске
            html = get_html(link)       # получаем html предполагаемого товара
            sleep(rand)     # пауза
            if part_number == check_part_number(html):      # проверям равняется ли партномер предполагаемого товара тому что мы ищем
                price = (get_price(html)).replace(",", "")      # если да то берем его цену, и убираем запятую если есть USA формат типа 1,259.69
                write_to_file(brand, part_number, result_file, price, link)     # записываем в файл данные
                print(brand, part_number, price, link)      # вывод того что получилось для контроля из консоли
                is_product_find = True      # так как товар нашелся переопределяем флаг что товар найден
                break   # выходим из цикла, другие ссылки нам не нужны
            else:
                continue    # если партномер не равняется тому что мы ищем продолжаем перебирать следуйщие ссылки на предпологаемый товар
        if is_product_find is not True:     # проверяем если товар в предыдущем цикле не был найден, значит ничего не нашло, нужно записать данные по умолчанию
            write_to_file(brand, part_number, result_file)     # записываем данные по умолчанию, цена и ссылка по умолчанию оперделены в методе записи в файл, их передавать не обязательно
            print(brand, part_number + " Not found")    # выводим в консоли что товар не нашло
    end = datetime.now()    # время работы конца скрипта
    print("Готово")
    print("Время работы: " + str(end - start))


if __name__ == '__main__':
    main()
