import requests



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


hh = HeadHunter("https://api.hh.ru/employers/23427")
hh.check_connect()
print(hh.get_employer())
