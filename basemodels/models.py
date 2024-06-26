class Employee:

    def __init__(self, id: int, pin: int, time: float = None, rounds: int = None, name: str = None, admin: bool = False):
        self.id = id
        self.pin = pin
        self.time = time
        self.rounds = rounds
        self.name = name
        self.admin = admin

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "pin": self.pin,
            "time": self.time,
            "rounds": self.rounds,
            "name": self.name,
            "admin": self.admin
        }


class Article:

    def __init__(self, id: int, expires: str, ean: str):
        self.id = id
        self.expires = expires
        self.ean = ean

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "expires": self.expires,
            "ean": self.ean
        }
