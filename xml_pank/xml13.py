import xmltodict
import pandas as pd
from flatten_json import flatten

with open("statement.xml", "r") as f:
    xml_data = f.read()

xml_dict = xmltodict.parse(xml_data)

transaction_list = xml_dict["Document"]["BkToCstmrAcctRpt"]["Rpt"]["Ntry"]

# Flatten each transaction and store the results in a list
flattened_transactions = [flatten(transaction) for transaction in transaction_list]

# Convert the list of flattened transactions to a Pandas DataFrame
df = pd.DataFrame(flattened_transactions)
print(df.columns)

# Select only the columns we want in the final output
columns_to_keep = [
    "NtryRef",
    "TxDtTm",
    "CdtDbtInd",
    "Amt.@Ccy",
    "Amt.#text",
    "BkTxCd.Prtry.#text",
    "NtryDtls.TxDtls.RmtInf.Ustrd"
]
df = df[columns_to_keep]

# Rename the columns to be more readable
column_names = {
    "NtryRef": "Entry Reference",
    "TxDtTm": "Transaction Date/Time",
    "CdtDbtInd": "Credit/Debit Indicator",
    "Amt.@Ccy": "Currency",
    "Amt.#text": "Amount",
    "BkTxCd.Prtry.#text": "Bank Transaction Code",
    "NtryDtls.TxDtls.RmtInf.Ustrd": "Transaction Details"
}

df = pd.DataFrame(flattened_transactions)[list(column_names.keys())].rename(columns=column_names)
print(df.to_string())