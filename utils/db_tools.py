import psycopg2


def create_database(database_name: str, params: dict):
    """
    Создает базу данных и таблицы.
    Args:
        database_name (str): Имя создаваемой базы данных.
        params (dict): Словарь с параметрами подключения к базе данных.
    """

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("SELECT datname FROM pg_catalog.pg_database WHERE datname = %s", (database_name,))
    exists = cur.fetchone()
    if exists:
        cur.execute(f"DROP DATABASE {database_name}")

    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS employers ("
                    "employer_id SERIAL PRIMARY KEY,"
                    "employer_name VARCHAR(100),"
                    "description TEXT,"
                    "site_url VARCHAR(100)"
                    ");")

    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS vacancies ("
                    "vacancy_id SERIAL PRIMARY KEY,"
                    "employer_id INT REFERENCES employers(employer_id),"
                    "vacancy_name varchar(100),"
                    "vacancy_url varchar(100),"
                    "salary_from real,"
                    "salary_to real,"
                    "average_salary real,"
                    "currency varchar(10),"
                    "description text"
                    ");")

    conn.commit()
    conn.close()


def fill_database(data, database_name, params: dict):
    """
    Заполняет базу данных данными о работодателях и вакансиях.
    Args:
        data (list): Список словарей с данными о работодателях и вакансиях.
        database_name (str): Имя базы данных.
        params (dict): Словарь с параметрами подключения к базе данных.
    """

    conn = psycopg2.connect(dbname=database_name, **params)

    if data[0]['vacancies']:
        info = data[0]["employer"]["name"]
        print(f"Заполняю базу данных от компании: {info}")
        with conn.cursor() as cur:
            for employer in data:
                employer_data = employer['employer']
                cur.execute(
                    """
                    INSERT INTO employers (employer_name, description, site_url)
                    VALUES (%s, %s, %s)
                    RETURNING employer_id
                    """,
                    (employer_data['name'], employer_data['description'], employer_data['site_url'])
                )
                employer_id = cur.fetchone()[0]
                vacancies_data = data[0]['vacancies']
                for vacancy in vacancies_data:
                    cur.execute(
                        """
                        INSERT INTO vacancies (employer_id, vacancy_name, vacancy_url, salary_from, salary_to,
                        average_salary, currency, description)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (employer_id, vacancy['title'], vacancy['url'], vacancy["salary_from"], vacancy["salary_to"],
                         vacancy["average_salary"], vacancy["currency"], vacancy["requirement"])
                    )

    conn.commit()
    conn.close()
