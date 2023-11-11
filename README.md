# Парсер вакансий с сайта `headhunter.ru` с помощью API, который заполняет созданные в БД PostgreSQL таблицы данными о работодателях и их вакансиях.



О проекте
        
    Данный проекте представляет собой инструмент для сбора и анализа данных о работодателях и вакансиях с 
    использованием API HeadHunter. 
    Он позволяет получить информацию о компаниях, вакансиях, средних зарплатах и других параметрах, связанных с рынком труда.

Как запустить проект

    Установите необходимые зависимости,уазанные в файле pyproject.toml.
    Создайте конфигурационный файл database.ini и укажите в нем параметры подключения к базе данных PostgreSQL.
    Создайте базу данных, выполнив функцию create_database("headhunter", params) из файла utils/db_tools.py.
    Запустите скрипт, выполнив функцию main() из файла main.py.


Как работать с проектом

    Для получения данных о компаниях и вакансиях используйте класс HeadHunter из файла classes/headhunter.py. 
    Передайте список URL-адресов работодателей в конструктор класса и вызовите методы для получения нужных данных.
    Для работы с базой данных используйте класс DBManager из файла classes/dbmanager.py. 
    Создайте экземпляр класса, указав имя базы данных, и вызовите соответствующие методы 
    для получения информации о компаниях и вакансиях, средних зарплатах и других параметрах.


Примеры использования методов класса DBManager:

    db = DBManager("headhunter")
    print(db.get_companies_and_vacancies_count()) - получить количество компаний и вакансий в базе данных.
    print(db.get_all_vacancies()) - получить все вакансии из базы данных.
    print(db.get_avg_salary()) - получить среднюю зарплату по вакансиям.
    print(db.get_vacancies_with_higher_salary()) - получить вакансии с зарплатой выше средней.
    print(db.get_vacancies_with_keyword("devops")) - получить вакансии с ключевым словом "devops".
