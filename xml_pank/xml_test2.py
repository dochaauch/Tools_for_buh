from lxml import etree

# Load the XML file
tree = etree.parse('statement_short.xml')

# Get the root element
root = tree.getroot()

# Get the namespace from the root element
ns = root.nsmap.get(None)
print(ns)

# # Define the XPath expressions for the data you want to extract
# expr_tx_inf = f".//{{{ns}}}Ntry// {{{ns}}}NtryDtls// {{{ns}}}TxDtls"
# expr_amt = f".//{{{ns}}}AmtDtls/{{{ns}}}TxAmt/{{{ns}}}Amt"
# expr_curr = f".//{{{ns}}}AmtDtls/{{{ns}}}TxAmt/{{{ns}}}Ccy"
# expr_date = f".//{{{ns}}}ValDt/{{{ns}}}Dt"
#
# print(expr_tx_inf)
#
# # Extract the data using XPath expressions
# tx_info = []
# for tx in root.xpath(expr_tx_inf, namespaces={'ns': ns}):
#     amt = tx.xpath(expr_amt, namespaces={'ns': ns})[0].text
#     curr = tx.xpath(expr_curr, namespaces={'ns': ns})[0].text
#     date = tx.xpath(expr_date, namespaces={'ns': ns})[0].text
#     tx_info.append({'Amount': amt, 'Currency': curr, 'Date': date})
#
# # Print the extracted data
# print(tx_info)


# extract the MsgId and CreDtTm elements from GrpHdr
msg_id = root.find('.//{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}MsgId').text
cre_dt_tm = root.find('.//{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}CreDtTm').text

# extract the Id, ElctrncSeqNb, and CreDtTm elements from Stmt
stmt_id = root.find('.//{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}Id').text
seq_nb = root.find('.//{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}ElctrncSeqNb').text
stmt_cre_dt_tm = root.find('.//{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}CreDtTm').text

# extract the IBAN and Ccy elements from Acct/Id
iban = root.find('.//{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}IBAN').text
ccy_s = root.findall(f".//{{{ns}}}Amt[@Ccy='EUR']")

# print the extracted elements
print(f"MsgId: {msg_id}")
print(f"CreDtTm: {cre_dt_tm}")
print(f"Stmt Id: {stmt_id}")
print(f"ElctrncSeqNb: {seq_nb}")
print(f"Stmt CreDtTm: {stmt_cre_dt_tm}")
print(f"IBAN: {iban}")

#print(f"Ccy: {ccy}")

for ccy in ccy_s:
    print(f"Ccy: {ccy.text}")
