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


