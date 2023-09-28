from abcFile import AbcFile
import json
from vacancy import Vacancy
import os
from settings import settings


class JSONReader(AbcFile):
    """
    Класс для работы с JSON файлами
    """
    file_name_default = settings.FILE_NAME
    cp = settings.FILE_CODEPAGE

    @classmethod
    def save_all_to_cash(cls, data: list[Vacancy]):
        """
        Сохранить все данные в JSON формате в кэш
        :param data: данные для записи
        :return: файл с данными в формате JSON
        """
        cls.save_as(data, cls.file_name_default)

    @classmethod
    def save_as(cls, data: list[Vacancy], file_name: str):
        cls.err.ErrorDataType(data)

        data_temp = []
        for item in data:
            data_temp.append(item.to_dict())

        json_object = json.dumps(data_temp, indent=4, ensure_ascii=False)

        with open(file_name + ".json", 'w', encoding=cls.cp) as file:
            file.write(json_object)

    def load_vacancies(self) -> list[Vacancy]:
        """
        Загрузить JSON-файл
        :return: Список экземпляров класса Vacancy
        """
        data = []
        if os.path.exists(self.file_name_default + ".json"):
            with open(self.file_name_default + ".json", "r", encoding=self.cp) as file:
                data_j = json.load(file)

            for item in data_j:
                v = Vacancy()
                v.from_dict(item)
                data.append(v)

            return data
        else:
            raise FileNotFoundError(f"Файл '{self.file_name_default}.json' не найден.")
