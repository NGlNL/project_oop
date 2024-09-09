from abc import ABC, abstractmethod

import requests


class VacancyAPI(ABC):
    """Абстрактный класс для API вакансий."""
    @abstractmethod
    def _connect(self):
        """Подключение к API вакансий."""
        pass

    @abstractmethod
    def get_vacancies(self, keyword):
        """Получение вакансий по ключевому слову."""
        pass


class HeadHunterAPI(VacancyAPI):
    """Класс для работы с API вакансий."""
    URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        self.__session = requests.Session()

    def _connect(self):
        """Подключение к API вакансий."""
        response = self.__session.get(self.URL)
        if response.status_code == 200:
            return response
        else:
            response.raise_for_status()

    def get_vacancies(self, key):
        """Получение вакансий по ключевому слову."""
        self._connect()
        params = {"text": key, "per_page": 100, "page": 0}
        response = self.__session.get(self.URL, params=params)
        response.raise_for_status()
        return response.json()
