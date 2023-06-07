import pandas as pd
import xml.etree.ElementTree as ET

# Load the XML file
tree = ET.parse('statement.xml')

# Get the root element
root = tree.getroot()

records = []
for record in root:
    record_dict = {}
    for field in record:
        record_dict[field.tag] = field.text
    records.append(record_dict)

df = pd.DataFrame(records)
print(df)