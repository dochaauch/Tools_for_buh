import PyPDF2
import xml.etree.ElementTree as ET
from xml.dom import minidom


# Чтение PDF-файла и извлечение текста
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ""
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text += page.extract_text()
    return text


# Парсинг текста и извлечение данных счета
def parse_invoice_text(text):
    lines = text.split('\n')
    invoice_data = {
        'invoice_lines': []
    }

    for line in lines:
        print(f"Parsing line: {line}")  # Debug print
        if line.startswith('BONUS TÕLKEBÜROO OÜ'):
            invoice_data['seller'] = 'BONUS TÕLKEBÜROO OÜ'
        if 'Reg. nr' in line:
            parts = line.split('Reg. nr')
            invoice_data['seller_reg_nr'] = parts[1].split()[0]
            invoice_data['seller_vat'] = line.split('KMK')[1].split()[0]
            invoice_data['seller_phone'] = line.split('Tel.')[1].strip()
        if 'Estonia pst' in line:
            invoice_data['seller_address'] = line.strip()
        if 'SEB Pank' in line:
            invoice_data['seller_bank'] = 'SEB Pank'
        if 'IBAN:' in line:
            invoice_data['seller_iban'] = line.split('IBAN:')[1].strip()
        if 'KLIENT:' in line:
            invoice_data['buyer'] = line.split('KLIENT:')[1].strip()
        if 'TELLIJA:' in line:
            invoice_data['buyer_contact'] = line.split('TELLIJA:')[1].strip().replace(' ä', 'ä')
        if 'ARVE  NR' in line:
            invoice_data['invoice_number'] = line.split('ARVE  NR')[1].strip()
        if 'Tõlketeenus' in line:
            invoice_data['service_description'] = ' '.join(line.split()).replace(' ,', ',')
        if 'Projektide tundide arvestus perioodil' in line:
            invoice_data['service_period'] = ' '.join(line.split())
        if 'Summa KM -ta' in line:
            invoice_data['subtotal'] = line.split(':')[-1].strip().replace(' ', '').replace(',', '.')
        if 'Käibemaks' in line:
            invoice_data['vat'] = line.split(':')[-1].strip().replace(' ', '').replace(',', '.')
        if 'Kokku' in line:
            invoice_data['total'] = line.split(':')[-1].strip().replace(' ', '').replace(',', '.')
        if 'Kuupäev:' in line:
            invoice_data['invoice_date'] = line.split('Kuupäev:')[1].split('Maksetähtaeg:')[0].strip()
            invoice_data['due_date'] = line.split('Maksetähtaeg:')[1].strip()
        if line.strip() and line.split()[0].isdigit():
            parts = line.split()
            invoice_line = {
                'date': parts[1],
                'description': ' '.join(parts[2:-2]),
                'quantity': '1',  # Default quantity to 1 since not specified
                'price': parts[-1].replace(',', '.'),
                'total': parts[-1].replace(',', '.')
            }
            invoice_data['invoice_lines'].append(invoice_line)

    print(f"Parsed invoice data: {invoice_data}")  # Debug print
    return invoice_data


# Проверка наличия всех необходимых данных
def check_missing_data(invoice_data):
    required_keys = [
        'seller', 'seller_reg_nr', 'seller_vat', 'seller_phone', 'seller_address', 'seller_bank', 'seller_iban',
        'buyer', 'buyer_contact', 'invoice_number', 'service_description', 'service_period',
        'subtotal', 'vat', 'total', 'invoice_date', 'due_date'
    ]
    missing_keys = [key for key in required_keys if key not in invoice_data]
    if missing_keys:
        print(f"Missing data for keys: {', '.join(missing_keys)}")


