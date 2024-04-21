import enum


class Facet(enum.StrEnum):
    author = "author", {"max_occurrences": 10,
                        "hints": True,
                        "matcher": '"[^"]+"',
                        "rule_type": "terms"}
    genre = "genre", {"max_occurrences": 10,
                      "hints": True,
                      "matcher": '"[^"]+"',
                      "rule_type": "terms"}
    year = "year", {"max_occurrences": None,
                    "hints": False,
                    "matcher": r'\d{4}-?\d{4}',
                    "rule_type": "range"}

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

    def mather(self) -> str:
        return self.data.get("matcher")

    def rule(self) -> str:
        return self.data.get("rule_type")

    def make_rule(self, occur_value: str):
        if self.rule() == "terms":
            occur_value = occur_value[1:][:-1]
            return [occur_value]
        elif self.rule() == "range":
            years = occur_value.split("-")
            return {"gte": years[0], "lte": years[1 if len(years) == 2 else 0]}
        raise ValueError(f"Unknown rule type: {self.rule()}")

    def merge_rules(self, fst: dict, snd: dict):
        for rule in fst:
            if rule:
                fst[rule].append(snd[rule])
            if rule in snd:
                self.merge_rules(fst[rule], snd[rule])

    def update_rule(self, occur_value: str, rule):
        if isinstance(rule, list):
            return rule.append(occur_value[1:][:-1])
        elif isinstance(rule, dict):
            years = occur_value.split("-")
            return {"gte": years[0], "lte": years[1 if len(years) == 2 else 0]}
        raise ValueError(f"Unknown rule type: {rule}")
