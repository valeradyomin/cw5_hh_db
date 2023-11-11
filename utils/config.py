from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    """
    Чтение конфигурационного файла и получение параметров подключения к базе данных.
    """
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Секция {0} не найдена в файле {1}.'.format(section, filename))
    return db
