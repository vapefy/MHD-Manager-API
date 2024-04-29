from flask_restx import Resource
from functools import wraps
from flask import request, abort

from database.helpers import *


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if api_key in APIHelper().get_keys():
            return f(*args, **kwargs)
        else:
            abort(401, "API key is invalid or missing")
    return decorated


class Employees(Resource):
    employee_helper = EmployeeHelper()
    method_decorators = [require_api_key]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def check_data(self, data) -> (bool, str):
        should = ["pin"]
        names = []
        for element in should:
            if element not in data.keys():
                names.append(element)
        return len(names) == 0, ", ".join(names)

    def get(self, pin: int = None):
        if pin is None:
            return {"employees": [employee.to_dict() for employee in self.employee_helper.get_employees()]}, 200
        else:
            employee = self.employee_helper.get_employees(pin)
            if employee:
                return {employee.pin: employee.to_dict()}, 200
            return {"message": "Employee not found"}, 404

    def post(self):
        data = request.get_json()
        correct, name = self.check_data(data)
        if not correct:
            return {"message": f"Data is invalid. Check {name}"}, 400
        employee_id = data["employee_id"]
        pin = data["pin"]
        employee_name = data["name"] if "name" in data else None
        employee = Employee(id=employee_id, pin=pin, name=employee_name)
        if self.employee_helper.add_employee(employee):
            return {"message": f"Employee {employee_id} has been added"}, 201
        return {"message": f"Employee {employee_id} already exists"}, 405

    def put(self):
        data = request.get_json()
        if "employee_id" in data:
            employee_id = data["employee_id"]
            employee = self.employee_helper.get_employees(employee_id)
            if employee:
                employee.pin = data["pin"] if "pin" in data else employee.pin
                employee.time = employee.time + float(data["time"]) if "time" in data else employee.time
                employee.rounds = employee.rounds + int(data["rounds"]) if "rounds" in data else employee.rounds
                employee.name = data["name"] if "name" in data else employee.name

                self.employee_helper.update_employee(employee)
                return {"message": f"Employee {employee_id} has been updated"}, 201
            return {"message": f"Employee {employee_id} does not exists"}, 405
        return {"message": f"Employee ID missing"}, 400

    def delete(self, employee_id: int):
        if self.employee_helper.delete_employee(employee_id):
            return {"message": f"Employee {employee_id} has been deleted"}, 202
        return {"message": f"Employee {employee_id} does not exist"}, 405


class Articles(Resource):
    article_helper = ArticleHelper()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def check_data(self, data) -> (bool, str):
        should = ["article_id", "expires", "ean"]
        names = []
        for element in should:
            if element not in data.keys():
                names.append(element)
        return len(names) == 0, ", ".join(names)

    def get(self, article_id_ean: str = None):
        if article_id_ean is None:
            return {"articles": [employee.to_dict() for employee in self.article_helper.get_article()]}, 200
        else:
            typ = article_id_ean.split("SP")
            employee = None
            if typ[0] == "articleid":
                employee = self.article_helper.get_article(int(typ[1]))
                if employee is None:
                    return {"message": "Article does not exist"}, 405
            elif typ[0] == "ean":
                employee = self.article_helper.get_article_by_ean(typ[1])
                if employee is None:
                    return {"message": "Article does not exist"}, 405
            return {employee.id: employee.to_dict()}, 200

    def post(self):
        data = request.get_json()
        correct, name = self.check_data(data)
        if not correct:
            return {"message": f"Data is invalid. Check {name}"}, 400
        article_id = data["article_id"]
        expires = data["expires"]
        ean = data["ean"]
        article = Article(id=article_id, expires=expires, ean=ean)
        if self.article_helper.add_article(article):
            return {"message": f"Article {article_id} has been added"}, 201
        return {"message": f"Article {article_id} already exists"}, 405

    def put(self):
        data = request.get_json()
        if "article_id" in data:
            if "expires" in data:
                article_id = data["article_id"]
                article = self.article_helper.get_article(article_id)
                if article:
                    article.expires = data["expires"]

                    self.article_helper.update_article(article)
                    return {"message": f"Article {article_id} has been updated"}, 201
                return {"message": f"Article {article_id} does not exists"}, 405
            return {"message": f"Expire date missing"}, 400
        return {"message": f"Employee ID missing"}, 400

    def delete(self, article_id: int):
        if self.article_helper.delete_article(article_id):
            return {"message": f"Article {article_id} has been deleted"}, 202
        return {"message": f"Article {article_id} does not exist"}, 405
