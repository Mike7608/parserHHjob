from abcAPI import AbcAPI
from vacancy import Vacancy
from settings import settings


class HeadHunterAPI(AbcAPI):
    """ API класс для работы с HH.RU """

    def get_vacancies(self, find_vacancy: str, area: int = None) -> list:
        """
        Процедура получения всех вакансий по наименованию и зоны (регион или город)
        :param find_vacancy: Наименование работы (вакансии). Например: Python
        :param area: Зона (регион или город) где требуется вакансия. Например: 1 - на HH.RU это Москва
        :return: возвращает список найденных вакансий
        """
        self.url = settings.HH_URL
        self.params = {'text': 'NAME:' + str(find_vacancy), 'per_page': settings.HH_PER_PEGE}

        data = []
        data_hh = self.get_all(pages=settings.HH_COUNT_PAGES, name_block=settings.HH_NAME_BLOCK_DATA)

        for item in data_hh:
            v = Vacancy()
            v.id_vacancy = str(item["id"])
            v.name = str(item["name"])
            v.url = str(item["alternate_url"])

            if item["salary"] is not None:
                ot = item["salary"]["from"]
                do = item["salary"]["to"]
                if ot is None:
                    ot = 0
                if do is None:
                    do = 0
                v.salary_from = ot
                v.salary_to = do
                v.currency = item["salary"]["currency"]
            else:
                v.salary_from = 0
                v.salary_to = 0

            v.description = str(item["snippet"]["requirement"]) + "\n" + str(item["snippet"]["responsibility"])

            data.append(v)

        return data
