import pandas as pd
from lxml import etree
import os


def create_xml_from_excel(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    root = etree.Element("E_Invoice")

    for invoice_id in df["InvoiceId"].unique():
        invoice_data = df[df["InvoiceId"] == invoice_id]

        # Header
        header_el = etree.SubElement(root, "Header")
        for _, row in invoice_data[invoice_data["Section"] == "Header"].iterrows():
            etree.SubElement(header_el, row["Key"]).text = str(row["Value"]).split()[0]  # Оставляем только дату

        # Invoice
        invoice_attrs = {row["Key"]: str(row["Value"]) for _, row in invoice_data[invoice_data["Section"] == "Invoice"].iterrows()}
        invoice_attrs["invoiceId"] = str(invoice_id)
        invoice_el = etree.SubElement(root, "Invoice", **invoice_attrs)

        # InvoiceParties
        parties_el = etree.SubElement(invoice_el, "InvoiceParties")
        for party in ["SellerParty", "BuyerParty"]:
            party_el = etree.SubElement(parties_el, party)
            party_data = invoice_data[invoice_data["Section"] == party]
            # Порядок элементов: Name, RegNumber, VATRegNumber, ContactData, AccountInfo
            for _, row in party_data.iterrows():
                key = row["Key"]
                value = str(row["Value"])
                if key in ["Name", "RegNumber", "VATRegNumber"]:
                    etree.SubElement(party_el, key).text = value
            contact_data_el = etree.SubElement(party_el, "ContactData")
            for _, row in party_data.iterrows():
                key = row["Key"]
                value = str(row["Value"])
                if key == "ContactName":
                    etree.SubElement(contact_data_el, key).text = value
            for _, row in party_data.iterrows():
                key = row["Key"]
                value = str(row["Value"])
                if key in ["PhoneNumber", "E-mailAddress"]:
                    etree.SubElement(contact_data_el, key).text = value
            legal_address_el = etree.SubElement(contact_data_el, "LegalAddress")
            for _, row in party_data.iterrows():
                key = row["Key"]
                value = str(row["Value"])
                if key in ["PostalAddress1", "City", "PostalCode"]:
                    etree.SubElement(legal_address_el, key).text = value
            if party == "SellerParty":
                account_info_el = etree.SubElement(party_el, "AccountInfo")
                for _, row in party_data.iterrows():
                    key = row["Key"]
                    value = str(row["Value"])
                    if key in ["AccountNumber", "IBAN", "BankName"]:
                        etree.SubElement(account_info_el, key).text = value

        # InvoiceInformation
        info_el = etree.SubElement(invoice_el, "InvoiceInformation")
        for _, row in invoice_data[invoice_data["Section"] == "InvoiceInformation"].iterrows():
            if row["Key"] == "Type":
                etree.SubElement(info_el, "Type", type=row["Value"])
            else:
                etree.SubElement(info_el, row["Key"]).text = str(row["Value"]).split()[0]  # Оставляем только дату

        # InvoiceSumGroup
        sum_group_el = etree.SubElement(invoice_el, "InvoiceSumGroup")
        total_sum = None
        for _, row in invoice_data[invoice_data["Section"] == "InvoiceSumGroup"].iterrows():
            key = row["Key"]
            value = "{:.2f}".format(float(row["Value"]))  # Форматируем числовые значения с двумя знаками после запятой
            etree.SubElement(sum_group_el, key).text = value
            if key == "TotalSum":
                total_sum = value
        # Добавляем недостающие элементы
        etree.SubElement(sum_group_el, "TotalVATSum").text = "{:.2f}".format(float(invoice_data[invoice_data["Key"] == "VATSum"]["Value"].values[0]))
        etree.SubElement(sum_group_el, "TotalToPay").text = total_sum
        etree.SubElement(sum_group_el, "Currency").text = "EUR"

        # InvoiceItems
        items_el = etree.SubElement(invoice_el, "InvoiceItem")
        item_group_el = etree.SubElement(items_el, "InvoiceItemGroup")
        item_entries = invoice_data[invoice_data["Section"] == "InvoiceItem"]
        for i in range(0, len(item_entries), 2):
            item_entry_el = etree.SubElement(item_group_el, "ItemEntry")
            description = item_entries.iloc[i]["Value"]
            item_sum = item_entries.iloc[i + 1]["Value"] if i + 1 < len(item_entries) else "0.00"
            etree.SubElement(item_entry_el, "Description").text = description
            etree.SubElement(item_entry_el, "ItemSum").text = "{:.2f}".format(float(item_sum))

        # AdditionalInformation
        additional_info_el = etree.SubElement(invoice_el, "AdditionalInformation", id="Note")
        etree.SubElement(additional_info_el, "InformationName")  # Пустой элемент
        for _, row in invoice_data[invoice_data["Section"] == "AdditionalInfo"].iterrows():
            etree.SubElement(additional_info_el, row["Key"]).text = str(row["Value"]).replace('\n', '\n  ')

        # PaymentInfo
        payment_info_el = etree.SubElement(invoice_el, "PaymentInfo")
        for _, row in invoice_data[invoice_data["Section"] == "PaymentInfo"].iterrows():
            key = row["Key"]
            value = str(row["Value"]).split()[0] if "Date" in key else str(row["Value"])
            etree.SubElement(payment_info_el, key).text = value
        etree.SubElement(payment_info_el, "PaymentTotalSum").text = total_sum
        etree.SubElement(payment_info_el, "PayerName").text = str(invoice_data[invoice_data["Section"] == "BuyerParty"]["Value"].values[0])
        etree.SubElement(payment_info_el, "PaymentId").text = str(invoice_data[invoice_data["Key"] == "InvoiceNumber"]["Value"].values[0])
        etree.SubElement(payment_info_el, "PayToAccount").text = str(invoice_data[invoice_data["Key"] == "IBAN"]["Value"].values[0])
        etree.SubElement(payment_info_el, "PayToName").text = str(invoice_data[invoice_data["Section"] == "SellerParty"]["Value"].values[0])

        # Footer
        footer_el = etree.SubElement(root, "Footer")
        for _, row in invoice_data[invoice_data["Section"] == "Footer"].iterrows():
            etree.SubElement(footer_el, row["Key"]).text = str(row["Value"])
        etree.SubElement(footer_el, "TotalAmount").text = total_sum

    return etree.tostring(root, pretty_print=True, encoding="UTF-8", xml_declaration=True)


# Путь к исходному файлу
file_path = "/Users/docha/Library/CloudStorage/GoogleDrive-mob37256213753@gmail.com/Мой диск/Bonus/2024-11/earve.xlsx"

# Генерация XML
xml_content = create_xml_from_excel(file_path)

# Определение директории исходного файла
output_directory = os.path.dirname(file_path)

# Имя выходного файла
output_file = os.path.join(output_directory, "output_invoice.xml")

# Сохранение файла
with open(output_file, "wb") as f:
    f.write(xml_content)

print(f"XML файл сохранён в {output_file}")
