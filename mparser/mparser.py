from bs4 import BeautifulSoup
from random import choice, uniform
import requests
import os
from time import sleep
from sys import exit


class BeautifulSoupPage(object):
    """
        Класс (функтор) получения объекта Beautiful Soup по url

        Параметры инициализации:

        work_dir - рабочая директория в которой находятся директории useragents и proxies,
        соответственно с файлами: useragents.txt и proxies_http.txt
        По умолчанию это -  директория файла mparser.py.

    """
    def __init__(self, work_dir=None):

        self.__useragents_filename = None
        self.__proxies_http_filename = None

        if not work_dir:
            self.__work_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            self.__work_dir = work_dir

        self.__useragents_filename = os.path.join(self.__work_dir, 'useragents', 'useragents.txt')
        self.__proxies_http_filename = os.path.join(self.__work_dir, 'proxies', 'proxies_http.txt')

        try:
            os.stat(self.__useragents_filename)
            os.stat(self.__proxies_http_filename)
        except FileNotFoundError as e:
            raise e('Не могу открыть файлы useragents.txt или/и proxies_*.txt !')

    def __get_useragent(self):  # Получаем очередной 'User-Agent' из случайной строки файла
        useragents = open(self.__useragents_filename).read().split('\n')
        return {'User-Agent': choice(useragents)}

    def __get_proxies_http(self):  # Получаем http proxies список
        proxies_http = open(self.__proxies_http_filename, 'r').read().split('\n')
        return proxies_http

    def __call__(self, url):  # По url возвращает экземпляр Beautiful Soup object для web страницы

        self.__url = url

        bs_page = None

        proxies_list = self.__get_proxies_http()

        if len(proxies_list[0]) > 0:
            proxies = {
                'http': 'http://' + choice(proxies_list)
            }
        else:
            proxies = None

        sleep(uniform(3.1, 6.1))  # Делаем таймаут из дипазона  3.1с - 6.1с
        try:
            response = requests.get(
                self.__url, headers=self.__get_useragent(), proxies=proxies, timeout=5
            )
            if response.status_code == 200:
                bs_page = BeautifulSoup(response.text, 'lxml')
            else:
                print(
                    'Ошибка доступа к странице. Код: %s ссылка: ' % response.status_code,
                    self.__url if self.__url else 'url не задан'
                )
        except Exception as ex:
            print('Не могу получить страницу по url:', self.__url if self.__url else 'url не задан')
            print(ex)

        return bs_page


# Делаем функцию получения объекта Beautiful Soup по url
get_bs_page = BeautifulSoupPage()  # Вызов get_bs_page(url)


