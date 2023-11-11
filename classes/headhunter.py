import requests
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore", category=UserWarning)


class HeadHunter:
    def __init__(self, employer_id_url):
        self.employer_id_url = employer_id_url
        self.headers = {'User-Agent': 'api-test-agent'}

    def check_connect(self):
        check = requests.get(url=self.employer_id_url, headers=self.headers)
        if check.status_code == requests.codes.ok:
            print(f"соединение с {__class__.__name__} успешно установлено.")
            connect_status = True
            return connect_status
        else:
            print(f"{check.status_code} - ошибка соединения. Программа завершается.")
            exit()

    def get_employer(self):
        raw_data = requests.get(url=self.employer_id_url, headers=self.headers).json()
        return raw_data

    def get_format_employer(self, raw_data):
        fixed = {
            "name": raw_data.get("name", None),
            "description": self.clean_text(raw_data.get("description", None)),
            "site_url": raw_data.get("site_url", None),
        }
        return fixed

    def get_vacancies(self, employer_raw_data):
        url = employer_raw_data.get("vacancies_url", None)
        all_vacancies = []
        page = 0
        per_page = 100
        while True:
            page += 1
            params = {
                "per_page": per_page,
                "page": page,
                "only_with_salary": True,
            }
            vacancies_data = requests.get(url=url, headers=self.headers, params=params).json()
            if "items" in vacancies_data:
                vacancies = vacancies_data["items"]
                all_vacancies.extend(vacancies)
                if len(vacancies) < per_page:
                    break
            else:
                break
        return all_vacancies

    def get_format_vacancies(self, raw_data):
        result = []
        for data in raw_data:
            fixed = {
                "title": data.get("name", None),
                "url": data.get("alternate_url", None),
                "salary_from": data.get("salary", None).get("from", None),
                "salary_to": data.get("salary", None).get("to", None),
                "average_salary": self.get_average_salary(data),
                "currency": self.format_currency(data),
                "requirement": self.clean_text(data.get("snippet", None).get("requirement", None)),
            }
            result.append(fixed)
        return result

    @staticmethod
    def clean_text(string):
        if string:
            soup = BeautifulSoup(string, 'html.parser')
            clean_text = soup.get_text()
            clean_text = clean_text.replace(
                "\xa0", " ").replace(
                "\n", " ").replace(
                "\r  \r \r", " ").replace(
                "<highlighttext>", "").replace(
                "</highlighttext>", "")
            return clean_text
        else:
            return string

    @staticmethod
    def get_average_salary(data):
        salary_from = data.get("salary", {}).get("from", 0)
        salary_to = data.get("salary", {}).get("to", 0)
        if salary_from is None:
            salary_from = 0
        if salary_to is None:
            salary_to = 0
        average_salary = (salary_from + salary_to) / 2
        return round(average_salary)

    @staticmethod
    def format_currency(data):
        currency = data.get("salary", {}).get("currency", 0)
        if currency in ("RUR", "rub"):
            upd_currency = "руб."
            return upd_currency
        else:
            return data.get("salary", None).get("currency", None),


hh = HeadHunter("https://api.hh.ru/employers/23427")
hh.check_connect()
# print(hh.get_format_employer(hh.get_employer()))
# print(hh.get_vacancies(hh.get_employer()))
print(hh.get_format_vacancies(hh.get_vacancies(hh.get_employer())))
