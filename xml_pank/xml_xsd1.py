import pprint

import xmlschema

# # Load the XSD files
# camt053_xsd = xmlschema.XMLSchema('camt.053.001.02.xsd')
# camt052_xsd = xmlschema.XMLSchema('camt.052.001.02.xsd')
#
# # Load the XML file, passing in the XSD schemas
# xsd = {'urn:iso:std:iso:20022:tech:xsd:camt.052.001.02': camt052_xsd,
#        'urn:iso:std:iso:20022:tech:xsd:camt.053.001.02': camt053_xsd}
# xml_file = 'statement_short.xml'
# d = camt052_xsd.to_dict(xml_file, process_namespaces=True)

# Load the XSD file for the namespace 'urn:iso:std:iso:20022:tech:xsd:camt.053.001.02'
xsd_file = 'camt.052.001.02.xsd'
camt053_xsd = xmlschema.XMLSchema(xsd_file)

# Generate a dictionary from an XML file using the XSD schema
xml_file = 'statement.xml'
d = camt053_xsd.to_dict(xml_file, process_namespaces=True)


# Print the resulting dictionary
#pprint.pprint(d)

for element_name in camt053_xsd.iter():
    #print(element_name.name)
    print(element_name)