# Получение множества set() с элементами из строк файла (или пустого set(), если нет файла)
def get_set_of_file_lines(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            set_of_file_lines = set((link.strip() for link in f))
    else:
        set_of_file_lines = set()

    return set_of_file_lines


# Добавить строку в файл
def write_line_to_file(file_name, line):
    if file_name and line:
        with open(file_name, 'a') as f:
            f.write(line.strip() + '\n')
    else:
        raise Exception('Не заданы для записи имя файла и/или строка!')


# Добавить строки в файл
def write_lines_to_file(file_name, lines):
    for line in lines:
        write_line_to_file(file_name, line)


# Функция инициирования остановки работы скрипта
# Выход из скрипта будет выполнен, если в директорию stop добавить файл(ы)
def stop_script_if_exists_files_in_stop_directory(work_dir):
    stop_directory = os.path.join(work_dir,  'stop')
    if os.listdir(stop_directory):
        print(
              '\t'*4,
              '===Скрипт остановлен! (--для запуска уберите файлы из директории stop и повторно запустите скрипт--)==='
              )
        exit(0)


class MonsterParser(object):
    """
        Класс парсера www.monster.com

        Параметры инициализации:
            work_dir - рабочая директория парсера (по умолчанию - директория файла mparser.py)

    """
    BASE_CATEGORIES_PAGE = 'https://www.monster.com/jobs/'

    def __init__(self, work_dir=None):

        if not work_dir:
            self.__work_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            self.__work_dir = work_dir

        if not os.path.exists(self.__work_dir):
            raise Exception('Проверьте параметр work_dir!')

        self.__base_categories_links = dict()  # Словарь ссылок на страницы с базовыми категориями

        # Файл с обработанными парсером ссылками основных категорий
        self.__worked_base_categories_links_filename = os.path.join(
            self.__work_dir,  'logs', 'worked_base_categories_links.txt'
        )

        self.__worked_base_categories_links = None  # Обработанные парсером ссылки основных категорий

    def __get_base_categories_links(self):  # Заполняем словарь ссылок на страницы с базовыми категориями
        # Получаем страницу с категориями
        categories_page = get_bs_page(__class__.BASE_CATEGORIES_PAGE)

        if not categories_page:
            print('Не получил ссылку: ', __class__.BASE_CATEGORIES_PAGE)
            return

        # Тэги 'a' ссылок страниц категорий
        categories_tags_a = (
            (
                categories_page.find('span', {'class': 'fa fa-folder-open'}).parent
            ).parent.ul.find_all('a')
        )
        # Формируем словарь ссылок категорий типа:
        for cat_link in categories_tags_a:
            self.__base_categories_links[cat_link.contents[0]] = cat_link.get('href')

    def run(self):

        stop_script_if_exists_files_in_stop_directory(self.__work_dir)

        # Заполняем словарь ссылок на страницы с базовыми категориями
        self.__get_base_categories_links()

        # Заполняем множество обработанных парсером ссылок основных категорий
        self.__worked_base_categories_links = get_set_of_file_lines(self.__worked_base_categories_links_filename)

        # Пробегаем по всем базовым категориям
        for job_category_title, job_category_link in self.__base_categories_links.items():
            # Останавливаем, если надо
            stop_script_if_exists_files_in_stop_directory(self.__work_dir)
            # Если базовая категория не отработана, отрабатываем ее
            if job_category_link not in self.__worked_base_categories_links:
                print('Работаем с категорией:', job_category_title, ' -> ', job_category_link)
                # Формируем списки вакансий
                rjobs = ReadJobsByCategory(job_category_title, job_category_link)
                rjobs.run()
                del rjobs
                # Записываем обработанную ссылку основной категории в соответствующий файл
                write_line_to_file(self.__worked_base_categories_links_filename, job_category_link)


class ReadJobsByCategory(object):
    """
        Параметры инициализации:
            job_category_title - название категории
            job_category_link - ссылка на страницу категории (страницу с подкатегориями)
            work_dir - рабочая директория парсера (по умолчанию - директория файла mparser.py)

    """
    def __init__(self, job_category_title, job_category_link, work_dir=None):

        self.__job_category_title = job_category_title
        self.__job_category_link = job_category_link

        if not work_dir:
            self.__work_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            self.__work_dir = work_dir

        if not os.path.exists(self.__work_dir):
            raise Exception('Проверьте параметр work_dir!')

        # Набор ссылок на страницы с подкатегориями
        self.__sub_categories_links = set()

        # Набор ссылок на все вакансии данной категории, чтобы избежать дублирования
        self.__all_jobs_links_on_job_category = set()

        # Файл со всеми обработанными парсером ссылками
        self.__worked_links_filename = os.path.join(self.__work_dir,  'logs', 'worked_links.txt')

        # Обработанные парсером ссылки вакансий
        self.__worked_links = None

        # Файл с обработанными парсером ссылками подкатегорий
        self.__worked_sub_categories_links_filename = os.path.join(
            self.__work_dir,  'logs', 'worked_sub_categories_links.txt'
        )

        self.__worked_sub_categories_links = None  # Обработанные парсером ссылки подкатегорий

        # Файл со описаниями вакансий
        self.__job_descriptions_filename = os.path.join(self.__work_dir,  'results', 'job_descriptions.txt')

    def __get_sub_categories_link(self):  # Заполняем набор ссылок на страницы с подкатегориями
        # Получаем страницу с подкатегориями
        sub_categories_page = get_bs_page(self.__job_category_link)

        if not sub_categories_page:
            print('Не получил ссылку: ', self.__job_category_link)
            return

        # Ищем тэг 'ul' со ссылками страниц подкатегорий
        sub_categories_ul = sub_categories_page.find('ul', {'class': 'card-columns browse-all'})

        if sub_categories_ul:
            # Ищем тэги 'li' со ссылками страниц подкатегорий
            sub_categories_tags_li = sub_categories_ul.find_all('li')
            # Получаем ссылки и пишем их в self.__sub_categories_links
            for sub_category_li in sub_categories_tags_li:
                self.__sub_categories_links.add(sub_category_li.h2.a.get('href'))
        else:  # Иногда бывает только одна подкатегория
            sub_category_single_a = sub_categories_page.find('h1', {'class': 'section-title'}).a.get('href')
            self.__sub_categories_links.add(sub_category_single_a)

    def run(self):
        # Останавливаем, если надо
        stop_script_if_exists_files_in_stop_directory(self.__work_dir)

        # Получаем ссылки подкатегорий для данной категории
        self.__get_sub_categories_link()

        # Получаем обработанные ранее парсером ссылки вакансий из файла
        self.__worked_links = get_set_of_file_lines(self.__worked_links_filename)

        # Получаем обработанные парсером ссылки подкатегорий из файла
        self.__worked_sub_categories_links = get_set_of_file_lines(self.__worked_sub_categories_links_filename)

        # Проходим по ссылкам подкатегорий, исключая отработанные подкатегории
        for link in self.__sub_categories_links - self.__worked_sub_categories_links:
            # Останавливаем, если надо
            stop_script_if_exists_files_in_stop_directory(self.__work_dir)
            print('\t', 'Работаем с подкатегорией: ', link)
            self.__go_to_sub_category_page(link)

    def __go_to_sub_category_page(self, sub_category_link):
        # Останавливаем, если надо
        stop_script_if_exists_files_in_stop_directory(self.__work_dir)

        sub_category_page = get_bs_page(sub_category_link)

        if not sub_category_page:
            print('Не получил страницу подкатегории: ', sub_category_link)
            return

        # Определяем кол-во страниц подкатегории
        total_pages_input = sub_category_page.find(id="totalPages")
        max_page_num = total_pages_input.get('value') if total_pages_input else None

        # Делаем набор ссылок на страницы подкатегории
        sub_category_pages = set()

        # Если страниц больше 1
        if max_page_num:
            max_page_num = int(max_page_num)
            sub_category_pages = set(
                (sub_category_link + '?page=' + str(page_number) for page_number in range(2, max_page_num + 1))
            )

        # Добавляем начальную страницу (без индекса)
        sub_category_pages.add(sub_category_link)

        # Проходим по всем страницам подкатегории
        for sub_category_page_link in sub_category_pages:
            # Останавливаем, если надо
            stop_script_if_exists_files_in_stop_directory(self.__work_dir)

            sleep(uniform(1.1, 2.5))  # Делаем таймаут из дипазона  1.1с - 2.5с

            # Получаем ссылки и описания вакансий (~ 20шт) с текущей страницы подкатегории
            job_links_descriptions_dict = \
                self.__get_links_and_descriptions_from_sub_category_page_jobs(sub_category_page_link)
            job_links, job_descriptions = job_links_descriptions_dict.keys(), job_links_descriptions_dict.values()
            # Записываем описание вакансий в файл
            write_lines_to_file(self.__job_descriptions_filename, job_descriptions)
            # Записываем ссылки вакансий в файл отработанных ссылок
            write_lines_to_file(self.__worked_links_filename, job_links)

        # Записываем обработанную подкатегорию в соответствующий файл
        write_line_to_file(self.__worked_sub_categories_links_filename, sub_category_link)

    def __get_links_and_descriptions_from_sub_category_page_jobs(self, jobs_page_link):
        """
            Перемещаемся по ссылкам страницы вакансий и записываем описание вакансий в словарь
            jobs_page_link - ссылка на страницу с вакансиями

        """
        jobs_page = get_bs_page(jobs_page_link)

        if not jobs_page:
            print('Не получил страницу: ', jobs_page_link)
            return dict()

        job_links_on_page = set(
            (
                job_title.a.get('href') for job_title in jobs_page.find(
                'section', id="resultsWrapper").find_all('div', {'class': 'jobTitle'})
            )

        )

        job_links_descriptions_dict = dict()

        # Перемещаемся по ссылкам (исключая отработанные) и записываем описания вакансий в словарь
        for job_link in job_links_on_page - self.__worked_links:

            if not job_link:
                continue

            # job_description = self.__get_job_description(job_link)

            job_description = 'Description of job on URL -> ' + job_link

            if job_description:
                job_links_descriptions_dict[job_link] = job_description

        return job_links_descriptions_dict

    def __get_job_description(self, job_link):
        job_page = get_bs_page(job_link)

        if not job_page:
            print('Не получил страницу: ', job_link)
            return

        job_description_div = job_page.find('div', id="JobDescription")
        if job_description_div:
            job_description = job_description_div.get_text().strip()
        else:
            job_description = 'No job description!!! -> link: ' + job_link
            print(job_description)

        return job_description


def main():
    mp = MonsterParser()
    mp.run()


if __name__ == '__main__':
    main()

