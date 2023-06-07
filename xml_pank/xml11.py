import pprint

from sepa import parser
import re
import pandas as pd

# Utility function to remove additional namespaces from the XML
def strip_namespace(xml):
    return re.sub(' xmlns="[^"]+"', '', xml, count=1)

# Read file
with open('statement_short.xml', 'r') as f:
    input_data = f.read()

# Parse the bank statement XML to dictionary
camt_dict = parser.parse_string(parser.bank_to_customer_statement, bytes(strip_namespace(input_data), 'utf8'))

statements = pd.DataFrame.from_dict(camt_dict['statements'])


all_entries = []
for i,_ in statements.iterrows():
    if 'entries' in camt_dict['statements'][i]:
        df = pd.DataFrame()
        dd = pd.DataFrame.from_records(camt_dict['statements'][i]['entries'])
        df['Date'] = dd['value_date'].str['date']
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
        iban = camt_dict['statements'][i]['account']['id']['iban']
        df['IBAN'] = iban
        df['Currency'] = dd['amount'].str['currency']
        all_entries.append(df)

pprint.pp(all_entries)
df_entries = pd.concat(all_entries)

print(statements.to_string())