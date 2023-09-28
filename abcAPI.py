from abc import ABC, abstractmethod
import time
import json
import requests


class AbcAPI(ABC):
    """ Абстрактный класс для API классов"""

    def __init__(self):
        self.params = {}
        self.url = None
        self.headers = {}

    @abstractmethod
    def get_vacancies(self, find_vacancy: str):
        """
        Абстрактный метод для определения процедуры получения вакансий
        :param find_vacancy: наименование вакансии
        """
        pass

    def get_all(self, pages: int = None, name_block: str = None) -> list:
        """
        Процедура получения всех данных с определенного ресурса
        :param pages: количество страниц для обработки
        :param name_block: наименование блока в котором находится вакансия
        :return: возвращает список словарей с вакансиями
        """
        data = []

        for page in range(0, int(pages)):
            raw = json.loads(self.get_page(page))

            data.extend(raw[str(name_block)])

            if len(data) < 100:
                break

            time.sleep(1)

        return data

    def get_page(self, page: int) -> str:
        """
        Процедура получения одной страницы с определенного ресурса
        :param page: номер страницы
        :return: возвращает список словарей с вакансиями заданной страницы
        """
        try:
            self.params["page"] = int(page)
            response = requests.get(self.url + "vacancies", params=self.params, headers=self.headers)
            if response.status_code == 200:
                data = response.content.decode()
                response.close()
        except:
            print(f"[{self.url}]. Запрашиваемая страница [{page}] не найдена")
        finally:
            return data
