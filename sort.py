import csv
import operator
from collections import defaultdict


def write_csv_header():  # обновляет файл, добавляя в него заголовки
    with open('work23.csv', 'w', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(('Город', 'Категория', 'ФИО / имя организации', 'Номер телефона', 'Описание профиля',
                         'Адрес', 'Наименование услуги', 'Цена за услугу', 'Описание услуги'))


def write_sort(sorted_list):
    write_csv_header()
    with open('work23.csv', 'a', encoding='utf8') as file:
        for i in sorted_list:
            if i['Город'] != '':
                print(i['Город'])
                writer = csv.writer(file)
                writer.writerow((i['Город'], i['Категория'], i['ФИО / имя организации'], i['Номер телефона'],
                                i['Описание профиля'], i['Адрес'], i['Наименование услуги'],
                                i['Цена за услугу'], i['Описание услуги']))


def read_csv():
    with open('work2.csv', encoding='utf8') as f:
        reader = csv.DictReader(f)
        sorted_list = sorted(reader, key=lambda row: (row['Город']), reverse=False)
    write_sort(sorted_list)


def main():
    read_csv()


if __name__ == '__main__':
    main()