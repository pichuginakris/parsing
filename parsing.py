import requests
import csv
from bs4 import BeautifulSoup


def write_csv_header():  # обновляет файл, добавляя в него заголовки
    with open('work23.csv', 'w', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(('Город', 'Категория', 'ФИО / имя организации', 'Номер телефона', 'Описание профиля',
                         'Адрес', 'Наименование услуги', 'Цена за услугу', 'Описание услуги'))


def write_csv(data):  # записывает данные в файл csv
    print(data)
    with open('work23.csv', 'a', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow((data['city'], data['category'], data['FIO'], data['phone_number'], data['description'],
                         data['address'], data['service_name'], data['price_for_service'], data['service_description']))


def cookie():  # хранит сведения о куки с сайта Яндекс.услуги
    cookies = dict(
        cookies_are='_ym_uid=1562097438760144276; mda=0; fuid01=5d75497528442b76.WJLTwvcBzZPTVSJ81bIDjeXCWAJixGiDH_d_6tyuGIBUM9S_jkvg-nqQDYcNbJH5jB9D9wbAsdajBshn6vcnh8J4Cd2kPUCm4-_neodGg1BTna5iQA2bVBlozVs8uWtG; yandexuid=1186228981561890726; yuidss=1186228981561890726; i=22ZIqAQDyOvlZtJR8D2WIaQCTWi4f4oND2SwA6wwo0McrgNhsMT01PtLfLLhyXHRaeAcdWNpybPd5YX3daNCm9GiiOk=; gdpr=0; ymex=1576788978.oyu.7287139971574196678#1877250726.yrts.1561890726#1889556979.yrtsi.1574196979; bltsr=1; yandex_gid=2; _ym_d=1585174495; font_loaded=YSv1; yabs-frequency=/4/0000000000000000/wrImS6Gw8DhqSd1aEYS0/; skid=7538336611585253025; ar=1586204800329223-744546; prodqad=1; zm=m-stream_ether-desktop-player.css%3As3ether-static_AS4qo3kpCXNmUdFPNay_rRJRF_w%3Al; my=YwA=; yp=1877250726.yrts.1561890726#1889556979.yrtsi.1574196979#1587766494.ygu.1#1590518002.hks.0; VTouhmwR=1; ys=c_chck.2855451005; _ym_isad=1')
    return cookies


def user_agent():  # хранит сведения о юзер агента с сайта Яндекс.услуги
    ua = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.163 Safari/537.36'}
    return ua


def get_number(worker_id):  # получает номер телефона специалиста
    data = '{"data":{"params":{"id":"'+str(worker_id)+'"}}}'  # данные для передачи значений через параметры
    cookies = cookie()
    user_agents = user_agent()
    r = requests.post('https://yandex.ru/uslugi/api/get_worker_phone?ajax=1',
                      data, headers=user_agents,
                      cookies=cookies)
    try:
        num_object = r.json()
    except:  # если номера телефона у специалиста нет
        num_object = {"data": {"phone": "undefined"}, "status": 400, "type": "ydo_backend_response"}
    return num_object


def find_all_workers(url, category, pattern):
    response = requests.get(url)
    j_obj = response.json()
    all_workers = j_obj['search']['params']['pagination']['totalItems']  # количество всех работников
    iteration = all_workers // 10  # общее число страниц (каждая страница хранит по 10 специалистов)
    remainder = all_workers % 10  # вычисление остатка на случай, если число работников не делится всецело на 10
    if remainder > 0:
        iteration = iteration + 1
    i = 0  # номер страницы
    for i in range(iteration):
        url = pattern.format(str(i))
        print(url)
        get_data(url, category)


def get_data(url, job_category):  # собирает всю информацию со страницы
    response = requests.get(url)
    j_obj = response.json()
    category = job_category
    workers_id = j_obj['search']['workerIds']   # список айди всех работников со страницы
    for worker_id in workers_id:
        numb_obj = get_number(worker_id)
        print(numb_obj)
        phone_number = numb_obj['data']['phone']
        description = ''
        try:  # сбор описания профила и разбиения описание на отдельные строки
            descriptions = j_obj['workers']['items'][str(worker_id)]['personalInfo']['description'].split('\n')
        except:
            descriptions = 'undefined'
        index = 0  # индекс строки из списка описаний
        while True:  # собирает элементы из списка descriptions в одну строку description
            try:
                description = description + descriptions[index] + ' '
                index = index + 1
            except:
                break

        description = description.replace('[', '').replace(']', '')  # удаляет [] из описания
        display_name = j_obj['workers']['items'][str(worker_id)]['personalInfo']['displayName']  # ФИО / название
        city_name = []
        i = 0  # счетчик адреса из списка
        address_list = []
        while True:  # пока не закончится список адресов профиля
            try:
                city_name = j_obj['workers']['items'][str(worker_id)]['personalInfo']['addressesList'][i]['cityName']
                address = j_obj['workers']['items'][str(worker_id)]['personalInfo']['addressesList'][i]['address']
                address_list.append(address)  # добавляет новый адрес к общему списку адресов
                i = i+1
            except:
                break
        if city_name == []:  # если специалист не указал город в специальной графе, но поставил пометку на карте
            city_name = j_obj['workers']['items'][str(worker_id)]['personalInfo']['areasList'][0]['name']
        try:  # сбор описания первой услуги
            service_description = j_obj['workers']['items'][str(worker_id)]['occupations'][0]['specializations'][0]['services'][0]['attrs']['description']
        except:  # если описание отсутствует
            service_description = ''
        try:  # наименование первой услуги
            service_name = j_obj['workers']['items'][str(worker_id)]['occupations'][0]['specializations'][0]['services'][0]['attrs']['name']
        except:  # если специалист не добавил первую услугу
            service_name = ''
        try:  # цена за первую услугу
            price_for_service = j_obj['workers']['items'][str(worker_id)]['occupations'][0]['specializations'][0]['services'][0]['attrs']['price']
        except:
            price_for_service = ''
        data = {'city': city_name,
                'category': category,
                'FIO': display_name,
                'phone_number': phone_number,
                'description': description,
                'address': address_list,
                'service_name': service_name,
                'price_for_service': price_for_service,
                'service_description': service_description
                }
        write_csv(data)  # запись информации о специалисте, включающее первую услугу
        k = 1  # счетчик количества услуг
        while True:  # пока не кончится лист услуг
            try:  # проверка на наличие наименования услуги
                service_name = j_obj['workers']['items'][str(worker_id)]['occupations'][0]['specializations'][0]['services'][k]['attrs']['name']
            except:  # если нет наименования услуги, то нет самой услуги
                break
            try:
                service_description = j_obj['workers']['items'][str(worker_id)]['occupations'][0]['specializations'][0]['services'][k]['attrs']['description']
            except:
                service_description = ''
            try:
                price_for_service = j_obj['workers']['items'][str(worker_id)]['occupations'][0]['specializations'][0]['services'][k]['attrs']['price']
            except:
                price_for_service = ''
            data = {'city': city_name,
                    'category': category,
                    'FIO': display_name,
                    'phone_number': phone_number,
                    'description': '',
                    'address': '',
                    'service_name': service_name,
                    'price_for_service': price_for_service,
                    'service_description': service_description
                    }
            write_csv(data)  # запись всех последующих услуг
            k = k+1


def main():
    write_csv_header()
    cookies = cookie()
    user_agents = user_agent()
    url = 'https://yandex.ru/uslugi/2-saint-petersburg/category?rubric=%2Frepetitory-i-obucenie'
    html = requests.get(url, headers=user_agents, cookies=cookies).text
    soup = BeautifulSoup(html, 'lxml')
    reference_headers = soup.find('div', class_='HomeRubricMenu-RubricGroup').find_all('a')  # нахождение заголовков
    for reference_header in reference_headers:
        try:  # нахождение категории из топа услуг
            category = reference_header.find('b').text
        except:
            category = 'None'
        if category == 'None':
            category = reference_header.find('span').text  # нахождение категории из остального списка услуг
        reference = reference_header.get('href')[7:]
        pattern = 'https://yandex.ru/uslugi/api' + reference + '?msp=no&p={}'
        first_page = pattern.format(str(0))
        find_all_workers(first_page, category, pattern)


if __name__ == '__main__':
    main()