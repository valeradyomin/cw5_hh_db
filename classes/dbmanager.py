import psycopg2
from utils.config import config
params = config()


class DBManager:
    def __init__(self, database_name):
        self.conn = psycopg2.connect(dbname=database_name, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
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
        self.conn.close()
        return data

    def get_all_vacancies(self):
        try:
            with self.conn:
                self.cur.execute("SELECT employer_name, vacancy_name, average_salary, vacancy_url "
                                 "FROM employers "
                                 "JOIN vacancies USING(employer_id)")
                data = self.cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        self.conn.close()
        return data

    def get_avg_salary(self):
        try:
            with self.conn:
                self.cur.execute("SELECT employer_name, ROUND(AVG(average_salary)) AS employer_avg_salary "
                                 "FROM employers "
                                 "JOIN vacancies USING(employer_id) "
                                 "GROUP BY employer_name "
                                 "ORDER BY employer_avg_salary DESC;")
                data = self.cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        self.conn.close()
        return data

    def get_vacancies_with_higher_salary(self):
        try:
            with self.conn:
                self.cur.execute("SELECT employer_name, vacancy_name, average_salary "
                                 "FROM vacancies "
                                 "JOIN employers USING(employer_id) "
                                 "WHERE average_salary > (SELECT ROUND(AVG(average_salary)) FROM vacancies) "
                                 "ORDER BY average_salary DESC")
                data = self.cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        self.conn.close()
        return data

    def get_vacancies_with_keyword(self, keyword):
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
        self.conn.close()
        return data
