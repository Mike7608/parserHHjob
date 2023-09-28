from abcFile import AbcFile
import csv
from vacancy import Vacancy
import os
from settings import settings
from error_vacancy import ErrorDataTypeVacancy


class CSVReader(AbcFile):
    """
    Класс для работы с CSV файлами
    """
    file_name_default = settings.FILE_NAME
    cp = settings.FILE_CODEPAGE

    @classmethod
    def save_all_to_cash(cls, data: list[Vacancy]):
        cls.save_as(data, cls.file_name_default + ".csv")

    @classmethod
    def save_as(cls, data: list[Vacancy], file_name: str):
        """
        Сохранить данные в CSV формате
        :param file_name: имя файла
        :param data: данные для записи
        :return: файл CSV с данными
        """
        cls.err.ErrorDataType(data)  # проверка данных на соответствие

        data_temp = []

        for item in data:
            data_temp.append(item.to_dict())

        with open(file_name + ".csv", 'w', encoding=cls.cp, newline='') as file:
            writer = csv.DictWriter(file, fieldnames=settings.FIELDS_NAME, delimiter='|')
            writer.writeheader()
            writer.writerows(data_temp)

    def load_vacancies(self):
        """
        Загрузить CSV-файл из кэш
        :return: Список экземпляров класса Vacancy
        """
        data = []
        if os.path.exists(self.file_name_default + ".csv"):
            with open(self.file_name_default + ".csv", "r", encoding=self.cp) as file:
                reader = csv.DictReader(file, delimiter='|')
                for row in reader:
                    v = Vacancy()
                    v.id_vacancy = row["id"]
                    v.name = row["name"]
                    v.url = row["url"]
                    v.salary_from = int(row["salary_from"])
                    v.salary_to = int(row["salary_to"])
                    v.currency = row["currency"]
                    v.description = row["descr"]
                    data.append(v)
            return data
        else:
            raise FileNotFoundError(f"Файл '{self.file_name_default}.csv' не найден.")
