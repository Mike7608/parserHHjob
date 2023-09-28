from hhAPI import HeadHunterAPI
from jsonreader import JSONReader
from vacancy import Vacancy
from sjAPI import SuperJobAPI
from settings import settings
from csvreader import CSVReader
from excelreader import ExcelReader


def print_vacancies(data: list[Vacancy]):
    """
    Вывод вакансии на экран
    :param data: список вакансий
    """

    if len(data) > 0:
        index = 1
        for item in data:
            print("--=*", index, "*=--")
            item.print()
            index += 1


def print_title(print_t: bool):
    """ элемент меню """
    if print_t:
        print(settings.MENU_MAIN_TITLE)
    print("=" * len(settings.MENU_MAIN_TITLE))


def get_vacancies(platform: int, find: str):
    """ Функция создает файл со списком вакансий из заданных платформ"""
    hh = HeadHunterAPI()
    sj = SuperJobAPI()

    select_vacancies = []

    print("Идет поиск. Ждите!\n")

    if platform == 1:  # поиск вакансий на HH.ru
        select_vacancies = hh.get_vacancies(find)
    if platform == 2:  # поиск вакансий на SuperJob.ru
        select_vacancies = sj.get_vacancies(find)
    if platform == 3:  # Поиск на обеих платформах
        hh_v = hh.get_vacancies(find)
        sj_v = sj.get_vacancies(find)
        select_vacancies = hh_v + sj_v

    print(f"Получено вакансий: {len(select_vacancies)}\n")

    jsr = JSONReader()
    jsr.save_vacancies(select_vacancies, "w")

    return select_vacancies


def print_total(data: list[Vacancy]):
    """ Вывод количества выбранных вакансий """
    print(f"Всего выбрано выкансий: {len(data)}")


def menu_main():
    """ ГЛАВНОЕ МЕНЮ """
    platforms = ["HeadHunter.ru", "SuperJob.ru"]

    while True:
        print_title(True)
        print_center_menu("Платформа для поиска вакансий")

        for i, item in enumerate(platforms, 1):
            print(f"{i}.", item)

        print("3. Все")
        print("0. Выход из приложения\n")
        select_platform = int(input("> "))

        if select_platform == 0:
            exit()
        else:
            menu_search_query(select_platform)


def menu_search_query(platform: int):
    """ элемент меню """
    print_title(False)
    print_center_menu("Критерии выборки на платформе")
    search_query = str(input("Запрос для выборки вакансий: "))
    sel_vac = get_vacancies(platform, search_query)  # получаем вакансии и сохраняем в файл
    if len(sel_vac) > 0:
        menu_main_sub()
    else:
        return


def menu_sub_1():
    """ Элемент меню """
    print_title(False)
    print_center_menu("Выбрать вакансии по оплате")
    cur = str(input("Валюта оплаты труда (Например: RUR или USD): "))
    ot = int(input("Оплата труда ОТ: "))
    do = int(input("Оплата труда ДО: "))
    jsr = JSONReader()
    data = jsr.get_vacancies_by_salary(ot, do, cur)
    print_total(data)

    if len(data) > 0:
        menu_print(data)
    else:
        return


def menu_print_save(data: list[Vacancy]):
    """ элемент меню """
    while True:
        print_title(False)
        print_center_menu("Вывод ЭКРАН/ФАЙЛ")
        print("1. Вывести на экран")
        print("2. Сохранить в файл")
        print("0. Выход в предыдущее меню")
        sel = int(input("> "))

        if sel == 0:
            return

        if sel == 1:
            print_vacancies(data)

        if sel == 2:
            menu_save(data)


def menu_save(data: list[Vacancy]):
    while True:
        print_title(False)
        print_center_menu("Вывод в ФАЙЛ")
        print("1. Сохранить в JSON формате")
        print("2. Сохранить в Excel формате")
        print("3. Сохранить в CSV формате")
        print("0. Выход в предыдущее меню")
        sel = int(input("> "))

        if sel == 0:
            break

        if sel == 1:
            jsr = JSONReader()
            file_name = str(input("Имя файла: "))
            jsr.save_as(data, file_name)
            print(f"Файл {file_name}.json записан успешно!")

        if sel == 2:
            xlr = ExcelReader()
            file_name = str(input("Имя файла: "))
            xlr.save_as(data, file_name)
            print(f"Файл {file_name}.xlsx записан успешно!")

        if sel == 3:
            csvr = CSVReader()
            file_name = str(input("Имя файла: "))
            csvr.save_as(data, file_name)
            print(f"Файл {file_name}.csv записан успешно!")


def menu_print(data: list[Vacancy]):
    """ элемент меню """
    while True:
        print_title(False)
        print_center_menu("Вывод данных")
        print("1. Вывести все вакансии (без сортировки)")
        print("2. Вывести все вакансии с сортировкой по оплате")
        print("3. Вывести ТОП вакансии")
        print("0. Выход в предыдущее меню")
        sel = int(input("> "))

        jsr = JSONReader()

        if sel == 0:
            break

        if sel == 1:
            menu_print_save(data)

        if sel == 2:
            sort = jsr.sort_vacancies_by_salary(data)
            sort.reverse()
            menu_print_save(sort)

        if sel == 3:
            top = int(input("Сколько вакансий должно входить в ТОП: "))
            sort = jsr.sort_vacancies_by_salary(data)
            top_v = jsr.get_top_vacancies(sort, top)
            menu_print_save(top_v)


def menu_sub_2(data: list[Vacancy]):
    """ элемент меню """
    print_title(False)
    print_center_menu("Выборка данных по ключевым словам")
    words = str(input("Введите слова для выборки: ")).split()
    jsr = JSONReader()
    sel_data = jsr.filter_vacancies(data, words)
    print(f"\n Найдено вакансий по ключевым словам: {len(sel_data)}\n")
    if len(sel_data) > 0:
        menu_print(sel_data)
    else:
        return


def menu_main_sub():
    """ элемент меню """
    while True:
        # os.system('cls')
        print_title(False)
        print_center_menu("Выборка данных")
        print("1. Выбрать вакансии по оплате")
        print("2. Выбрать вакансии по ключевым словам в описании")
        print("0. Выход в предыдущее меню")

        sel = int(input("> "))
        jsr = JSONReader()
        data = jsr.load_vacancies()

        if sel == 0:
            break

        if sel == 1:
            menu_sub_1()

        if sel == 2:
            menu_sub_2(data)


def print_center_menu(text: str):
    """ центрирование строки"""
    print(text.upper().center(len(settings.MENU_MAIN_TITLE)))


def main():

    while True:
        menu_main()


if __name__ == '__main__':
    main()
