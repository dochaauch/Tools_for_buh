import json
import xmltodict
import pandas as pd
import pprint



# open the input xml file and read
# data in form of python dictionary
# using xmltodict module
from pandas.io.json import json_normalize

with open("statement_short.xml") as xml_file:
    data_dict = xmltodict.parse(xml_file.read())

    json_data = json.dumps(data_dict)

    # Write the json data to output
    # json file
    with open("data.json", "w") as json_file:
        json_file.write(json_data)

    # Use json_normalize() to convert JSON to DataFrame
    dict_ = json.loads(json_data)

pprint.pprint(dict_)

def find_key(key, dictionary, path=''):
    if isinstance(dictionary, dict):
        if key in dictionary:
            yield f'{path}.{key}' if path else key, dictionary[key]
        for k, v in dictionary.items():
            yield from find_key(key, v, f'{path}.{k}' if path else k)
    elif isinstance(dictionary, list):
        for i, item in enumerate(dictionary):
            yield from find_key(key, item, f'{path}[{i}]')


ntry_values = list(find_key("Ntry", data_dict, "Document.BkToCstmrStmt"))
#df = pd.DataFrame.from_dict(dict(ntry_values), orient='index')
#print(df)

#pprint.pprint(ntry_values)
#df = pd.DataFrame(ntry_values)
#print(df.to_string())
#pprint.pprint(ntry_values)