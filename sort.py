import csv


def write_csv_header():  # обновляет файл, добавляя в него заголовки
    with open('work.csv', 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(('Город', 'Категория', 'ФИО / имя организации', 'Номер телефона', 'Ссылка на профиль',
                         'Описание профиля', 'Адрес', 'Услуга', 'Вконтакте', 'Инстаграм', 'Профи', 'Ютуб', 'Юдо',
                         'Одноклассники'))


def write_sort(sorted_list):  # записывает в файл отсортированный список
    write_csv_header()
    with open('work.csv', 'a', encoding='utf8', newline='') as file:
        i = 0

        while i < (len(sorted_list)-1):
            services = str(sorted_list[i]['Услуга'].split('\\n'))  # удаление лишних знаков в услугах
            services = services.replace('[', '').replace(']', '').replace('\'', '').replace('"', '')
            services = services.replace('\,', '').replace('\Ц', 'Ц').replace('\У', 'У').replace('\О', 'О')
            address = str(sorted_list[i]['Адрес']).replace('[', '').replace(']', '')
            category = sorted_list[i]['Категория']
            while sorted_list[i]['ФИО / имя организации'] == sorted_list[i+1]['ФИО / имя организации']:  # проверяет повтор имени в списке
                if sorted_list[i]['Категория'] != sorted_list[i+1]['Категория']:  # записывает новые категории для специалиста в список
                    category = category + ', ' + sorted_list[i+1]['Категория']
                    i = i + 1
            writer = csv.writer(file)
            writer.writerow(
                (sorted_list[i]['Город'], str(category), sorted_list[i]['ФИО / имя организации'],
                 sorted_list[i]['Номер телефона'], sorted_list[i]['Ссылка на профиль'],
                 sorted_list[i]['Описание профиля'], address, services,
                 sorted_list[i]['Вконтакте'], sorted_list[i]['Инстаграм'],
                 sorted_list[i]['Профи'], sorted_list[i]['Ютуб'], sorted_list[i]['Юдо'],
                 sorted_list[i]['Одноклассники']))
            i = i + 1
        writer = csv.writer(file)  # запись последнего члена списка, который не вошел в цикл
        writer.writerow(
            (sorted_list[i]['Город'], sorted_list[i]['Категория'], sorted_list[i]['ФИО / имя организации'],
             sorted_list[i]['Номер телефона'], sorted_list[i]['Ссылка на профиль'],
             sorted_list[i]['Описание профиля'],address, services,
             sorted_list[i]['Вконтакте'], sorted_list[i]['Инстаграм'],
             sorted_list[i]['Профи'], sorted_list[i]['Ютуб'], sorted_list[i]['Юдо'],
             sorted_list[i]['Одноклассники']))


def read_csv():  # сортирует полученный список по имени и городу
    with open('work_0.csv', encoding='utf8') as f:
        reader = csv.DictReader(f)
        sorted_list = sorted(reader, key=lambda row: (row['ФИО / имя организации']), reverse=False)
        sorted_list = sorted(sorted_list, key=lambda row: (row['Город']), reverse=False)
    write_sort(sorted_list)


def main():
    read_csv()


if __name__ == '__main__':
    main()