# Форматирование XML-документа
def prettify_xml(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


# Создание XML-документа e-arve
def create_e_arve_xml(invoice_data):
    invoice = ET.Element("Invoice", invoiceId=invoice_data.get('invoice_number', 'N/A'),
                         sellerRegnumber=invoice_data.get('seller_reg_nr', 'N/A'))

    invoice_number = ET.SubElement(invoice, "InvoiceNumber")
    invoice_number.text = invoice_data.get('invoice_number', 'N/A')

    invoice_date = ET.SubElement(invoice, "InvoiceDate")
    invoice_date.text = invoice_data.get('invoice_date', 'N/A')

    due_date = ET.SubElement(invoice, "DueDate")
    due_date.text = invoice_data.get('due_date', 'N/A')

    currency_code = ET.SubElement(invoice, "DocumentCurrencyCode")
    currency_code.text = "EUR"

    invoice_parties = ET.SubElement(invoice, "InvoiceParties")

    seller = ET.SubElement(invoice_parties, "SellerParty")
    seller_name = ET.SubElement(seller, "PartyName")
    seller_name.text = invoice_data.get('seller', 'N/A')
    seller_address = ET.SubElement(seller, "PostalAddress")
    seller_address.text = invoice_data.get('seller_address', 'N/A')
    seller_reg = ET.SubElement(seller, "CompanyID")
    seller_reg.text = invoice_data.get('seller_reg_nr', 'N/A')
    seller_vat = ET.SubElement(seller, "TaxScheme")
    seller_vat_id = ET.SubElement(seller_vat, "ID")
    seller_vat_id.text = invoice_data.get('seller_vat', 'N/A')
    seller_phone = ET.SubElement(seller, "Telephone")
    seller_phone.text = invoice_data.get('seller_phone', 'N/A')
    seller_bank = ET.SubElement(seller, "FinancialInstitution")
    seller_bank.text = invoice_data.get('seller_bank', 'N/A')
    seller_iban = ET.SubElement(seller, "IBAN")
    seller_iban.text = invoice_data.get('seller_iban', 'N/A')

    buyer = ET.SubElement(invoice_parties, "BuyerParty")
    buyer_name = ET.SubElement(buyer, "PartyName")
    buyer_name.text = invoice_data.get('buyer', 'N/A')
    buyer_contact = ET.SubElement(buyer, "Contact")
    buyer_contact.text = invoice_data.get('buyer_contact', 'N/A')

    service_description = ET.SubElement(invoice, "ServiceDescription")
    service_description.text = invoice_data.get('service_description', 'N/A')

    service_period = ET.SubElement(invoice, "ServicePeriod")
    service_period.text = invoice_data.get('service_period', 'N/A')

    for line in invoice_data['invoice_lines']:
        invoice_line = ET.SubElement(invoice, "InvoiceLine")
        line_item = ET.SubElement(invoice_line, "LineItem")
        description = ET.SubElement(line_item, "Description")
        description.text = ' '.join(line['description'].split())
        quantity = ET.SubElement(line_item, "Quantity", unitCode="EA")
        quantity.text = line['quantity']
        price = ET.SubElement(line_item, "Price")
        price.text = line['price']
        line_extension_amount = ET.SubElement(invoice_line, "LineExtensionAmount", currencyID="EUR")
        line_extension_amount.text = line['total']

    legal_monetary_total = ET.SubElement(invoice, "LegalMonetaryTotal")
    line_extension_amount = ET.SubElement(legal_monetary_total, "LineExtensionAmount", currencyID="EUR")
    line_extension_amount.text = invoice_data.get('subtotal', 'N/A')
    tax_exclusive_amount = ET.SubElement(legal_monetary_total, "TaxExclusiveAmount", currencyID="EUR")
    tax_exclusive_amount.text = invoice_data.get('subtotal', 'N/A')
    tax_inclusive_amount = ET.SubElement(legal_monetary_total, "TaxInclusiveAmount", currencyID="EUR")
    tax_inclusive_amount.text = invoice_data.get('total', 'N/A')
    payable_amount = ET.SubElement(legal_monetary_total, "PayableAmount", currencyID="EUR")
    payable_amount.text = invoice_data.get('total', 'N/A')

    pretty_xml_as_string = prettify_xml(invoice)
    with open("e-arve.xml", "w", encoding="utf-8") as file:
        file.write(pretty_xml_as_string)


pdf_path = '/Users/docha/Downloads/020724_Arve_Bonus.pdf'
text = extract_text_from_pdf(pdf_path)
invoice_data = parse_invoice_text(text)
check_missing_data(invoice_data)
create_e_arve_xml(invoice_data)
