import pprint
import xml.etree.ElementTree as ET
import pandas as pd

# parse the xml file
tree = ET.parse('statement.xml')
root = tree.getroot()

# define the namespace
ns = {'ns': 'urn:iso:std:iso:20022:tech:xsd:camt.052.001.02'}

# create empty dictionaries to store the data
general_dict = {}
transaction_dict = {}

# recursively iterate through the xml elements and extract the data
def parse_element(element, path=''):
    for child in element:
        tag = child.tag.replace('{urn:iso:std:iso:20022:tech:xsd:camt.052.001.02}', '')

        if child.text:
            value = child.text.strip() if child.text else None
            if path:
                key = f"{path}.{tag}"
            else:
                key = tag
            if 'Ntry' in key:
                dict_to_use = transaction_dict
            else:
                dict_to_use = general_dict
            if key in dict_to_use:
                dict_to_use[key].append(value)
            else:
                dict_to_use[key] = [value]
        else:
            parse_element(child, path=f"{path}.{tag}" if path else tag)

parse_element(root)

# create a list of dictionaries from transaction_dict
rows = []
for i in range(len([k for k in transaction_dict.keys() if 'Ntry' in k])):
    row = {}
    for key in transaction_dict:
        if 'Ntry' in key:
            if len(transaction_dict[key]) > i:
                row[key] = transaction_dict[key][i]
            else:
                row[key] = None
        else:
            row[key] = transaction_dict[key][0]
    rows.append(row)

# create a pandas dataframe from transaction_dict
df = pd.DataFrame(rows)

# fill missing values with NaN and replace NaN with None
df = df.fillna(pd.np.nan).replace(pd.np.nan, None)


# print the data
print("General Dict:")
pprint.pprint(general_dict)
print("\nTransaction Dict:")
print(df.to_string())
