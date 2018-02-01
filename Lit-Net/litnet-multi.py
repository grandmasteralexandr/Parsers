# -*- coding: utf-8 -*-
import requests
import csv
from multiprocessing import Pool
from bs4 import BeautifulSoup
from datetime import datetime


def get_html(url):          # метод получения html кода страницы
    r = requests.get(url)   # подключение к сайту
    # r.encoding = 'UTF-8'    # перекодировка? (не получилось проверить работает ли вообще) по идее не нужна, и так идет в UTF-8
    html = r.text           # получения html
    return html             # возращает html


def get_all_links(html):    # на основе html базовой страницы получаем все ссылки которые нужно спарсить
    pars_url = "https://litnet.com/ru/top/litrpg?alias=litrpg&page="
    s = BeautifulSoup(html, 'lxml')     # передаем html для BeautifulSoup
    page_count = int(s.find('li', class_="last").find('a').text)  # находим общее ко-во стр.
    print("Всего найдено:" + str(page_count) + " стр.")
    all_links = []      # задаем пустой массив куда в цикле будут записыватся ссылки
    for page in range(1, page_count + 1):  # генерим все ссылки на основе к-ва страниц
        link = (pars_url + str(page))
        all_links.append(link)      # добавляем ссылку в масив
    return all_links


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
    with open(fname, 'a', newline='') as csvfile:   # открываем файл на запись
        fieldnames = ['title', 'link', 'rating', 'author', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for row in data:
            writer.writerow(row)    # записываем в цикле строку в файл


def multiprocess(url):  # метод который выполняют множество потоков Pool
    fname = 'result.csv'
    data = []       # задаем основной массив с даннными
    html = get_html(url)    # получаем html нужной страници
    data.extend(parser(html))   # записываем в цикле данные полученые со страници
    write_file(data, fname)     # вызываем сохранения данных в файл


def main():     # основной метод, который все собирает
    start = datetime.now()  # замеряем время начала работы скрипта
    base_url = "https://litnet.com/ru/genre/litrpg"
    html = get_html(base_url)   # получаем html базовой страницы
    all_links = get_all_links(html)     # на основе html базовой страницы получаем все ссылки которые нужно спарсить

    with Pool(6) as p:      # многопоточность 5-6шт. нормально, 10 - уже зависает
        p.map(multiprocess, all_links)  # создает много потоков, которые выполняют ф-ю multiprocess в цикле подставляя каждый раз ссылку из all_links

    end = datetime.now()    # время конца работы скрипта
    print("Готово")
    print("Время работы: " + str(end - start))  # итоговое время работы скрипта


if __name__ == '__main__':  # типовая конструкция необходимая для выполнения любого скрипта
    main()
