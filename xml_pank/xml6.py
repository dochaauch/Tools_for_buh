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
def parse_element(element, path='', transaction=None):
    if transaction is None:
        transaction = {}

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

            if 'Ntry' in path:
                transaction[tag] = value
        else:
            parse_element(child, path=f"{path}.{tag}" if path else tag, transaction=transaction)

            if 'Ntry' in path:
                dict_to_use = transaction_dict
                if 'Ntry' in dict_to_use:
                    dict_to_use['Ntry'].append(transaction)
                else:
                    dict_to_use['Ntry'] = [transaction]

# start parsing the XML document
parse_element(root)

# create a pandas dataframe from transaction_dict
df = pd.DataFrame(transaction_dict['Ntry'])

# fill missing values with NaN and replace NaN with None
df = df.fillna(pd.np.nan).replace(pd.np.nan, None)

# print the data
print("General Dict:")
pprint.pprint(general_dict)

print("\nTransaction Dict:")
print(df.to_string())
