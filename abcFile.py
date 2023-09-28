from abc import ABC, abstractmethod
from vacancy import Vacancy
from error_vacancy import ErrorDataTypeVacancy


class AbcFile(ABC):
    """
    Абстрактный класс для определения структуры записи и чтения файлов
    """
    err = ErrorDataTypeVacancy()

    @abstractmethod
    def save_as(self, data: list[Vacancy], file_name: str):
        """
        Абстрактный метод для записи данных
        :param file_name: имя файла
        :param data: данные для записи в виде списка экземпляров класс Vacancy
        :return: должен возвращать файл с данными
        """
        pass

    @abstractmethod
    def save_all_to_cash(self, data: list[Vacancy]):
        """
        Абстрактный метод для записи всех данных в кэш
        :param data: данные для записи в виде списка экземпляров класс Vacancy
        :return: должен возвращать файл с данными
        """
        pass

    @abstractmethod
    def load_vacancies(self):
        """
        Абстрактный метод для загрузки данных из файла
        :return: возвращает список экземпляров класса Vacancy
        """
        pass

    def save_vacancies(self, data: list[Vacancy], mode: str = "w"):
        """
        Процедура создает (перезаписывает имеющийся) или добавляет записи в файл
        :param mode: режим записи 'w' - запись нового файла или перезапись существующего, 'a' - добавление записей
         в существующий файл
        :param data: список экземпляров класса Vacancy
        """
        if mode is None:
            raise TypeError("Не указан режим записи данных.")

        self.err.ErrorDataType(data)  # проверка данных на соответствие

        if mode.lower() == 'w':
            self.save_all_to_cash(data)

        if mode.lower() == "a":
            data_temp = self.load_vacancies()
            data_temp.extend(data)
            self.save_all_to_cash(data_temp)

    def delete_vacancy(self, vacancy: Vacancy):
        """
        Удаление заданного элемента
        :param vacancy: Экземпляр класса Vacancy для удаления
        """
        if isinstance(vacancy, Vacancy):
            data = self.load_vacancies()
            data.remove(vacancy)
            self.save_vacancies(data)
        else:
            raise TypeError("Аргумент [vacancy] принимается только как экземпляр класса Vacancy")

    def delete_vacancy_by_id(self, id_vacancy: str):
        """
        Удаление вакансии по ID. Удаляется первая найденная вакансия
        :param id_vacancy: код вакансии
        """
        data = self.load_vacancies()
        index = 0

        for item in data:
            if item.id_vacancy == str(id_vacancy):
                break
            index += 1
        data.pop(index)

        self.save_vacancies(data)

    @staticmethod
    def filter_vacancies(data: list[Vacancy], filter_word: list[str]):
        """
        Функция возвращает список экземпляров Vacancy выбранных по заданному критерию
        :param data: Список экземпляров Vacancy для фильтрации
        :param filter_word: Список слов или строк
        :return: Список экземпляров класса Vacancy по заданному критерию
        """
        data_temp = []

        err = ErrorDataTypeVacancy()
        err.ErrorDataType(data)  # проверка данных на соответствие

        if len(data) > 0 and len(filter_word) > 0:
            for item in data:

                f_in = 0

                for f_string in filter_word:
                    if f_string.lower() not in item.description.lower():
                        continue
                    f_in += 1

                if f_in == len(filter_word):
                    data_temp.append(item)
        return data_temp

    @staticmethod
    def get_top_vacancies(data: list[Vacancy], top: int):
        """
        Функция возвращает ТОП вакансий
        :param data: Список вакансий
        :param top: ТОП значение
        :return: Список ТОП вакансий
        """
        err = ErrorDataTypeVacancy()
        err.ErrorDataType(data)  # проверка данных на соответствие

        data_temp = data.copy()
        data_temp.reverse()
        return data_temp[0:int(top)]

    def get_vacancies_by_salary(self, salary_from: int, salary_to: int, currency: str = None):
        """
        Выбрать вакансии по заданному критерию
        :param salary_from: Зарплата ОТ
        :param salary_to: Зарплата ДО
        :param currency: В ВАЛЮТЕ (Например: RUR)
        :return: Возвращает список вакансий по критерию
        """

        data = self.load_vacancies()
        data_temp = []

        if currency is not None:
            if type(currency) is not str or len(currency) != 3:
                raise TypeError("Валюта только как строка из 3-х символов, например: USD")

        if type(salary_from) == int and type(salary_to) == int:

            for item in data:

                s_from = item.salary_from
                s_to = item.salary_to
                curr = item.currency

                if curr is None:
                    curr = ""

                if s_from is None:
                    s_from = 0

                if s_to is None:
                    s_to = 0

                if currency is None:
                    if s_from in range(salary_from, salary_to + 1) or s_to in range(salary_from, salary_to + 1):
                        data_temp.append(item)
                else:
                    if curr.upper() == currency.upper():
                        if s_from in range(salary_from, salary_to + 1) or s_to in range(salary_from, salary_to + 1):
                            data_temp.append(item)
        else:
            raise TypeError("salary_from и salary_to допускается только как int выражение.")

        return data_temp

    @staticmethod
    def sort_vacancies_by_salary(data: list[Vacancy]):
        """
        Функция сортировки списка вакансий
        :param data: список для сортировки
        :return: отсортированный список
        """
        err = ErrorDataTypeVacancy()
        err.ErrorDataType(data)  # проверка данных на соответствие

        def keys(v: Vacancy):
            ot = v.salary_from
            do = v.salary_to

            if ot == 0 and do > 0:
                return do

            if do == 0 and ot > 0:
                return ot

            if do > 0 and ot > 0:
                return (ot + do) / 2
            else:
                return 0

        sorted_list = sorted(data, key=keys)

        return sorted_list
