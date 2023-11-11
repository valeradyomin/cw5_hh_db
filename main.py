from classes.dbmanager import DBManager
from classes.headhunter import HeadHunter
from utils.db_tools import create_database, fill_database
from utils.config import config
params = config()


def main():
    employers_url_lst = ["https://api.hh.ru/employers/78638",  # Tinkoff
                         "https://api.hh.ru/employers/23427",  # РЖД
                         "https://api.hh.ru/employers/2180",  # OZON
                         "https://api.hh.ru/employers/84585",  # AVITO
                         "https://api.hh.ru/employers/3529",  # Sber
                         "https://api.hh.ru/employers/1740",  # Yandex
                         "https://api.hh.ru/employers/4934",  # BeeLine
                         "https://api.hh.ru/employers/3776",  # МТС
                         "https://api.hh.ru/employers/89117",  # Триколор
                         "https://api.hh.ru/employers/1942336",  # Перекресток
                         "https://api.hh.ru/employers/907345"]  # ЛУКОЙЛ

    create_database("headhunter", params)

    hh = HeadHunter(employers_url_lst[0])
    hh.check_connect()

    for url in employers_url_lst:
        hh = HeadHunter(url)
        fill_database(hh.get_unite_data_for_db(), "headhunter", params)

    db = DBManager("headhunter")
    print(db.get_companies_and_vacancies_count())
    # print(db.get_all_vacancies())
    # print(db.get_avg_salary())
    # print(db.get_vacancies_with_higher_salary())
    # print(db.get_vacancies_with_keyword("devops"))


if __name__ == '__main__':
    main()
