import pprint

import xmlschema

xs = xmlschema.XMLSchema("camt.053.001.02.xsd")
d = xs.to_dict("statement_short.xml")
#pprint.pprint(d)

def find_key(key, dictionary):
    if isinstance(dictionary, dict):
        if key in dictionary:
            yield dictionary[key]
        for value in dictionary.values():
            yield from find_key(key, value)
    elif isinstance(dictionary, list):
        for item in dictionary:
            yield from find_key(key, item)

ntry_values = list(find_key("Ntry", d))

pprint.pprint(ntry_values)