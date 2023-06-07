import camt_to_bankstatement from sepa

# Load the CAMT.053 file into a string
#with open('statement.camt053', 'r') as f:
with open('statement.xml', 'r') as f:
    camt_str = f.read()

# Parse the CAMT.053 file into a list of BankStatement objects
statements = camt_to_bankstatement(camt_str)

# Iterate over each BankStatement object and print its details
for statement in statements:
    print('Account holder:', statement.holder_name)
    print('Account number:', statement.iban)
    print('Statement date:', statement.date)
    print('Opening balance:', statement.opening_balance)
    print('Closing balance:', statement.closing_balance)
    for transaction in statement.transactions:
        print('Transaction date:', transaction.date)
        print('Transaction amount:', transaction.amount)
        print('Transaction description:', transaction.description)
