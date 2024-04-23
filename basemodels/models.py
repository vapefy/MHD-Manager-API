class Employee:

    def __init__(self, id: int, pin: int, time: float = None, rounds: int = None, name: str = None):
        self.id = id
        self.pin = pin
        self.time = time
        self.rounds = rounds
        self.name = name

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "pin": self.pin,
            "time": self.time,
            "rounds": self.rounds,
            "name": self.name
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
