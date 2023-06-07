import xml.etree.ElementTree as ET

# Load XML file
tree = ET.parse('statement_short.xml')
root = tree.getroot()

# Define namespace
ns = {'ns': 'urn:iso:std:iso:20022:tech:xsd:camt.052.001.02'}

# Loop over reports
for rpt in root.findall('.//ns:Rpt', ns):

    # Get report details
    rpt_id = rpt.find('.//ns:Id', ns).text
    rpt_elm = rpt.find('.//ns:Elm', ns).text
    rpt_cre_dt_tm = rpt.find('.//ns:CreDtTm', ns).text
    rpt_fr_to_dt = rpt.find('.//ns:FrToDt', ns)
    rpt_fr_dt = rpt_fr_to_dt.find('.//ns:FrDtTm', ns).text
    rpt_to_dt = rpt_fr_to_dt.find('.//ns:ToDtTm', ns).text
    rpt_cpy_dplct_ind = rpt.find('.//ns:CpyDplctInd', ns).text

    # Loop over accounts
    for acct in rpt.findall('.//ns:Acct', ns):

        # Get account details
        acct_id = acct.find('.//ns:Id', ns).text
        acct_tp = acct.find('.//ns:Tp', ns).find('.//ns:Cd', ns).text
        acct_ccy = acct.find('.//ns:Ccy', ns).text
        acct_schm_nm = acct.find('.//ns:SchmeNm', ns).find('.//ns:Cd', ns).text
        acct_ownr = acct.find('.//ns:Ownr', ns).find('.//ns:Nm', ns).text

        # Loop over entries
        for ntry in acct.findall('.//ns:Ntry', ns):

            # Get entry details
            ntry_amt = ntry.find('.//ns:Amt', ns).text
            ntry_cdt_dbt_ind = ntry.find('.//ns:CdtDbtInd', ns).text
            ntry_sts = ntry.find('.//ns:Sts', ns).text
            ntry_bookg_dt = ntry.find('.//ns:BookgDt', ns).find('.//ns:Dt', ns).text
            ntry_val_dt = ntry.find('.//ns:ValDt', ns).find('.//ns:Dt', ns).text
            ntry_bk_tx_inf = ntry.findall('.//ns:BkTxCd', ns)

            # Loop over bank transaction codes
            for bk_tx_cd in ntry_bk_tx_inf:
                ntry_bk_tx_cd_cd = bk_tx_cd.find('.//ns:Cd', ns).text
                ntry_bk_tx_cd_issr = bk_tx_cd.find('.//ns:Issr', ns).text

            # Loop over transaction details
            for tx_dtls in ntry.findall('.//ns:TxDtls', ns):
                tx_dtls_rmt_inf = tx_dtls.find('.//ns:RmtInf', ns).find('.//ns:Strd', ns).find('.//ns:RfrdDocInf',
                                                                                               ns)
                tx_dtls_rmt_inf_rfrd_doc_tp = tx_dtls_rmt_inf.find('.//ns:Tp', ns).find('.//ns:Cd', ns).text
                tx_dtls_rmt_inf_rfrd_doc_nb = tx_dtls_rmt_inf.find('.//ns:Nb', ns).text
                tx_dtls_rmt_inf_rfrd_doc_rltd_dt = tx_dtls_rmt_inf.find('.//ns:RltdDt', ns).text
                tx_dtls_rmt_inf_rfrd_doc_amt = tx_dtls_rmt_inf.find('.//ns:Amt', ns).text
                tx_dtls_rmt_inf_rfrd_doc_cy = tx_dtls_rmt_inf.find('.//ns:Ccy', ns).text

print(ntry)