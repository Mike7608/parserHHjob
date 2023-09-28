from settings import settings


class VacancyTypeError(TypeError):
    """ Класс для ошибок в классе Vacancy"""
    pass


class Vacancy:
    """
    Класс для работы с данными вакансии
    """
    def __init__(self):
        self.__id_vacancy = self.__name = self.__url = self.__salary_from = self.__salary_to = self.__currency = self.__descr = None

    def add(self, id_vacancy: str, name: str, url: str, salary_from: int, salary_to: int, currency: str, descr: str):
        """ Вносит данные в определенный экземпляр класс"""
        self.id_vacancy = id_vacancy
        self.name = name
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.description = descr

    @property
    def id_vacancy(self) -> str:
        """ id вакансии (обязательный параметр если требуется удалять данные по ключу из списка вакансий) """
        return self.__id_vacancy

    @id_vacancy.setter
    def id_vacancy(self, value: str):
        if type(value) == str:
            self.__id_vacancy = value
        else:
            raise VacancyTypeError(settings.ERR_INIT_STR)

    @property
    def name(self) -> str:
        """ Наименование вакансии """
        return self.__name

    @name.setter
    def name(self, value: str):
        if type(value) == str:
            self.__name = value
        else:
            raise VacancyTypeError(settings.ERR_INIT_STR)

    @property
    def url(self) -> str:
        """ Ссылка на вакансию"""
        return self.__url

    @url.setter
    def url(self, value: str):
        if type(value) == str:
            if value[0:6] == "https:" or value[0:5] == "http:":
                self.__url = value
            else:
                raise VacancyTypeError("Данная строка не является ссылкой")
        else:
            raise VacancyTypeError(settings.ERR_INIT_STR)

    @property
    def salary_from(self) -> int:
        """ Зарплата от """
        return self.__salary_from

    @salary_from.setter
    def salary_from(self, value: int):
        if type(value) == int or value is None:
            self.__salary_from = value
        else:
            raise VacancyTypeError(settings.ERR_INIT_INT)

    @property
    def salary_to(self) -> int:
        """ Зарплата до """
        return self.__salary_to

    @salary_to.setter
    def salary_to(self, value: int):
        if type(value) == int or value is None:
            self.__salary_to = value
        else:
            raise VacancyTypeError(settings.ERR_INIT_INT)

    @property
    def currency(self) -> str:
        """ Валюта вакансии (например: USD) """
        return self.__currency

    @currency.setter
    def currency(self, value: str):
        if type(value) == str or value is None:
            self.__currency = value
        else:
            raise VacancyTypeError(settings.ERR_INIT_STR)

    @property
    def description(self) -> str:
        """ Описание вакансии (работы) """
        return self.__descr

    @description.setter
    def description(self, value: str):
        if type(value) == str:
            self.__descr = value
        else:
            raise VacancyTypeError(settings.ERR_INIT_STR)

    def __eq__(self, other):
        """ Переопределяем метод сравнения (==) экземпляра класса вакансий """
        if not isinstance(other, Vacancy):
            raise VacancyTypeError("Операнд справа должен иметь тип Vacancy")

        return self.salary_to == other.salary_to and self.salary_from == other.salary_from

    def print(self):
        """
        Вывод на экран текущей вакансии
        """
        print("Код:", self.id_vacancy)
        print("Наименование:", self.name)
        print("URL:", self.url)
        if self.salary_from is not None and self.salary_from > 0:
            print("Оплата от:", self.salary_from)
        if self.salary_to is not None and self.salary_to > 0:
            print("Оплата до:", self.salary_to)
        if self.currency is not None:
            print("Валюта:", self.currency)
        print("Описание:", self.description)
        print()

    def to_dict(self) -> dict:
        """
        Возвращает библиотеку данных текущей вакансии из экземпляра класса
        :return: словарь с данными текущей вакансии
        """
        return {"id": self.id_vacancy, "name": self.name, "url": self.url, "salary_from": self.salary_from,
                "salary_to": self.salary_to, "currency": self.currency, "descr": self.description}

    def from_dict(self, data: dict):
        """
        Возвращает вакансию как экземпляр класса
        :param data: данные как dict
        :return: экземпляр класса
        """
        self.id_vacancy = data["id"]
        self.name = data["name"]
        self.url = data["url"]
        self.salary_from = data["salary_from"]
        self.salary_to = data["salary_to"]
        self.currency = data["currency"]
        self.description = data["descr"]

        return self

    def __repr__(self):
        return (f"Vacancy {{'id': {self.id_vacancy}, 'name': {self.name}, 'url': {self.url}, " 
                f"'salary_from': {self.salary_from}, 'salary_to': {self.salary_to}, 'currency': {self.currency}, "
                f"'descr': {self.description}}}")

    def __str__(self):
        return (f"Vacancy({self.id_vacancy}, {self.name}, {self.url}, {self.salary_from}, {self.salary_to}, "
                f"{self.currency}, {self.description})")

