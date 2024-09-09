class Vacancy:
    """Класс для представления вакансии."""
    slots = ("title", "link", "salary_from", "salary_to", "currency", "area", "employer")

    def __init__(
        self,
        title: str,
        link: str,
        salary_from: str = None,
        salary_to: str = None,
        currency: str = "",
        area: str = "",
        employer: str = "",
    ):
        self.title = title
        self.link = self._validate_link(link)
        self.salary_from = self._validate_salary(salary_from)
        self.salary_to = self._validate_salary(salary_to)
        self.currency = currency
        self.area = area
        self.employer = employer

    @staticmethod
    def _validate_salary(salary):
        """Проверка и преобразование зарплаты."""
        if salary is None:
            return None
        if not isinstance(salary, str):
            salary = str(salary)
        if salary.replace(" ", "").replace("-", "").isdigit():
            return salary
        else:
            return None

    @staticmethod
    def _validate_link(link):
        """Проверка и преобразование ссылки."""
        if link is None:
            return None
        if not isinstance(link, str):
            link = str(link)
        if link.startswith("http"):
            return link
        else:
            return None

    @classmethod
    def cast_to_object_list(cls, json_data):
        """Преобразование списка вакансий из JSON в список объектов Vacancy."""
        vacancies = []
        for item in json_data.get("items", []):
            title = item.get("name")
            link = item.get("alternate_url")
            salary = item.get("salary")
            salary_from = salary["from"] if salary else None
            salary_to = salary["to"] if salary else None
            currency = salary["currency"] if salary else ""
            area = item.get("area", {}).get("name")
            employer = item.get("employer", {}).get("name")

            vacancy = cls(title, link, salary_from, salary_to, currency)
            vacancy.area = area
            vacancy.employer = employer
            vacancies.append(vacancy)
        return vacancies

    def to_dict(self):
        """Преобразование объекта Vacancy в словарь."""
        return {
            "title": self.title,
            "link": self.link,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "currency": self.currency,
            "area": self.area,
            "employer": self.employer,
        }

    @staticmethod
    def _convert_salary(salary):
        """Преобразование зарплаты в число."""
        return float(salary) if salary is not None else 0.0

    def __lt__(self, other):
        """Сравнение вакансий по зарплате."""
        return self._convert_salary(self.salary_from) < self._convert_salary(other.salary_from)

    def __le__(self, other):

        return self._convert_salary(self.salary_from) <= self._convert_salary(other.salary_from)

    def __gt__(self, other):
        return self._convert_salary(self.salary_from) > self._convert_salary(other.salary_from)

    def __ge__(self, other):
        return self._convert_salary(self.salary_from) >= self._convert_salary(other.salary_from)

    def __eq__(self, other):
        return self._convert_salary(self.salary_from) == self._convert_salary(other.salary_from)


def print_vacancies(vacancies):
    """Функция для печати списка вакансий."""
    for vacancy in vacancies:
        print(
            f"\nВакансия: {vacancy.title}\n"
            f"Зарплата: {vacancy.salary_from} - {vacancy.salary_to} {vacancy.currency}\n"
            f"Регион: {vacancy.area}\n"
            f"Работодатель: {vacancy.employer}\n"
        )


def filter_vacancies(vacancies, key):
    """Фильтрация вакансий по ключевым словам."""
    return [v for v in vacancies if any(keyword.lower() in (v.title + v.area + v.employer).lower() for keyword in key)]


def get_vacancies_by_salary(vacancies, salary):
    """Фильтрация вакансий по диапазону зарплаты."""
    if "-" not in salary:
        print("Неправильный формат диапазона зарплаты. Пожалуйста, используйте формат 'min-max'.")
        return []

    min_salary, max_salary = map(int, salary.split("-"))

    def is_in_range(value, min_value, max_value):
        """Проверка, находится ли значение в диапазоне."""
        if value is None:
            return False
        try:
            value = int(value.replace(" ", ""))
        except ValueError:
            return False
        return min_value <= value <= max_value

    return [
        v
        for v in vacancies
        if (is_in_range(v.salary_from, min_salary, max_salary) or is_in_range(v.salary_to, min_salary, max_salary))
    ]


def get_top_vacancies(vacancies, top_n):
    """Функция для получения топ-n вакансий."""
    return vacancies[:top_n]


def sort_vacancies(vacancies):
    """Сортировка вакансий по зарплате."""
    def get_salary(v):
        salary_from = int(v.salary_from.replace(" ", "")) if v.salary_from is not None else 0
        salary_to = int(v.salary_to.replace(" ", "")) if v.salary_to is not None else 0
        return salary_from, salary_to

    return sorted(vacancies, key=get_salary, reverse=True)
