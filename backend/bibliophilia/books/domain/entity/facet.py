import enum


class Facet(enum.StrEnum):
    author = "author", {"max_occurrences": 10, "hints": True}
    genre = "genre", {"max_occurrences": 10, "hints": True}
    year = "year", {"max_occurrences": None, "hints": False}

    def __new__(cls, value, data):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.data = data
        return obj

    def __str__(self):
        return str(self.value)

    def max_occurrences(self) -> int:
        return self.data.get("max_occurrences")

    def hints(self) -> bool:
        return self.data.get("hints")
