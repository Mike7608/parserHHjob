from vacancy import Vacancy


class ErrorDataTypeVacancy(TypeError):
    """
    Класс для проверки типа данных списка вакансий
    """
    @classmethod
    def ErrorDataType(cls, data: list[Vacancy]):
        if len(data) > 0:
            if not isinstance(data[0], Vacancy):
                raise TypeError("Список данных принимается только как экземпляр класс Vacancy")