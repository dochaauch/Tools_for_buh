from sepa import parser

# Read file
# with open('statement_short.xml', 'r') as f:
#     data_in = f.read()
#
# print(data_in)

data_in = ('<MndtInitnReq>'
    '<GrpHdr></GrpHdr>'
    '<Mndt>'
        '<MndtId>78904536</MndtdId>'
        '<MndtReqId>9823701</MndtReqId>'
        '<Authntcn>'
            '<Dt>2017-03-05</Dt>'
            '<Chanl><Cd>ABC</Cd></Chanl>'
        '</Authntcn>'
    '</Mndt>'
'</MndtInitnReq>')

data_out = parser.parse_string(parser.mandate_initiation_request, data_in)
print(data_out)
