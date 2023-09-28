# Настройки для сохранения данных
MENU_MAIN_TITLE = "ПАРСИНГ HeadHanter.ru и SuperJob.ru. Поиск вакансий"
FILE_NAME = "vacancies"
FILE_CODEPAGE = "UTF-8"
FIELDS_NAME = ["id", 'name', 'url', 'salary_from', "salary_to", "currency", "descr"]

# Настройки класса Vacancy
ERR_INIT_STR = "Только строковое значение"
ERR_INIT_INT = "Только целое числовое значение"

# Настройки API HH.RU
HH_URL = "https://api.hh.ru/"
HH_PER_PEGE = 100
HH_COUNT_PAGES = 20
HH_NAME_BLOCK_DATA = "items"

# Настройки API SuperJob.ru
SJ_URL = "https://api.superjob.ru/2.0/"
SJ_PER_PEGE = 100
SJ_COUNT_PAGES = 5
SJ_NAME_BLOCK_DATA = "objects"
SJ_KEY = "v3.r.137841415.8be915b16debcda54dfe6e46487fec29806d4f75.28cf26515363d9ab9e304b78177d5622b242bd81"