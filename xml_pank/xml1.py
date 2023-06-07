import pandas as pd
import xml.etree.ElementTree as ET


# Load the XML data
tree = ET.parse('statement_short.xml')
root = tree.getroot()

# Define a function to extract data from the XML elements
def extract_data(elem):
    data = {}
    for child in elem:
        if len(child) == 0:
            data[child.tag] = child.text
        else:
            data[child.tag] = extract_data(child)
    return data

# Extract the data from the XML and create a DataFrame
data = []
for elem in root:
    data.append(extract_data(elem))
df = pd.DataFrame(data)
df1 = pd.read_xml('statement_short.xml')

# Display the DataFrame
print(df1)