import xml.etree.ElementTree as ET
import pandas as pd

# parse the xml file
tree = ET.parse('statement_short.xml')
root = tree.getroot()

# define the namespace
ns = {'ns': 'urn:iso:std:iso:20022:tech:xsd:camt.053.001.02'}

# create empty lists to store the data
msg_id = []
cre_dt_tm = []
stmt_id = []
elctrnc_seq_nb = []
stmt_cre_dt_tm = []
fr_dt_tm = []
to_dt_tm = []
iban = []
ccy = []
owner_nm = []
owner_ctry = []
owner_addr_line = []
owner_id = []
bic = []
bic_nm = []
bic_ctry = []
bic_addr_line = []
bic_id = []
bal_tp_cd = []
bal_amt = []
bal_dt = []

ntry_ref = []
ntry_amt = []
ntry_cd = []
ntry_sts = []
ntry_bookg_dt = []
ntry_val_dt = []
ntry_acct_svcr_ref = []
ntry_bktxcd_pmnt_cd = []
ntry_bktxcd_icdt_cd = []
ntry_bktxcd_autt_cd = []
bic_othr_bktxcd_mk_cd = []
bic_othr_bktxcd_issr = []

# iterate through the xml elements and extract the data
for child in root.findall('.//ns:BkToCstmrStmt', ns):
    for stmt in child.findall('ns:Stmt', ns):
        for acct in stmt.findall('ns:Acct', ns):
            iban.append(acct.find('.//ns:IBAN', ns).text)
            ccy.append(acct.find('ns:Ccy', ns).text)
            for owner in acct.findall('ns:Ownr', ns):
                owner_nm.append(owner.find('.//ns:Nm', ns).text)
                owner_ctry.append(owner.find('.//ns:Ctry', ns).text)
                owner_addr_line.append(owner.find('.//ns:AdrLine', ns).text)
                for org_id in owner.findall('.//ns:OrgId', ns):
                    owner_id.append(org_id.find('.//ns:Id', ns).text)
            for svcr in acct.findall('ns:Svcr', ns):
                bic.append(svcr.find('.//ns:BIC', ns).text)
                bic_nm.append(svcr.find('.//ns:Nm', ns).text)
                bic_ctry.append(svcr.find('.//ns:Ctry', ns).text)
                bic_addr_line.append(svcr.find('.//ns:AdrLine', ns).text)
                for othr in svcr.findall('.//ns:Othr', ns):
                    bic_id.append(othr.find('.//ns:Id', ns).text)
                    bic_othr_bktxcd_mk_cd.append(othr.find('.//ns:Cd', ns).text)
                    if othr.find('.//ns:Issr', ns) is not None:
                        bic_othr_bktxcd_issr.append(othr.find('.//ns:Issr', ns).text)
                    else:
                        bic_othr_bktxcd_issr.append(None)
        for bal in stmt.findall('ns:Bal', ns):
            bal_tp_cd.append(bal.find('.//ns:Cd', ns).text)
            bal_amt.append(float(bal.find('.//ns:Amt', ns).text))
            bal_dt.append(bal.find('.//ns:Dt', ns).text)
        for ntry in stmt.findall('ns:Ntry', ns):
            ntry_ref.append(ntry.find('.//ns:NtryRef', ns).text)
            ntry_amt.append(float(ntry.find('.//ns:Amt', ns).text))
            ntry_cd.append(ntry.find('.//ns:Cd', ns).text)
            ntry_sts.append(ntry.find('.//ns:Sts', ns).text)
            ntry_bookg_dt.append(ntry.find('.//ns:BookgDt/ns:Dt', ns).text)
            ntry_val_dt.append(ntry.find('.//ns:ValDt/ns:Dt', ns).text)
            ntry_acct_svcr_ref.append(ntry.find('.//ns:AcctSvcrRef', ns).text)
            for bktxcd in ntry.findall('.//ns:BkTxCd', ns):
                if bktxcd.find('.//ns:PmtTpInf/ns:LclInstrm/ns:Cd', ns) is not None:
                    ntry_bktxcd_pmnt_cd.append(bktxcd.find('.//ns:PmtTpInf/ns:LclInstrm/ns:Cd', ns).text)
                else:
                    ntry_bktxcd_pmnt_cd.append(None)
                if bktxcd.find('.//ns:PmtTpInf/ns:CtgyPurp/ns:Cd', ns) is not None:
                    ntry_bktxcd_icdt_cd.append(bktxcd.find('.//ns:PmtTpInf/ns:CtgyPurp/ns:Cd', ns).text)
                else:
                    ntry_bktxcd_icdt_cd.append(None)
                if bktxcd.find('.//ns:Prtry', ns) is not None:
                    ntry_bktxcd_autt_cd.append(bktxcd.find('.//ns:Prtry', ns).text)
                else:
                    ntry_bktxcd_autt_cd.append("")

data_gen = {'Message ID': msg_id,
'Creation Date and Time': cre_dt_tm,
'Statement ID': stmt_id,
'Electronic Sequence Number': elctrnc_seq_nb,
'Statement Creation Date and Time': stmt_cre_dt_tm,
'From Date and Time': fr_dt_tm,
'To Date and Time': to_dt_tm,
'IBAN': iban,
'Currency': ccy,
'Owner Name': owner_nm,
'Owner Country': owner_ctry,
'Owner Address Line': owner_addr_line,
'Owner ID': owner_id,
'BIC': bic,
'BIC Name': bic_nm,
'BIC Country': bic_ctry,
'BIC Address Line': bic_addr_line,
'BIC ID': bic_id,
'Balance Type Code': bal_tp_cd,
'Balance Amount': bal_amt,
'Balance Date': bal_dt,
'Entry Bank Transaction Marker Code': bic_othr_bktxcd_mk_cd,
'Entry Bank Transaction Issuer': bic_othr_bktxcd_issr,
            }

trans_data = {
'Entry Reference': ntry_ref,
'Entry Amount': ntry_amt,
'Entry Code': ntry_cd,
'Entry Status': ntry_sts,
'Entry Booking Date': ntry_bookg_dt,
'Entry Value Date': ntry_val_dt,
'Entry Account Servicer Reference': ntry_acct_svcr_ref,
'Entry Bank Transaction Payment Code': ntry_bktxcd_pmnt_cd,
'Entry Bank Transaction Category Purpose Code': ntry_bktxcd_icdt_cd,
'Entry Bank Transaction Authentication Code': ntry_bktxcd_autt_cd,
 }

print(data_gen)
print()
print(trans_data)

df = pd.DataFrame(trans_data)

print(df.to_string())
