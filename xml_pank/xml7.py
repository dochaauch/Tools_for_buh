import pprint
import xml.etree.ElementTree as ET
import pandas as pd

# parse the xml file
tree = ET.parse('statement.xml')
root = tree.getroot()

# define the namespace
ns = {'ns': 'urn:iso:std:iso:20022:tech:xsd:camt.052.001.02'}

def parse_element(element, path='', transaction_list=None):
    for child in element:
        tag = child.tag.replace('{urn:iso:std:iso:20022:tech:xsd:camt.052.001.02}', '')
        print("0", tag)

        if child.text:
            value = child.text.strip() if child.text else None
            if path:
                key = f"{path}.{tag}"
            else:
                key = tag
            print("1", key, tag)
            if '.Ntry.' in key:
                if not transaction_list:
                    transaction_list = []
                print(key, tag)
                if tag == 'NtryRef':
                    transaction_dict = {}
                    transaction_list.append(transaction_dict)
                if transaction_dict is not None:
                    transaction_dict[tag] = value
            else:
                if key in general_dict:
                    general_dict[key].append(value)
                else:
                    general_dict[key] = [value]
        else:
            parse_element(child, path=f"{path}.{tag}" if path else tag, transaction_list=transaction_list)


general_dict = {}
transaction_list = []
parse_element(root, transaction_list=transaction_list)

pprint.pprint(general_dict)