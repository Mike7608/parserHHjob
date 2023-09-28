from abcAPI import AbcAPI
from vacancy import Vacancy
from settings import settings


class SuperJobAPI(AbcAPI):
    """
    API класс для работы с SuperJob.ru
    """
    def get_vacancies(self, find_vacancy: str):
        """
        Процедура получения всех вакансий по наименованию и зоны (регион или город)
        :param find_vacancy: Наименование работы (вакансии). Например: Python
        :param area: Зона (регион или город) где требуется вакансия. Например: 41 - на SuperJob.ru это Москва
        :return: возвращает список найденных вакансий
        """
        self.url = settings.SJ_URL
        self.params = {'keyword': str(find_vacancy), 'count': settings.SJ_PER_PEGE}
        self.headers = {'X-Api-App-Id': settings.SJ_KEY}

        data = []
        data_obj = self.get_all(pages=settings.SJ_COUNT_PAGES, name_block=settings.SJ_NAME_BLOCK_DATA)

        for item in data_obj:
            v = Vacancy()
            v.id_vacancy = str(item["id"])
            v.name = str(item["profession"])
            v.url = str(item["link"])
            v.salary_from = item["payment_from"]
            v.salary_to = item["payment_to"]
            cur = str(item["currency"])
            if cur.lower() == "rub":
                cur = "RUR"
            v.currency = cur
            v.description = str(item["candidat"])

            data.append(v)

        return data
