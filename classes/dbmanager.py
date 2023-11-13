import psycopg2
from utils.config import config
params = config()


class DBManager:
    """Класс для работы с базой данных."""

    def __init__(self, database_name):
        """
        Инициализация объекта класса DBManager.
        """
        self.conn = psycopg2.connect(dbname=database_name, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        try:
            with self.conn:
                self.cur.execute("SELECT employer_name, COUNT(employer_id) AS vacancies_count "
                                 "FROM employers "
                                 "JOIN vacancies USING(employer_id) "
                                 "GROUP BY employer_id "
                                 "ORDER BY employer_id")
                data = self.cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        # self.conn.close()
        return data

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        try:
            with self.conn:
                self.cur.execute("SELECT employer_name, vacancy_name, average_salary, vacancy_url "
                                 "FROM employers "
                                 "JOIN vacancies USING(employer_id)")
                data = self.cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        # self.conn.close()
        return data

    def get_avg_salary(self, currency="руб."):
        """
        Получение средней зарплаты для каждого работодателя с учетом валюты(по дефолту рубли).
        """
        try:
            with self.conn:
                self.cur.execute(f"""SELECT employer_name, ROUND(AVG(average_salary)) AS employer_avg_salary
                                 FROM employers
                                 JOIN vacancies USING(employer_id)
                                 WHERE currency = '{currency}'
                                 GROUP BY employer_name
                                 ORDER BY employer_avg_salary DESC""")
                data = self.cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        # self.conn.close()
        return data

    def get_vacancies_with_higher_salary(self, currency="руб."):
        """
        Получает список всех вакансий, у которых зарплата(по дефолту рубли) выше средней по всем вакансиям.
        """
        try:
            with self.conn:
                self.cur.execute(f"""SELECT employer_name, vacancy_name, average_salary
                                 FROM vacancies
                                 JOIN employers USING(employer_id)
                                 WHERE vacancies.currency = '{currency}'
                                 GROUP BY employer_name, vacancy_name, average_salary
                                 HAVING average_salary > (SELECT ROUND(AVG(average_salary)) FROM vacancies)
                                 ORDER BY average_salary DESC""")
                data = self.cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        # self.conn.close()
        return data

    def get_vacancies_with_keyword(self, keyword):
        """
        Получение вакансий, содержащих указанное ключевое слово.
        """
        try:
            with self.conn:
                self.cur.execute(f"""SELECT *
                                 FROM vacancies
                                 WHERE lower(vacancy_name) LIKE '%{keyword}%'
                                 OR lower(vacancy_name) LIKE '%{keyword}'
                                 OR lower(vacancy_name) LIKE '{keyword}%'""")
                data = self.cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        # self.conn.close()
        return data
