import re

from backend.bibliophilia.books.domain.entity.facet import Facet


def parse_facets(query: str) -> (str, dict):
    rules_map: {str: {str: dict}} = {"must": {"terms": {}, "range": {}},
                                     "must_not": {"terms": {}, "range": {}}}
    final_query = query
    for facet in Facet:
        fc: Facet = Facet(facet)
        matches = re.findall(f'-?{fc.value}:{fc.mather()}', final_query)
        for occurrence in matches:
            print(f"occurence: {occurrence}")
            final_query = re.sub(re.escape(occurrence), '', final_query)
            match_mode = "must_not" if occurrence[0] == '-' else 'must'
            value = occurrence.split(":")[1]
            if fc.value not in rules_map[match_mode][fc.rule()]:
                rules_map[match_mode][fc.rule()][fc.value] = fc.make_rule(value)
            else:
                rules_map[match_mode][fc.rule()][fc.value] = (
                    fc.update_rule(value, rules_map[match_mode][fc.rule()][fc.value]))
    final_query = ' '.join(final_query.split())
    must = ([{"terms": {arr+".value.key": rules_map["must"]["terms"][arr]}} for arr in rules_map["must"]["terms"]]
            + [{"range": {dictionary: rules_map["must"]["range"][dictionary]}} for dictionary in rules_map["must"]["range"]])
    must_not = ([{"terms": {arr+".value.key": rules_map["must_not"]["terms"][arr]}} for arr in rules_map["must_not"]["terms"]]
                + [{"range": {dictionary: rules_map["must_not"]["range"][dictionary]}} for dictionary in rules_map["must_not"]["range"]])
    print(must)
    print(must_not)
    return final_query, {"bool": {"must": must, "must_not": must_not}}
