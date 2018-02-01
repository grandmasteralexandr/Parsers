# -*- coding: utf-8 -*-
import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime


def get_html(url):          # метод получения html кода страницы
    r = requests.get(url)   # подключение к сайту
    # r.encoding = 'UTF-8'    # перекодировка? (не получилось проверить работает ли вообще) по идее не нужна, и так идет в UTF-8
    html = r.text           # получения html
    return html             # возращает html


def get_next_page(html):
    s = BeautifulSoup(html, 'lxml')
    try:
        next_page = "https://litnet.com" + s.find('li', class_="next").find('a').get("href")  # находим следуйщую страницу
    except:
        next_page = None    # если не найдет возвращаем null
    return next_page


def parser(html):                       # метод спарсивания нужных данных
    s = BeautifulSoup(html, 'lxml')     # передаем html для BeautifulSoup
    rows = s.find_all("div", class_='row book-item')        # ищем по html все строки содержащие нужные данные
    data = []               # определяем пустой массив для наших данных

    # в цикле перебираем каждую строку и записываем в переменные конкретные данные, затем записываем его в массив
    for row in rows:
        try:    # конструкция try - except - обработка исключения
            titles = row.find("h4", class_='book-title').find('a').text.strip()     # находим заголовок, вытягиваем текст
            ratings = row.find('div', class_='meta-info').find('p').text.strip()    # находим рейтинг, strip() - обрезает лишнее
            ratings = ratings.replace("Общий рейтинг: ", "")    # удаляем лишнее в строке
            link = "https://litnet.com" + row.find("h4", class_='book-title').find('a').get('href')
            author = row.find("a", class_="author").text.strip()
            price = row.find('div', class_="item-price").text.strip()
            price_exept = "\r\n "   # определяем лишние символы попадающиеся в цене
            price = price.replace("Подписка:", "").replace("Цена:", "")  # удаляем лишнее слово
        except: continue    # если попадается исключение просто продолжаем работу
        for exept in price_exept:               # в цикле убираем лишниие символы
            price = price.replace(exept, "")

        data.append({                           # заполняем словарь
                'title': titles,
                'link': link,
                'rating': ratings,
                'author': author,
                'price': price
        })

    return data


def write_file(data, fname):    # записываем в файл
    with open(fname, 'w', newline='') as csvfile:   # открываем файл на запись
        fieldnames = ['title', 'link', 'rating', 'author', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)    # записываем в цикле строку в файл


def main():     # основной метод, который все собирает
    start = datetime.now()                # замеряем время начала работы скрипта
    url = "https://litnet.com/ru/genre/litrpg"
    fname = 'result.csv'
    data = []                             # задаем основной массив с даннными
    index = 1
    while url is not None:  # в цикле запускаем парсинг страници, передавая ему каждый раз новую страницу
        html = get_html(url)         # получаем html страницы
        data.extend(parser(html))               # записываем в цикле данные полученые со страници
        url = get_next_page(html)        # находим ссылку на новую страницу и начинаем заново, пока не закончатся страници (в url не придет null)
        print("Парсинг " + str(index) + "-й страници")
        index += 1
    print("Сохранение...")
    write_file(data, fname)  # вызываем сохранения данных в файл
    end = datetime.now()    # время конца работы скрипта
    print("Готово")
    print("Время работы: " + str(end - start))  # итоговое время работы скрипта


if __name__ == '__main__':      # типовая конструкция необходимая для выполнения любого скрипта
    main()
