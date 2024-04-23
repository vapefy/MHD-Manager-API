from database.db import ORM
from basemodels.models import *


class APIHelper:
    TABLE = "api_key"

    def __init__(self):
        self.db = ORM()

    def get_keys(self) -> list[str] | None:
        ret = self.db.read_from_table(self.TABLE)
        return [x[0] for x in ret]

    def add_key(self, key: str) -> bool:
        if not self.key_exists(key):
            data = {"key": key}
            self.db.write_to_table(self.TABLE, data)
            return True
        return False

    def delete_key(self, key: str) -> bool:
        if self.key_exists(key):
            self.db.remove_from_table(self.TABLE, "key", key)
            return True
        return False

    def key_exists(self, key: str) -> bool:
        return self.db.exists_entry(self.TABLE, "key", key)


class EmployeeHelper:
    TABLE = "employee"

    def __init__(self):
        self.db = ORM()

    def to_employee(self, x):
        return Employee(x[0], x[1], x[2], x[3], x[4])

    def get_employees(self, employee_id: int = None) -> Employee | list[Employee] | None:
        if not employee_id:
            ret = self.db.read_from_table(self.TABLE)
            return [self.to_employee(x) for x in ret]
        else:
            if self.employee_exists(employee_id):
                ret = self.db.read_from_table(self.TABLE, "employee_id", employee_id)
                print(ret)
                return self.to_employee(ret[0])
            return None

    def add_employee(self, employee: Employee) -> bool:
        if not self.employee_exists(employee.id):
            data = {"employee_id": employee.id, "pin": employee.pin, "time": employee.time,
                    "rounds": employee.rounds, "name": employee.name}
            self.db.write_to_table(self.TABLE, data)
            return True
        return False

    def delete_employee(self, employee_id: int) -> bool:
        if self.employee_exists(employee_id):
            self.db.remove_from_table(self.TABLE, "employee_id", employee_id)
            return True
        return False

    def update_employee(self, employee: Employee) -> bool:
        if self.employee_exists(employee.id):
            data = {"pin": employee.pin, "time": employee.time,
                    "rounds": employee.rounds, "name": employee.name}
            self.db.update_to_table(self.TABLE, data, "employee_id", employee.id)
            return True
        return False

    def employee_exists(self, id: int) -> bool:
        return self.db.exists_entry(self.TABLE, "employee_id", id)


class ArticleHelper:
    TABLE = "article"

    def __init__(self):
        self.db = ORM()

    def to_article(self, x):
        return Article(x[0], x[1], x[2])

    def get_article(self, article_id: int = None) -> Article | list[Article] | None:
        if not article_id:
            ret = self.db.read_from_table(self.TABLE)
            return [self.to_article(x) for x in ret]
        else:
            if self.article_exists(article_id=article_id):
                ret = self.db.read_from_table(self.TABLE, "article_id", article_id)
                print(ret)
                return self.to_article(ret[0])
            return None

    def get_article_by_ean(self, ean: str) -> Article | None:
        ret = self.db.read_from_table(self.TABLE, "ean", ean)
        if len(ret) != 0:
            return self.to_article(ret[0])
        return None

    def add_article(self, article: Article) -> bool:
        if not self.article_exists(article_id=article.id):
            data = {"article_id": article.id, "expires": article.expires, "ean": article.ean}
            self.db.write_to_table(self.TABLE, data)
            return True
        return False

    def delete_article(self, article_id: int) -> bool:
        if self.article_exists(article_id=article_id):
            self.db.remove_from_table(self.TABLE, "article_id", article_id)
            return True
        return False

    def update_article(self, article: Article) -> bool:
        if self.article_exists(article_id=article.id):
            data = {"expires": article.expires}

            self.db.update_to_table(self.TABLE, data, "article_id", article.id)
            return True
        return False

    def article_exists(self, article_id: int = None, ean: str = None) -> bool:
        if article_id and ean is None:
            return self.db.exists_entry(self.TABLE, "article_id", article_id)
        if ean and article_id is None:
            return self.db.exists_entry(self.TABLE, "ean", ean)

