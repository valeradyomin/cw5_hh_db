import psycopg2


def create_database(database_name: str, params: dict):
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
