import json
import os
from abc import ABC, abstractmethod


class FileHandler(ABC):
    """Абстрактный класс для работы с файлами."""
    @abstractmethod
    def add_vacancy(self, data):
        """Добавление вакансии в файл."""
        pass

    @abstractmethod
    def delete_vacancy(self, data):
        """Удаление вакансии из файла."""
        pass


class JSONSaver(FileHandler):
    """Класс для работы с JSON-файлами."""
    def __init__(self, file_name: str = "data/vacancies.json"):
        self.__file_name = file_name

    def _read_file(self):
        """Чтение файла."""
        if not os.path.exists(self.__file_name):
            return []
        with open(self.__file_name, "r", encoding="utf-8") as file:
            return json.load(file)

    def _write_file(self, data):
        """Запись данных в файл."""
        with open(self.__file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy):
        """Добавление вакансии в файл."""
        data = self._read_file()
        if vacancy.to_dict() not in data:
            data.append(vacancy.to_dict())
            self._write_file(data)

    def delete_vacancy(self, vacancy):
        """Удаление вакансии из файла."""
        data = self._read_file()
        if vacancy.to_dict() in data:
            data.remove(vacancy.to_dict())
            self._write_file(data)
        else:
            print("Вакансия не найдена")

    def get_vacancies(self):
        """Получение всех вакансий из файла."""
        return self._read_file()

    def update_vacancy(self, old_vacancy, new_vacancy):
        """Обновление вакансии в файле."""
        data = self._read_file()
        if old_vacancy.to_dict() in data:
            data.remove(old_vacancy.to_dict())
            data.append(new_vacancy.to_dict())
            self._write_file(data)
        else:
            print("Вакансия не найдена")

    def update_vacancy_file(self, new_vacancies):
        """Обновление файла вакансий."""
        existing_vacancies = self._read_file()
        new_vacancies_dict = [vac.to_dict() for vac in new_vacancies]
        for vacancy in new_vacancies_dict:
            if vacancy not in existing_vacancies:
                existing_vacancies.append(vacancy)
        self._write_file(existing_vacancies)
