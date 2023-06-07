import pprint
import xml.etree.ElementTree as ET

# parse the xml file
tree = ET.parse('statement_short.xml')
root = tree.getroot()

# create empty dictionaries to store the data
data = {}
for child in root:
    for element in child.iter():
        if element.tag not in data:
            data[element.tag] = []

# iterate through the xml elements and extract the data
for child in root:
    for element in child.iter():
        data[element.tag].append(element.text)

# print the data
pprint.pprint(data)