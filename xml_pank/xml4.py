import pprint
import xml.etree.ElementTree as ET

# parse the xml file
tree = ET.parse('statement.xml')
root = tree.getroot()

# define the namespace
#ns = {'ns': 'urn:iso:std:iso:20022:tech:xsd:camt.053.001.02'}
ns = {'ns': 'urn:iso:std:iso:20022:tech:xsd:camt.052.001.02'}

# create empty dictionary to store the data
data = {}

# recursively iterate through the xml elements and extract the data
def parse_element(element, path=''):
    for child in element:
        #tag = child.tag.replace('{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}', '')
        tag = child.tag.replace('{urn:iso:std:iso:20022:tech:xsd:camt.052.001.02}', '')
        if child.text:
            value = child.text.strip()
            if path:
                key = f"{path}.{tag}"
            else:
                key = tag
            if key in data:
                data[key].append(value)
            else:
                data[key] = [value]
        else:
            parse_element(child, path=f"{path}.{tag}" if path else tag)

parse_element(root)

# print the data
#for key, value in data.items():
#    print(f"{key}: {value}")
pprint.pprint(data)